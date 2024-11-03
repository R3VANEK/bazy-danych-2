from django.db import models
from planets.models import Planet
from clients.models import Client
from drivers.models import Driver, Course, Vehicle
from datetime import datetime

# Create your models here.


class Ride(models.Model):

    class Meta:
        db_table = "rides"
        verbose_name = "ride"
        verbose_name_plural = "rides"

    course = models.ForeignKey(
        to=Course, on_delete=models.SET_NULL, related_name="rides", null=True
    )
    vehicle = models.ForeignKey(
        to=Vehicle, on_delete=models.SET_NULL, related_name="rides", null=True
    )
    client = models.ForeignKey(
        to=Client, on_delete=models.SET_NULL, related_name="rides", null=True
    )
    departure = models.ForeignKey(
        to=Planet, on_delete=models.SET_NULL, related_name="rides", null=True
    )
    grade = models.PositiveSmallIntegerField()
    start_date = models.DateTimeField(default=datetime.now)
    end_date = models.DateTimeField()
    is_paid = models.BooleanField(default=False)
