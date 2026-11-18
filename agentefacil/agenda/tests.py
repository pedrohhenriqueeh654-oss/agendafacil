from concurrent.futures import ThreadPoolExecutor
from datetime import time, timedelta
from threading import Barrier
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.db import close_old_connections
from django.test import Client, TestCase, TransactionTestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from .booking import reserve
from .models import Appointment, Availability, Service, User


def scenario():
    day = timezone.localdate() + timedelta(days=1)
    pro = User.objects.create_user("carlos@agenda.example", first_name="Carlos", role=User.Role.PRO)
    ana = User.objects.create_user("ana@agenda.example")
    bela = User.objects.create_user("bela@agenda.example")
    service = Service.objects.create(professional=pro, name="Corte masculino", duration=30, price=40)
    Availability.objects.create(professional=pro, weekday=day.weekday(), start=time(9), end=time(12))
    return day, pro, ana, bela, service


class AgendaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.day, cls.pro, cls.ana, cls.bela, cls.service = scenario()

    def data(self, **kwargs):
        return {"service": self.service.pk, "date": self.day.isoformat(), **kwargs}

    def test_signup_password_hash_and_login(self):
        password = "EfeitoBrisa!4627D"
        data = {"first_name": "Lu", "email": "LU@agenda.example", "role": "client",
                "password1": password, "password2": password}
        self.assertContains(self.client.get(reverse("home")), "Entrar no AgendaFácil")
        self.assertRedirects(self.client.post(reverse("signup"), data), reverse("dashboard"),
                             fetch_redirect_response=False)
        user = User.objects.get(email="lu@agenda.example")
        self.assertNotEqual(password, user.password)
        self.assertTrue(user.check_password(password))
        self.assertRedirects(self.client.post(reverse("logout")), reverse("home"))
        self.assertRedirects(self.client.post(reverse("home"), {"username": "LU@agenda.example", "password": password}),
                             reverse("dashboard"), fetch_redirect_response=False)
        self.client.logout()
        self.assertContains(self.client.post(reverse("signup"), data), "errorlist")
        self.assertEqual(User.objects.filter(email="lu@agenda.example").count(), 1)

    def test_booking_flow(self):
        self.client.force_login(self.ana)
        self.assertContains(self.client.get(reverse("booking"), self.data()), "09:00:00")
        response = self.client.post(reverse("booking"), self.data(start="09:00"), follow=True)
        self.assertContains(response, "Agendamento confirmado!")
        self.assertEqual(Appointment.objects.get().end, time(9, 30))
        self.assertContains(self.client.get(reverse("history")), "Corte masculino")

    def test_stale_or_overlapping_times(self):
        reserve(self.ana, self.service.pk, self.day, time(9))
        self.client.force_login(self.bela)
        self.assertNotContains(self.client.get(reverse("booking"), self.data()), "09:15:00")
        self.assertContains(self.client.post(reverse("booking"), self.data(start="09:15")),
                            "escolha outro", status_code=409)
        self.assertEqual(Appointment.objects.count(), 1)
        self.assertEqual(reserve(self.bela, self.service.pk, self.day, time(9, 30)).start, time(9, 30))

    def test_inaccessible_other_accounts_and_anonymous(self):
        record = reserve(self.ana, self.service.pk, self.day, time(9))
        url = reverse("confirmation", args=[record.pk])
        self.assertEqual(self.client.get(url).status_code, 302)
        self.client.force_login(self.bela)
        self.assertEqual(self.client.get(url).status_code, 404)
        self.assertEqual(self.client.get(reverse("professional")).status_code, 403)

    def test_professional_can_register_service_and_availability(self):
        self.client.force_login(self.pro)
        url = reverse("professional")
        response = self.client.post(url, {"action": "service", "service-name": "Barba",
                                          "service-duration": 40, "service-price": "35,00"}, follow=True)
        self.assertContains(response, "Serviço cadastrado.")
        period = {"action": "hours", "hours-weekday": self.day.weekday(), "hours-start": "13:00", "hours-end": "17:00"}
        self.assertContains(self.client.post(url, period, follow=True), "Disponibilidade cadastrada.")
        self.assertContains(self.client.post(url, period), "sobrepõe")
        self.assertEqual(Availability.objects.filter(professional=self.pro).count(), 2)

    def test_reservation_requires_csrf(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.ana)
        response = client.post(reverse("booking"), self.data(start="09:00"))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Appointment.objects.count(), 0)

    @override_settings(DEBUG=True)
    def test_seed_is_repeatable_and_has_no_usable_password(self):
        call_command("dados_demo", verbosity=0)
        call_command("dados_demo", verbosity=0)
        self.assertFalse(self.pro.has_usable_password())
        self.assertEqual(Service.objects.filter(professional=self.pro, name="Corte masculino").count(), 1)


class ConcurrencyTest(TransactionTestCase):
    def test_simultaneous_requests_for_overlapping_slots(self):
        day, _, first, second, service = scenario()
        barrier = Barrier(2)

        def request(user, start):
            close_old_connections()
            try:
                barrier.wait(timeout=5)
                reserve(user, service.pk, day, start)
                return "confirmado"
            except ValidationError:
                return "indisponível"
            finally:
                close_old_connections()

        with ThreadPoolExecutor(max_workers=2) as pool:
            one = pool.submit(request, first, time(9))
            two = pool.submit(request, second, time(9, 15))
            outcomes = [one.result(timeout=15), two.result(timeout=15)]
        self.assertCountEqual(outcomes, ["confirmado", "indisponível"])
        self.assertEqual(Appointment.objects.count(), 1)
