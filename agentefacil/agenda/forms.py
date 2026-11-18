from datetime import timedelta
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils import timezone
from .models import Availability, Service, User


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={"autocomplete": "username"}))
    error_messages = {
        "invalid_login": "Não foi possível entrar. Confira o e-mail e a senha.",
        "inactive": "Não foi possível entrar. Confira o e-mail e a senha.",
    }

    def clean_username(self):
        return self.cleaned_data["username"].lower()


class SignupForm(UserCreationForm):
    first_name = forms.CharField(label="Nome", max_length=150)

    class Meta:
        model = User
        fields = ["first_name", "email", "role"]

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()


class SearchForm(forms.Form):
    service = forms.ModelChoiceField(label="Serviço e profissional", queryset=Service.objects.none(),
                                    empty_label="Selecione um serviço")
    date = forms.DateField(label="Data do atendimento", widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = timezone.localdate()
        self.fields["date"].widget.attrs.update(min=today.isoformat(), max=(today + timedelta(days=90)).isoformat())
        self.fields["service"].queryset = Service.objects.filter(
            active=True, professional__is_active=True, professional__role=User.Role.PRO
        ).select_related("professional")

    def clean_date(self):
        day = self.cleaned_data["date"]
        today = timezone.localdate()
        if not today <= day <= today + timedelta(days=90):
            raise forms.ValidationError("Escolha uma data entre hoje e os próximos 90 dias.")
        return day


class ServiceForm(forms.ModelForm):
    duration = forms.IntegerField(label="Duração em minutos", min_value=1, max_value=480)
    price = forms.DecimalField(label="Preço (R$)", min_value=0, max_digits=8, decimal_places=2, localize=True)

    class Meta:
        model = Service
        fields = ["name", "duration", "price"]


class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ["weekday", "start", "end"]
        widgets = {"start": forms.TimeInput(attrs={"type": "time"}), "end": forms.TimeInput(attrs={"type": "time"})}

    def clean(self):
        data = super().clean()
        if data.get("start") and data.get("end") and data["end"] <= data["start"]:
            self.add_error("end", "O fim deve ser posterior ao início.")
        return data
