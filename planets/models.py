from django.db import models


# Create your models here.
class Planet(models.Model):
    class Meta:
        db_table = "planets"
        verbose_name = "planet"
        verbose_name_plural = "planets"

    name = models.TextField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name}"
