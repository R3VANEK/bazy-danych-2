from django.db import models
from clients.models import User
from planets.models import Planet
from datetime import datetime


# Create your models here.
class Driver(User):
    class Meta:
        db_table = "drivers"
        verbose_name = "driver"
        verbose_name_plural = "drivers"

    license_expiration = models.DateTimeField()
    work_start = models.DateTimeField(default=datetime.now)
    gender = models.BooleanField()


class Course(models.Model):

    class Meta:
        db_table = "courses"
        verbose_name = "course"
        verbose_name_plural = "courses"

    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="courses")
    destination = models.ForeignKey(Planet, on_delete=models.CASCADE, related_name="+")
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Vehicle(models.Model):
    class Meta:
        db_table = "vehicles"
        verbose_name = "vehicle"
        verbose_name_plural = "vehicles"

    driver = models.ForeignKey(
        Driver, on_delete=models.CASCADE, related_name="vehicles"
    )
    name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=50, unique=True)
    max_passengers = models.PositiveIntegerField()
