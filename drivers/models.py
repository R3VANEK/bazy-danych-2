from django.db import models
from django.contrib.auth.models import User
from planets.models import Planet
from datetime import datetime


# Create your models here.
class Driver(models.Model):
    class Meta:
        db_table = "drivers"
        verbose_name = "driver"
        verbose_name_plural = "drivers"
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    license_expiration = models.DateTimeField()
    work_start = models.DateTimeField(default=datetime.now)
    gender = models.BooleanField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} | {self.work_start} | {self.gender}"


class Course(models.Model):

    class Meta:
        db_table = "courses"
        verbose_name = "course"
        verbose_name_plural = "courses"

    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="courses")
    destination = models.ForeignKey(Planet, on_delete=models.CASCADE, related_name="+")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField(default=datetime.now)

    # represents number of hours
    duration = models.PositiveIntegerField()

    def __str__(self):
        return f"course of {self.driver} to {self.destination} | price: {self.price} | start: {self.start_date} | price: {self.price}"


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
