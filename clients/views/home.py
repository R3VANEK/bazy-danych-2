from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from planets.models import Planet
from rides.models import Ride
from ..utils import get_courses
import json

def client_home(request):
    if not request.user.is_authenticated or not getattr(request.user, "client", None):
        return redirect("driver_home")

    all_courses = get_courses(client=request.user.client)
    my_rides = (
        Ride.objects.select_related("departure")
        .prefetch_related("course")
        .annotate(destination_name=F("course__destination__name"))
        .annotate(departure_name=F("departure__name"))
        .filter(client_id=request.user.client.id)
    )
    return render(
        request,
        "clients/main.html",
        {
            "get_courses_url": f"{request.build_absolute_uri()}courses",
            "book_ride_url": f"{request.build_absolute_uri()}ride/book",
            "planets": list(Planet.objects.all().distinct().values()),
            "courses": list(all_courses),
            "my_rides": list(my_rides),
        },
    )