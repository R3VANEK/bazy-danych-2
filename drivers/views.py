from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import (
    DriverLoginForm,
    DriverRegistrationForm,
)
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import get_vehicles
import json
from .models import Vehicle
from clients.utils import get_rides
from rides.models import Ride


def __validate_driver(request):
    if not getattr(request.user, "driver", None):
        return JsonResponse({"type": "error", "text": "You aren't a driver"})


def driver_login(request):
    is_error = False
    if request.method == "POST":
        form = DriverLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            client = authenticate(request, username=username, password=password)
            if client is not None:
                login(request, client)
                return redirect("driver_home")
        is_error = True
    else:
        form = DriverLoginForm()

    return render(request, "drivers/login.html", {"form": form, "is_error": is_error})


def driver_vehicles_manage(request):

    if not request.user.is_authenticated or not getattr(request.user, "driver", None):
        return reverse_lazy("client_home")

    vehicle_list = get_vehicles(driver=request.user.driver)

    my_rides_requests = get_rides(request.user)

    return render(
        request,
        "drivers/vehicles.html",
        {
            "vehicles": list(vehicle_list),
            "my_ride_requests": list(my_rides_requests),
            "delete_vehicle_url": f"{request.build_absolute_uri()}delete",
            "get_vehicles_url": f"{request.build_absolute_uri()}get",
            "edit_vehicle_url": f"{request.build_absolute_uri()}edit",
            "get_vehicle_url": f"{request.build_absolute_uri()}get/single",
            "add_vehicle_url": f"{request.build_absolute_uri()}add",
            "get_rides_url": f"{request.scheme}://{request.get_host()}/drivers/rides/get",
            "accept_ride_url": f"{request.scheme}://{request.get_host()}/drivers/rides/accept",
        },
    )


def driver_courses_manage(request):
    return render(
        request,
        "drivers/vehicles.html",
    )


def driver_rides_manage(request):
    return render(
        request,
        "drivers/vehicles.html",
    )


@csrf_exempt
def get_rides_endpoint(request):
    __validate_driver(request)

    return JsonResponse(list(get_rides(request.user).values()), safe=False)


@csrf_exempt
def accept_ride_endpoint(request):
    __validate_driver(request)

    driver = request.user.driver

    body = json.loads(request.body)
    ride_id = int(body.get("id"))

    try:
        ride = Ride.objects.prefetch_related("course", "course__vehicle").get(
            id=ride_id
        )
    except Ride.DoesNotExist:
        return JsonResponse(
            {
                "type": "error",
                "text": "This ride doesn't exist",
            },
            safe=False,
        )

    if not ride.course.vehicle.driver_id == driver.id:
        return JsonResponse(
            {
                "type": "error",
                "text": "This ride isn't yours",
            },
            safe=False,
        )

    ride.is_accepted = True
    ride.save()

    return JsonResponse(
        {
            "type": "success",
            "text": "accepted ride!",
        },
        safe=False,
    )


@csrf_exempt
def get_vehicles_endpoint(request):
    if not getattr(request.user, "driver", None):
        return JsonResponse(
            {"type": "error", "text": "You aren't a driver and cannot manage vehicles!"}
        )

    vehicle_list = get_vehicles(driver=request.user.driver)

    return JsonResponse(list(vehicle_list.values()), safe=False)


@csrf_exempt
def get_vehicle_endpoint(request):
    if not getattr(request.user, "driver", None):
        return JsonResponse(
            {"type": "error", "text": "You aren't a driver and cannot manage vehicles!"}
        )

    body = json.loads(request.body)
    vehicle_list = get_vehicles(
        driver=request.user.driver, vehicle_id=int(body.get("id"))
    )

    return JsonResponse(list(vehicle_list.values()), safe=False)


@csrf_exempt
def edit_vehicle_endpoint(request):

    if not getattr(request.user, "driver", None):
        return JsonResponse(
            {"type": "error", "text": "You aren't a driver and cannot manage vehicles!"}
        )

    body = json.loads(request.body)
    driver_id = request.user.driver.id
    vehicle_id = int(body.get("id"))
    name = body.get("name")
    max_passengers = int(body.get("maxPassengers"))

    try:
        vehicle = Vehicle.objects.get(id=vehicle_id, driver_id=driver_id)
    except Vehicle.DoesNotExist:
        return JsonResponse(
            {
                "type": "error",
                "text": "Such vehicle does not exists!",
            },
            safe=False,
        )

    vehicle.name = name
    vehicle.max_passengers = max_passengers
    vehicle.save()

    return JsonResponse(
        {"type": "success", "text": "Edited given vehicle!"}, safe=False
    )


@csrf_exempt
def add_vehicle_ednpoint(request):

    if not getattr(request.user, "driver", None):
        return JsonResponse(
            {"type": "error", "text": "You aren't a driver and cannot manage vehicles!"}
        )

    body = json.loads(request.body)
    driver_id = request.user.driver.id
    name = body.get("name")
    max_passengers = int(body.get("maxPassengers"))
    registration_number = body.get("registrationNumber")

    try:
        _, created = Vehicle.objects.get_or_create(
            driver_id=driver_id,
            name=name,
            max_passengers=max_passengers,
            registration_number=registration_number,
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
        text = "The same vehicle already exists!"
    else:
        type = "success"
        text = "Successfully created new vehicle!"

    return JsonResponse(
        {
            "type": type,
            "text": text,
        },
        safe=False,
    )


@csrf_exempt
def delete_vehicle_endpoint(request):

    if not getattr(request.user, "driver", None):
        return JsonResponse(
            {"type": "error", "text": "You aren't a driver and cannot manage vehicles!"}
        )

    body = json.loads(request.body)
    driver_id = request.user.driver.id
    vehicle_id = int(body.get("id"))

    try:
        deleted, _ = Vehicle.objects.get(id=vehicle_id, driver_id=driver_id).delete()
    except Vehicle.DoesNotExist:
        return JsonResponse(
            {
                "type": "error",
                "text": "Such vehicle does not exists!",
            },
            safe=False,
        )
    return JsonResponse(
        {
            "type": "success",
            "text": "Deleted vehicle!",
        },
        safe=False,
    )


class DriverRegistrationView(CreateView):
    template_name = "drivers/register.html"
    form_class = DriverRegistrationForm
    success_url = reverse_lazy("driver_home")
