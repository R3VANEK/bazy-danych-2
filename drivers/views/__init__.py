from .authentication_views import driver_login, DriverRegistrationView
from .vehicles_views import (
    driver_vehicles_manage,
    get_vehicles_endpoint,
    get_vehicle_endpoint,
    edit_vehicle_endpoint,
    add_vehicle_endpoint,
    delete_vehicle_endpoint,
)
from .courses_views import driver_courses_manage
from .rides_views import driver_rides_manage