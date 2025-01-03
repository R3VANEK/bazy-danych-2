from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
   path("", login_required(views.driver_home), name="driver_home"),
   path("login/", views.driver_login, name="driver_login"),
   path("register/", views.DriverRegistrationView.as_view(), name="driver_register"),
]
