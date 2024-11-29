from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.client_login, name="client_login"),
    path("home/", views.client_home, name="client_home"),
    path("register/", views.ClientRegistrationView.as_view(), name="client_register"),
]
