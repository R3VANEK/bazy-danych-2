from typing import Optional
from datetime import datetime, time
from drivers.models import Course
from rides.models import Ride
from django.db.models import Subquery, OuterRef, Avg, F, QuerySet, Count, Q, Value
from django.db.models.functions import Concat
from django.utils import timezone


def get_courses(
    destination_id: Optional[int] = None,
    driver_grade: Optional[int] = None,
    max_price: Optional[float] = None,
    time_for_departure: Optional[str] = None,
    driver_is_male: Optional[bool] = None,
) -> QuerySet[Course]:

    # Use timezone.now() to ensure it's timezone-aware
    now = timezone.now()

    base_courses = (
        Course.objects.prefetch_related(
            "vehicle", "vehicle__driver", "vehicle__driver__user"
        )
        .select_related("destination")
        .annotate(destination_name=F("destination__name"))
        .annotate(
            driver_name=Concat(
                F("vehicle__driver__user__first_name"),
                Value(" "),
                F("vehicle__driver__user__last_name"),
            )
        )
        .annotate(
            driver_grade=Subquery(
                Ride.objects.filter(
                    course__vehicle__driver_id=OuterRef("vehicle__driver_id")
                )
                .values("course__vehicle__driver_id")
                .annotate(avg_grade=Avg("grade"))
                .values("avg_grade")[:1]
            )
        )
        .annotate(taken_seats=Count("rides"))
        .annotate(max_seats=F("vehicle__max_passengers"))
        .filter(start_date__gt=now, taken_seats__lt=F("max_seats"))
        .order_by("start_date")
    )

    extra_filters = Q()

    # Apply filters dynamically
    if destination_id:
        extra_filters &= Q(destination_id=destination_id)

    if driver_grade:
        extra_filters &= Q(driver_grade__gte=driver_grade)

    if max_price:
        extra_filters &= Q(price__lte=max_price)

    if time_for_departure:
        parsed_departure_time = datetime.strptime(time_for_departure, "%d/%m/%Y")
        parsed_departure_time = timezone.make_aware(parsed_departure_time, timezone.utc)

        # start_of_day = timezone.make_aware(
        #     datetime.combine(parsed_departure_time, time.min), timezone=timezone.utc
        # )
        end_of_day = timezone.make_aware(
            datetime.combine(parsed_departure_time, time.max), timezone=timezone.utc
        )

        extra_filters &= Q(start_date__lte=end_of_day)

    if driver_is_male:
        extra_filters &= Q(vehicle__driver__is_male=bool(driver_is_male))

    # Apply extra filters to the queryset
    return base_courses.filter(extra_filters)