from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path("vehicles/", login_required(views.driver_vehicles_manage), name="driver_home"),
    path("vehicles/delete", views.delete_vehicle_endpoint, name="vehicle_delete"),
    path("vehicles/get", views.get_vehicles_endpoint, name="vehicle_get"),
    path("vehicles/get/single", views.get_vehicle_endpoint, name="vehicle_get_single"),
    path("vehicles/edit", views.edit_vehicle_endpoint, name="vehicles_edit"),
    path("vehicles/add", views.add_vehicle_ednpoint, name="vehicles_add"),
    path("courses/delete", views.delete_course_endpoint, name="course_delete"),
    path("courses/get", views.get_courses_endpoint, name="course_get"),
    path("courses/get/single", views.get_course_endpoint, name="course_get_single"),
    path("courses/edit", views.edit_course_endpoint, name="course_edit"),
    path("courses/add", views.add_course_endpoint, name="course_add"),
    path("courses/", login_required(views.driver_courses_manage), name="driver_courses"),
    path("rides/get", views.get_rides_endpoint, name="driver_rides"),
    path("rides/accept", views.accept_ride_endpoint, name="driver_rides_accept"),
    path("rides/", login_required(views.driver_rides_manage), name="driver_rides"),
    path("login/", views.driver_login, name="driver_login"),
    path("register/", views.DriverRegistrationView.as_view(), name="driver_register"),
    path('get_vehicles/', views.get_vehicles, name='get_vehicles'),
]
