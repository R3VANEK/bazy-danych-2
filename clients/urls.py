from django.urls import path
from . import views

urlpatterns = [
    path("", views.client_home, name="client_home"),
    path("login/", views.client_login, name="client_login"),
    path("register/", views.ClientRegistrationView.as_view(), name="client_register"),
    path("courses", views.courses_rest_view),
]
