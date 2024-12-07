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
from django.contrib.auth.decorators import login_required
import json


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

    return render(request, "login.html", {"form": form, "is_error": is_error})


@login_required
def client_home(request):
    return render(
        request,
        "main.html",
        {
            "get_courses_url": f"{request.build_absolute_uri()}clients/courses",
            "planets": list(Planet.objects.all().distinct().values()),
        },
    )


@csrf_exempt
def courses_rest_view(request):
    body = json.loads(request.body)
    departure_id = body.get("departure")
    courses = list(Course.objects.values())
    return JsonResponse(courses, safe=False)


class ClientRegistrationView(CreateView):
    template_name = "register.html"
    form_class = ClientRegistrationForm
    success_url = reverse_lazy("home")
