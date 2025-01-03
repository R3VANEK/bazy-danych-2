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

    courses = (
        Course.objects.prefetch_related(
            "vehicle", "vehicle__driver", "vehicle__driver__user"
        )
        .select_related("destination")
        .annotate(destination_name=F("destination__name"))
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
        .filter(start_date__gt=datetime.now(), taken_seats__lt=F("max_seats"))
        .order_by("start_date")
    )

    return render(
        request,
        "clients/main.html",
        {
            "get_courses_url": f"{request.build_absolute_uri()}clients/courses",
            "planets": list(Planet.objects.all().distinct().values()),
            "courses": list(courses),
        },
    )


@csrf_exempt
def courses_rest_view(request):
    # TODO: zabezpiecz
    body = json.loads(request.body)
    departure_id = body.get("departure")
    courses = list(Course.objects.values())
    return JsonResponse(courses, safe=False)


class ClientRegistrationView(CreateView):
    template_name = "clients/register.html"
    form_class = ClientRegistrationForm
    success_url = reverse_lazy("client_home")
