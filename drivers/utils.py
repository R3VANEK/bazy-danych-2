from .models import Driver, Vehicle
from django.db.models import QuerySet


def get_vehicles(driver: Driver) -> QuerySet[Vehicle]:
    return (
        Vehicle.objects.prefetch_related("driver")
        .filter(driver_id=driver.id)
        .order_by("name")
    )
