from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import IntegrityError, OperationalError, transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from .booking import reserve, slots
from .forms import AvailabilityForm, LoginForm, SearchForm, ServiceForm, SignupForm
from .models import Appointment, User


class Home(LoginView):
    template_name = "agenda/home.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


@require_http_methods(["GET", "POST"])
def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = SignupForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                user = form.save()
        except IntegrityError:
            form.add_error("email", "Não foi possível cadastrar esse e-mail.")
        else:
            login(request, user)
            return redirect("dashboard")
    return render(request, "agenda/signup.html", {"form": form})


@login_required
def dashboard(request):
    return redirect("professional" if request.user.role == User.Role.PRO else "booking")


@login_required
@require_http_methods(["GET", "POST"])
def booking(request):
    if request.user.role != User.Role.CLIENT:
        raise PermissionDenied
    is_post = request.method == "POST"
    data = request.POST if is_post else (request.GET or None)
    search = SearchForm(data)
    service, day, times, error = None, None, [], None
    if search.is_valid():
        service, day = search.cleaned_data["service"], search.cleaned_data["date"]
        if is_post:
            from django.forms import TimeField
            try:
                start = TimeField().clean(request.POST.get("start"))
                result = reserve(request.user, service.pk, day, start)
            except ValidationError:
                error = "Selecione um horário disponível. Se ele acabou de ser reservado, escolha outro."
            except IntegrityError:
                error = "O horário acabou de ser reservado. Escolha outro."
            except OperationalError as exc:
                if "locked" not in str(exc).lower():
                    raise
                error = "Não foi possível confirmar agora. Confira os horários e tente de novo."
            else:
                return redirect("confirmation", pk=result.pk)
        times = slots(service, day)
    context = {"search": search, "service": service, "day": day, "times": times, "error": error}
    return render(request, "agenda/booking.html", context, status=409 if error else 200)


@login_required
def confirmation(request, pk):
    appointment = get_object_or_404(
        Appointment.objects.select_related("professional", "service"), pk=pk, client=request.user
    )
    return render(request, "agenda/confirmation.html", {"appointment": appointment})


@login_required
def history(request):
    if request.user.role != User.Role.CLIENT:
        raise PermissionDenied
    records = request.user.bookings.select_related("service", "professional")
    return render(request, "agenda/history.html", {"records": records})


@login_required
@require_http_methods(["GET", "POST"])
def professional(request):
    user = request.user
    if user.role != User.Role.PRO:
        raise PermissionDenied
    action = request.POST.get("action")
    service_form = ServiceForm(request.POST if action == "service" else None, prefix="service")
    hours_form = AvailabilityForm(request.POST if action == "hours" else None, prefix="hours")
    if action == "service" and service_form.is_valid():
        item = service_form.save(commit=False)
        item.professional = user
        item.save()
        messages.success(request, "Serviço cadastrado.")
        return redirect("professional")
    if action == "hours" and hours_form.is_valid():
        item = hours_form.save(commit=False)
        with transaction.atomic():
            if user.availability.filter(weekday=item.weekday, active=True, start__lt=item.end, end__gt=item.start).exists():
                hours_form.add_error("start", "Esse período sobrepõe um horário já cadastrado.")
            else:
                item.professional = user
                item.save()
                messages.success(request, "Disponibilidade cadastrada.")
                return redirect("professional")
    return render(request, "agenda/professional.html", {
        "service_form": service_form, "hours_form": hours_form,
        "services": user.services.all(), "periods": user.availability.all(),
        "records": user.appointments.select_related("service", "client"),
    })
