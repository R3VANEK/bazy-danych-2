from .models import Driver, Vehicle, Course
from django.db.models import QuerySet
from typing import Optional


def get_vehicles(driver: Driver, vehicle_id: Optional[int] = None) -> QuerySet[Vehicle]:

    base_vehicle_query = (
        Vehicle.objects.prefetch_related("driver")
        .filter(driver_id=driver.id)
        .order_by("name")
    )    
    print(base_vehicle_query) 
    if vehicle_id:
        return base_vehicle_query.filter(id=vehicle_id)

    return base_vehicle_query

def get_courses(driver: Driver, course_id: Optional[int] = None) -> QuerySet[Course]:
    base_course_query = (
        Course.objects.prefetch_related("vehicle")
        .order_by("destination")
    )

    if course_id:
        return base_course_query.filter(id=course_id)

    return base_course_query