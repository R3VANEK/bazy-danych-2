from .models import Driver, Vehicle, Course, Planet
from django.db.models import QuerySet
from typing import Optional
from django.db.models import Count, F

def get_vehicles(driver: Driver, vehicle_id: Optional[int] = None) -> QuerySet[Vehicle]:
    base_vehicle_query = Vehicle.objects.prefetch_related("driver").filter(driver_id=driver.id).order_by("name")
    if vehicle_id:
        return base_vehicle_query.filter(id=vehicle_id)
    return base_vehicle_query

def get_courses(driver: Driver, course_id: Optional[int] = None) -> QuerySet[Course]:
    base_course_query = (
        Course.objects
        .select_related("vehicle")
        .prefetch_related("rides", "rides__client")
        .annotate(taken_seats=Count("rides"))
        .annotate(max_seats=F("vehicle__max_passengers"))
        .filter(vehicle__driver_id=driver.id)
        .order_by("destination")
    )
    if course_id:
        return base_course_query.filter(id=course_id)
    return base_course_query

def get_planets(planet_id: Optional[int] = None) -> QuerySet[Planet]:
    base_planet_query = Planet.objects.all().order_by("name")
    if planet_id:
        return base_planet_query.filter(id=planet_id)
    return base_planet_query

