from django.db import transaction
from faker import Faker
from clients.models import Client
from drivers.models import Driver
from drivers.models import Vehicle
from drivers.models import Course
from planets.models import Planet
from rides.models import Ride
from datetime import datetime, timedelta
import os
import random
import django


from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = "Populate db with fake data"

    def add_arguments(self, parser):
        parser.add_argument("--clients", nargs="+", type=int)
        parser.add_argument("--drivers", nargs="+", type=int)

    def handle(self, *args, **kwargs):

        with transaction.atomic():

            fake = Faker()

            planet_name_list = [
                "Earth",
                "Pluto",
                "Uran",
                "Neptun",
                "Alpha Centauri",
            ]

            planet_list = []
            courses_list = []
            vehicles_list = []
            clients_list = []

            for planet in planet_name_list:
                planet_list.append(
                    Planet.objects.create(
                        name=planet,
                    )
                )

            for _ in range(kwargs["clients"][0] if kwargs["clients"] else 50):

                clients_list.append(
                    Client.objects.create(
                        email=fake.email(),
                        phone_number=fake.phone_number(),
                        created_at=fake.date_between_dates(
                            datetime.strptime(
                                "2021-02-28 14:30:00", "%Y-%m-%d %H:%M:%S"
                            ),
                            datetime.now(),
                        ),
                        first_name=fake.first_name(),
                        last_name=fake.last_name(),
                    )
                )

            for _ in range(kwargs["drivers"][0] if kwargs["drivers"] else 30):

                driver = Driver.objects.create(
                    email=fake.email(),
                    phone_number=fake.phone_number(),
                    created_at=fake.date_between_dates(
                        datetime.strptime("2021-02-28 14:30:00", "%Y-%m-%d %H:%M:%S"),
                        datetime.now(),
                    ),
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    license_expiration=fake.date_between_dates(
                        datetime.strptime("2030-12-30 14:30:00", "%Y-%m-%d %H:%M:%S"),
                        datetime.strptime("2037-12-30 14:30:00", "%Y-%m-%d %H:%M:%S"),
                    ),
                    work_start=fake.date_between_dates(
                        datetime.strptime("2021-02-28 14:30:00", "%Y-%m-%d %H:%M:%S"),
                        datetime.now(),
                    ),
                    gender=fake.boolean(),
                )

                rand_vehicle_count = random.randint(1, 5)
                for _ in range(rand_vehicle_count):
                    vehicles_list.append(
                        Vehicle.objects.create(
                            driver=driver,
                            name=fake.company(),
                            registration_number=fake.vin(),
                            max_passengers=fake.random_int(min=5, max=100),
                        )
                    )

                rand_courses_count = random.randint(1, 10)

                for _ in range(rand_courses_count):
                    courses_list.append(
                        Course.objects.create(
                            driver=driver,
                            destination=planet_list[
                                random.randint(0, len(planet_list) - 1)
                            ],
                            price=fake.pydecimal(min_value=100.0, max_value=1500.0),
                            start_date=fake.date_between_dates(
                                datetime.now(),
                                datetime.strptime(
                                    "2025-02-28 14:30:00", "%Y-%m-%d %H:%M:%S"
                                ),
                            ),
                            duration=fake.random_int(min=5, max=100),
                        )
                    )

            for _ in range(100):

                random_course = courses_list[random.randint(0, len(courses_list) - 1)]

                departure_list = [
                    planet
                    for planet in planet_list
                    if planet != random_course.destination
                ]
                Ride(
                    course=random_course,
                    vehicle=vehicles_list[random.randint(0, len(vehicles_list) - 1)],
                    client=clients_list[random.randint(0, len(clients_list) - 1)],
                    departure=departure_list[
                        random.randint(0, len(departure_list) - 1)
                    ],
                    grade=random.randint(0, 10),
                    is_paid=fake.boolean(),
                ).save()
