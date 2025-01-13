from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .forms import (
    DriverLoginForm,
    DriverRegistrationForm,
)
from .utils import get_vehicles, get_courses
from .models import Vehicle, Course

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
        return redirect("client_home")
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
    if not request.user.is_authenticated or not getattr(request.user, "driver", None):
        return redirect("client_home")
    course_list = get_courses(driver=request.user.driver)
    vehicle_list = get_vehicles(driver=request.user.driver)
    return render(
        request,
        "drivers/courses.html",
        {
            "courses": list(course_list),
            "vehicles": list(vehicle_list),
            "delete_course_url": f"{request.build_absolute_uri()}delete",
            "get_courses_url": f"{request.build_absolute_uri()}get",
            "get_vehicles_url": reverse("vehicle_get"),
            "edit_course_url": f"{request.build_absolute_uri()}edit",
            "get_course_url": f"{request.build_absolute_uri()}get/single",
            "add_course_url": f"{request.build_absolute_uri()}add",
        },
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
        ride = Ride.objects.prefetch_related("course", "course__vehicle").get(id=ride_id)
    except Ride.DoesNotExist:
        return JsonResponse({"type": "error", "text": "This ride doesn't exist"}, safe=False)
    if not ride.course.vehicle.driver.id == driver.id:
        return JsonResponse({"type": "error", "text": "This ride isn't yours"}, safe=False)
    ride.is_accepted = True
    ride.save()
    return JsonResponse({"type": "success", "text": "accepted ride!"}, safe=False)

@csrf_exempt
def get_vehicles_endpoint(request):
    if not getattr(request.user, "driver", None):
        return JsonResponse({"type": "error", "text": "You aren't a driver and cannot manage vehicles!"})
    vehicle_list = get_vehicles(driver=request.user.driver)
    return JsonResponse(list(vehicle_list.values()), safe=False)

@csrf_exempt
def get_vehicle_endpoint(request):
    if not getattr(request.user, "driver", None):
        return JsonResponse({"type": "error", "text": "You aren't a driver and cannot manage vehicles!"})
    body = json.loads(request.body)
    vehicle_list = get_vehicles(driver=request.user.driver, vehicle_id=int(body.get("id")))
    return JsonResponse(list(vehicle_list.values()), safe=False)

@csrf_exempt
def edit_vehicle_endpoint(request):
    if not getattr(request.user, "driver", None):
        return JsonResponse({"type": "error", "text": "You aren't a driver and cannot manage vehicles!"})
    body = json.loads(request.body)
    driver_id = request.user.driver.id
    vehicle_id = int(body.get("id"))
    name = body.get("name")
    max_passengers = int(body.get("maxPassengers"))
    try:
        vehicle = Vehicle.objects.get(id=vehicle_id, driver_id=driver_id)
    except Vehicle.DoesNotExist:
        return JsonResponse({"type": "error", "text": "Such vehicle does not exist!"}, safe=False)
    vehicle.name = name
    vehicle.max_passengers = max_passengers
    vehicle.save()
    return JsonResponse({"type": "success", "text": "Edited given vehicle!"}, safe=False)

@csrf_exempt
def add_vehicle_ednpoint(request):
    if not getattr(request.user, "driver", None):
        return JsonResponse({"type": "error", "text": "You aren't a driver and cannot manage vehicles!"})
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
        return JsonResponse({"type": "error", "text": "Some unexpected error occurred, please try again"}, safe=False)
    if not created:
        return JsonResponse({"type": "error", "text": "The same vehicle already exists!"}, safe=False)
    return JsonResponse({"type": "success", "text": "Successfully created new vehicle!"}, safe=False)

@csrf_exempt
def delete_vehicle_endpoint(request):
    if not getattr(request.user, "driver", None):
        return JsonResponse({"type": "error", "text": "You aren't a driver and cannot manage vehicles!"})
    body = json.loads(request.body)
    driver_id = request.user.driver.id
    vehicle_id = int(body.get("id"))
    try:
        deleted, _ = Vehicle.objects.get(id=vehicle_id, driver_id=driver_id).delete()
    except Vehicle.DoesNotExist:
        return JsonResponse({"type": "error", "text": "Such vehicle does not exist!"}, safe=False)
    return JsonResponse({"type": "success", "text": "Deleted vehicle!"}, safe=False)

@csrf_exempt
def delete_course_endpoint(request):
    if not getattr(request.user, "driver", None):
        return JsonResponse({"type": "error", "text": "You aren't a driver and cannot manage courses!"})
    body = json.loads(request.body)
    course_id = int(body.get("id"))
    try:
        Course.objects.get(id=course_id, vehicle__driver=request.user.driver).delete()
    except Course.DoesNotExist:
        return JsonResponse({"type": "error", "text": "Such course does not exist!"}, safe=False)
    return JsonResponse({"type": "success", "text": "Course deleted successfully!"}, safe=False)

@csrf_exempt
def get_courses_endpoint(request):
    if not getattr(request.user, "driver", None):
        return JsonResponse({"type": "error", "text": "You aren't a driver and cannot manage courses!"})
    course_list = get_courses(driver=request.user.driver)
    return JsonResponse(list(course_list.values()), safe=False)

@csrf_exempt
def get_course_endpoint(request):
    if not getattr(request.user, "driver", None):
        return JsonResponse({"type": "error", "text": "You aren't a driver and cannot manage courses!"})
    body = json.loads(request.body)
    course_id = body.get("id")
    if course_id is None:
        return JsonResponse({"type": "error", "text": "Course ID is required!"})
    course_list = get_courses(driver=request.user.driver, course_id=int(course_id))
    return JsonResponse(list(course_list.values()), safe=False)

@csrf_exempt
def edit_course_endpoint(request):
    if not getattr(request.user, "driver", None):
        return JsonResponse({"type": "error", "text": "You aren't a driver and cannot manage courses!"})
    body = json.loads(request.body)
    course_id = int(body.get("id"))
    name = body.get("name")
    description = body.get("description")
    try:
        course = Course.objects.get(id=course_id, vehicle__driver=request.user.driver)
    except Course.DoesNotExist:
        return JsonResponse({"type": "error", "text": "Such course does not exist!"}, safe=False)
    course.name = name
    course.description = description
    course.save()
    return JsonResponse({"type": "success", "text": "Course updated successfully!"}, safe=False)

@csrf_exempt
def add_course_endpoint(request):
    if not getattr(request.user, "driver", None):
        return JsonResponse({"type": "error", "text": "You aren't a driver and cannot manage courses!"})
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"type": "error", "text": "Invalid JSON in request body!"}, safe=False)

    destination = body.get("destination")
    duration = body.get("duration")
    vehicle_id = body.get("vehicle")  
    price = body.get("price")
    print(f"Driver: {request.user.driver}")
    print(f"Destination: {destination}")
    print(f"Duration: {duration}")
    print(f"Vehicle: {vehicle_id}")
    print(f"Price: {price}")

    if not all([destination, duration, vehicle_id, price]):
        return JsonResponse({"type": "error", "text": "All fields (destination, duration, vehicle, price) are required!"}, safe=False)
    try:
        vehicle_instance = Vehicle.objects.get(id=vehicle_id, driver=request.user.driver)
    except Vehicle.DoesNotExist:
        return JsonResponse({"type": "error", "text": "Selected vehicle does not exist or does not belong to you."}, safe=False)

    try:
        course, created = Course.objects.get_or_create(
            vehicle=vehicle_instance,
            destination=destination, 
            duration_days=duration, 
            price=price,
        )
    except Exception as e:
        return JsonResponse({"type": "error", "text": f"Some unexpected error occurred: {str(e)}"}, safe=False)

    if not created:
        return JsonResponse({"type": "error", "text": "Course already exists!"}, safe=False)

    return JsonResponse({"type": "success", "text": "Course added successfully!"}, safe=False)

class DriverRegistrationView(CreateView):
    template_name = "drivers/register.html"
    form_class = DriverRegistrationForm
    success_url = reverse_lazy("driver_home")
