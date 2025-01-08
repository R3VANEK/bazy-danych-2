
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from ..forms import DriverLoginForm, DriverRegistrationForm

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

class DriverRegistrationView(CreateView):
    template_name = "drivers/register.html"
    form_class = DriverRegistrationForm
    success_url = reverse_lazy("driver_home")
