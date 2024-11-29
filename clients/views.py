from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import (
    ClientLoginForm,
    ClientRegistrationForm,
)
from django.http import HttpResponse


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

    return render(request, "login.html", {"form": form, "is_error": is_error})


def client_home(request):
    return render(request, "success.html")


def home(request):
    return HttpResponse("Witaj na stronie głównej aplikacji Klienci!")


class ClientRegistrationView(CreateView):
    template_name = "register.html"
    form_class = ClientRegistrationForm
    success_url = reverse_lazy("home")
