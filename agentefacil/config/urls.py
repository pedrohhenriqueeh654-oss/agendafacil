from django.contrib.auth.views import LogoutView
from django.urls import path
from agenda import views

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("cadastro/", views.signup, name="signup"),
    path("sair/", LogoutView.as_view(), name="logout"),
    path("painel/", views.dashboard, name="dashboard"),
    path("agendar/", views.booking, name="booking"),
    path("reserva/<int:pk>/", views.confirmation, name="confirmation"),
    path("minhas-reservas/", views.history, name="history"),
    path("profissional/", views.professional, name="professional"),
]
