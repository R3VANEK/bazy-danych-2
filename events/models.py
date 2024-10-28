from django.db import models
from datetime import datetime
from client.models import Patient

# Create your models here.


class Event(models.Model):

    start = models.DateTimeField(default=datetime.now)
    place = models.TextField()
    end = models.DateTimeField(default=datetime.now)
    room = models.TextField(default="room 1")
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, null=True, blank=True, related_name="events"
    )

