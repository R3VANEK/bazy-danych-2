
from django.urls import path
from .views import (
    driver_login,
    DriverRegistrationView,
    driver_vehicles_manage,
    get_vehicles_endpoint,
    get_vehicle_endpoint,
    edit_vehicle_endpoint,
    add_vehicle_endpoint,
    delete_vehicle_endpoint,
    driver_courses_manage,
    driver_rides_manage,
)

urlpatterns = [
    path('login/', driver_login, name='driver_login'),
    path('register/', DriverRegistrationView.as_view(), name='driver_register'),
    path('vehicles/', driver_vehicles_manage, name='driver_vehicles_manage'),
    path('vehicles/get/', get_vehicles_endpoint, name='get_vehicles'),
    path('vehicles/get/single/', get_vehicle_endpoint, name='get_vehicle'),
    path('vehicles/edit/', edit_vehicle_endpoint, name='edit_vehicle'),
    path('vehicles/add/', add_vehicle_endpoint, name='add_vehicle'),
    path('vehicles/delete/', delete_vehicle_endpoint, name='delete_vehicle'),
    path('courses/', driver_courses_manage, name='driver_courses_manage'),
    path('rides/', driver_rides_manage, name='driver_rides_manage'),
]
