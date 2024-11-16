from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="client_home"),
    path("login/", views.client_login, name="client_login"),
    path("home/", views.client_home, name="client_home"),
]
