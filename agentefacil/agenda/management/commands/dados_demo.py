from datetime import time
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import transaction
from agenda.models import Availability, Service, User


class Command(BaseCommand):
    help = "Cria um profissional fictício, um serviço e horários para testes locais."

    @transaction.atomic
    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError("A demonstração só pode ser criada em modo local.")
        person, created = User.objects.get_or_create(email="carlos@agenda.example", defaults={
            "first_name": "Carlos", "last_name": "Lima", "role": User.Role.PRO,
        })
        if created:
            person.set_unusable_password()
            person.save(update_fields=["password"])
        if person.role != User.Role.PRO:
            raise CommandError("O e-mail fictício já está cadastrado com outro perfil.")
        Service.objects.get_or_create(professional=person, name="Corte masculino", defaults={"duration": 30, "price": 40})
        for weekday in range(6):
            Availability.objects.get_or_create(professional=person, weekday=weekday, start=time(9), end=time(17))
        self.stdout.write(self.style.SUCCESS("Demonstração pronta. Crie uma conta de cliente e escolha uma data de segunda a sábado."))
