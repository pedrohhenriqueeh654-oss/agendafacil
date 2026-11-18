from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models import F, Q


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra):
        if not email:
            raise ValueError("O e-mail é obrigatório.")
        user = self.model(email=email.strip().lower(), **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra):
        return self.create_user(email, password, **{**extra, "is_staff": True, "is_superuser": True})


class User(AbstractUser):
    class Role(models.TextChoices):
        CLIENT = "client", "Cliente"
        PRO = "pro", "Profissional"

    username = None
    email = models.EmailField("e-mail", unique=True)
    role = models.CharField("perfil", max_length=6, choices=Role.choices, default=Role.CLIENT)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.get_full_name() or self.email


class Service(models.Model):
    professional = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="services")
    name = models.CharField("nome", max_length=100)
    duration = models.PositiveSmallIntegerField("duração em minutos")
    price = models.DecimalField("preço (R$)", max_digits=8, decimal_places=2)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name", "professional_id"]
        constraints = [models.CheckConstraint(condition=Q(duration__gt=0, price__gte=0), name="service_valid_values")]

    def __str__(self):
        return f"{self.name} — {self.professional}"


WEEKDAYS = tuple(enumerate(["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira",
                            "Sexta-feira", "Sábado", "Domingo"]))


class Availability(models.Model):
    professional = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="availability")
    weekday = models.PositiveSmallIntegerField("dia da semana", choices=WEEKDAYS)
    start = models.TimeField("início")
    end = models.TimeField("fim")
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["weekday", "start"]
        constraints = [models.CheckConstraint(condition=Q(weekday__lte=6, end__gt=F("start")), name="availability_valid_period")]


class Appointment(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = "confirmed", "Confirmado"
        CANCELED = "canceled", "Cancelado"

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="bookings")
    professional = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="appointments")
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.CONFIRMED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date", "start"]
        indexes = [models.Index(fields=["professional", "date", "status"])]
        constraints = [
            models.CheckConstraint(condition=Q(end__gt=F("start")), name="appointment_valid_period"),
            models.UniqueConstraint(fields=["professional", "date", "start"], condition=Q(status="confirmed"),
                                    name="unique_confirmed_start"),
        ]
