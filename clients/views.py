from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import (
    ClientLoginForm,
    ClientRegistrationForm,
)
from django.http import HttpResponse, JsonResponse
from drivers.models import Course
from planets.models import Planet
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from datetime import datetime
from django.db.models import Avg, Count, F, Subquery, OuterRef
from drivers.models import Driver, Vehicle
from rides.models import Ride
from .utils import get_courses


# Widok logowania klienta
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

    all_courses = get_courses()

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
            "planets": list(Planet.objects.all().distinct().values()),
            "courses": list(all_courses),
            "my_rides": list(my_rides),
        },
    )


@csrf_exempt
def courses_rest_view(request):

    body = json.loads(request.body)

    filtered_courses = get_courses(
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
