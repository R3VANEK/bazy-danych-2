from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class ClientManager(BaseUserManager):
    def create_user(self, email, phone_number, first_name, last_name, password=None):
        if not email:
            raise ValueError("The Email field must be set")
        user = self.model(
            email=email,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, phone_number, first_name, last_name, password=None
    ):
        user = self.create_user(
            email=email,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


# class User(AbstractBaseUser):
#     email = models.EmailField(unique=True)
#     phone_number = models.CharField(max_length=12)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=200)
#     created_at = models.DateTimeField(default=datetime.now)
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#
#     objects = ClientManager()
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name']
#
#     def __str__(self):
#         return self.email
#
#     def has_perm(self, perm, obj=None):
#         return True
#
#     def has_module_perms(self, app_label):
#         return True
#
#     def is_staff(self):
#         return self.is_admin
#
#     @property
#     def full_name(self):
#         return f"{self.first_name} {self.last_name}"


class Client(models.Model):
    class Meta:
        db_table = "clients"
        verbose_name = "client"
        verbose_name_plural = "clients"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12)
