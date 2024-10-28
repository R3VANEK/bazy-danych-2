from django.db import models

class Driver(models.Model):
    name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50)
    experience_years = models.IntegerField()

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration_hours = models.IntegerField()

class Vehicle(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
