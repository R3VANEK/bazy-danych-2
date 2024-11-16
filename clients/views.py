from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import ClientLoginForm
from django.shortcuts import render
from django.http import HttpResponse


def client_login(request):
    if request.method == "POST":
        form = ClientLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            client = authenticate(request, username=username, password=password)
            if client is not None:
                login(request, client)
                return redirect("client_home")
    else:
        form = ClientLoginForm()

    return render(request, "clients/login.html", {"form": form})


def client_home(request):
    return render(request, "clients/success.html")


def home(request):
    return HttpResponse("Witaj na stronie głównej aplikacji Klienci!")
