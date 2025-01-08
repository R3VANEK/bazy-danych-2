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

@csrf_exempt
def book_ride_endpoint(request):
    body = json.loads(request.body)
    departure_id = int(body.get("departureId"))
    course_id = int(body.get("courseId"))

    try:
        _, created = Ride.objects.get_or_create(
            course_id=course_id,
            departure_id=departure_id,
            client_id=request.user.client.id,
        )
    except Exception:
        return JsonResponse(
            {
                "type": "error",
                "text": "Some unexpected error occured, please try again",
            },
            safe=False,
        )

    if not created:
        type = "error"
        text = "You already booked this ride!"
    else:
        type = "success"
        text = "Successfully booked a ride!"

    return JsonResponse(
        {
            "type": type,
            "text": text,
        },
        safe=False,
    )

@csrf_exempt
def courses_rest_view(request):
    body = json.loads(request.body)
    filtered_courses = get_courses(
        client=request.user.client,
        destination_id=body.get("destination"),
        driver_grade=body.get("grade"),
        max_price=body.get("maxPrice"),
        time_for_departure=body.get("timeForDeparture"),
        driver_is_male=body.get("driverGender"),
    )
    return JsonResponse(list(filtered_courses.values()), safe=False)
