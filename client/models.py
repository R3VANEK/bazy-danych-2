from django.db import models

# Create your models here.


class Patient(models.Model):

    full_name = models.TextField()
    birthday = models.DateField()
    phone = models.TextField()
    pesel = models.TextField()





