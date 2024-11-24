from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),  # Strona główna aplikacji
    path("login/", views.client_login, name="client_login"),  # Logowanie klienta
    path("home/", views.client_home, name="client_home"),  # Strona sukcesu po zalogowaniu
    path("register/", views.ClientRegistrationView.as_view(), name="client_register"),  # Rejestracja klienta
]
