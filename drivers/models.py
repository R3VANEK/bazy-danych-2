from django.db import models

class Driver(models.Model):
    user_id = models.IntegerField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    license_expiration = models.DateTimeField()
    work_start = models.DateTimeField()
    gender = models.BooleanField()

class Course(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    destination_id = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Vehicle(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=50, unique=True)
    max_passengers = models.IntegerField()
