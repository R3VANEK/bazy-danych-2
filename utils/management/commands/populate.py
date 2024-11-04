from faker import Faker
from clients.models import Client
from datetime import datetime
import os
import django


from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = "Populate db with fake data"

    def handle(self, *args, **kwargs):

        fake = Faker()
        for i in range(50):
            Client(
                email=fake.email(),
                phone_number=fake.phone_number(),
                created_at=fake.date_between_dates(
                    datetime.strptime("2021-02-28 14:30:00", "%Y-%m-%d %H:%M:%S"),
                    datetime.now(),
                ),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            ).save()
