from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path("vehicles/", login_required(views.driver_vehicles_manage), name="driver_home"),
    path("vehicles/delete", views.delete_vehicle_endpoint, name="vehicle_delete"),
    path("vehicles/get", views.get_vehicles_endpoint, name="vehicle_get"),
    path(
        "courses/", login_required(views.driver_courses_manage), name="driver_courses"
    ),
    path("rides/", login_required(views.driver_rides_manage), name="driver_rides"),
    path("login/", views.driver_login, name="driver_login"),
    path("register/", views.DriverRegistrationView.as_view(), name="driver_register"),
]
