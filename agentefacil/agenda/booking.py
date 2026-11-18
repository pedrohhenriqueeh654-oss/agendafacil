"""Regras do fluxo de reserva. A interface não decide quais horários são válidos."""
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from .models import Appointment, Availability, Service

STEP = timedelta(minutes=15)


def slots(service, day):
    now = timezone.localtime().replace(tzinfo=None)
    if day < now.date() or day > now.date() + timedelta(days=90):
        return []
    duration = timedelta(minutes=service.duration)
    periods = Availability.objects.filter(professional=service.professional, weekday=day.weekday(), active=True)
    occupied = list(Appointment.objects.filter(
        professional=service.professional, date=day, status=Appointment.Status.CONFIRMED
    ).values_list("start", "end"))
    available = set()
    for period in periods:
        current = datetime.combine(day, period.start)
        end_of_period = datetime.combine(day, period.end)
        while current + duration <= end_of_period:
            end = (current + duration).time()
            start = current.time()
            if current > now and not any(start < used_end and end > used_start for used_start, used_end in occupied):
                available.add(start)
            current += STEP
    return sorted(available)


@transaction.atomic
def reserve(client, service_id, day, start):
    # No SQLite, BEGIN IMMEDIATE serializa a consulta e a gravação dos escritores.
    service = Service.objects.select_related("professional").filter(
        pk=service_id, active=True, professional__is_active=True,
        professional__role="pro",
    ).first()
    if not service or start not in slots(service, day):
        raise ValidationError("Esse horário não está mais disponível. Escolha outro.")
    end = (datetime.combine(day, start) + timedelta(minutes=service.duration)).time()
    return Appointment.objects.create(client=client, professional=service.professional, service=service,
                                      date=day, start=start, end=end)
