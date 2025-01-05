from .models import Driver, Vehicle
from django.db.models import QuerySet
from typing import Optional


def get_vehicles(driver: Driver, vehicle_id: Optional[int] = None) -> QuerySet[Vehicle]:

    base_vehicle_query = (
        Vehicle.objects.prefetch_related("driver")
        .filter(driver_id=driver.id)
        .order_by("name")
    )

    if vehicle_id:
        return base_vehicle_query.filter(id=vehicle_id)

    return base_vehicle_query
