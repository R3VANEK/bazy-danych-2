from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import (
    ClientLoginForm,
    ClientRegistrationForm,
)
from django.http import HttpResponse, JsonResponse
from planets.models import Planet
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from datetime import datetime
from django.db.models import F
from rides.models import Ride
from .utils import get_courses, get_rides


def __validate_client(request):
    if not getattr(request.user, "client", None):
        return JsonResponse({"type": "error", "text": "You aren't a client"})


def client_login(request):
    is_error = False
    if request.method == "POST":
        form = ClientLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            client = authenticate(request, username=username, password=password)
            if client is not None:
                login(request, client)
                return redirect("client_home")
        is_error = True
    else:
        form = ClientLoginForm()

    return render(request, "clients/login.html", {"form": form, "is_error": is_error})


def client_home(request):

    if not request.user.is_authenticated or not getattr(request.user, "client", None):
        return reverse_lazy("driver_home")

    all_courses = get_courses(client=request.user.client)

    my_rides = get_rides(request.user)
    return render(
        request,
        "clients/main.html",
        {
            "get_courses_url": f"{request.build_absolute_uri()}courses",
            "get_rides_url": f"{request.build_absolute_uri()}rides",
            "book_ride_url": f"{request.build_absolute_uri()}ride/book",
            "delete_ride_url": f"{request.build_absolute_uri()}ride/delete",
            "pay_ride_url": f"{request.build_absolute_uri()}ride/pay",
            "planets": list(Planet.objects.all().distinct().values()),
            "courses": list(all_courses),
            "my_rides": list(my_rides),
        },
    )


@csrf_exempt
def pay_ride_endpoint(request):
    __validate_client(request)

    client = request.user.client
    body = json.loads(request.body)
    ride_id = int(body.get("id"))

    try:
        ride = Ride.objects.get(id=ride_id)
    except Ride.DoesNotExist:
        return JsonResponse(
            {
                "type": "error",
                "text": "This ride doesn't exist",
            },
            safe=False,
        )

    if not ride.client == client:
        return JsonResponse(
            {
                "type": "error",
                "text": "This ride isn't yours",
            },
            safe=False,
        )

    ride.is_paid = True
    ride.save()

    return JsonResponse(
        {
            "type": "success",
            "text": "paid for the ride!",
        },
        safe=False,
    )


@csrf_exempt
def get_rides_endpoint(request):
    __validate_client(request)

    return JsonResponse(list(get_rides(request.user).values()), safe=False)


@csrf_exempt
def delete_ride_endpoint(request):

    __validate_client(request)

    client = request.user.client

    body = json.loads(request.body)
    ride_id = int(body.get("id"))

    try:
        ride = Ride.objects.get(id=ride_id)
    except Ride.DoesNotExist:
        return JsonResponse(
            {
                "type": "error",
                "text": "This ride doesn't exist",
            },
            safe=False,
        )

    if not ride.client == client:
        return JsonResponse(
            {
                "type": "error",
                "text": "This ride isn't yours",
            },
            safe=False,
        )

    ride.delete()

    return JsonResponse(
        {
            "type": "success",
            "text": "deleted ride!",
        },
        safe=False,
    )


@csrf_exempt
def book_ride_endpoint(request):

    __validate_client(request)

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

    __validate_client(request)

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


class ClientRegistrationView(CreateView):
    template_name = "clients/register.html"
    form_class = ClientRegistrationForm
    success_url = reverse_lazy("client_home")
