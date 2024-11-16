from django.db import models
from datetime import datetime

# Create your models here.


class User(models.Model):

    class Meta:
        abstract = True
        db_table = "users"
        verbose_name = "user"
        verbose_name_plural = "users"

    email = models.EmailField()
    phone_number = models.CharField(max_length=12)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=datetime.now)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Client(User):

    class Meta:
        db_table = "clients"
        verbose_name = "client"
        verbose_name_plural = "clients"
