from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import ClientLoginForm, ClientRegistrationForm  # Dodaj nowy formularz rejestracji
from django.http import HttpResponse


# Widok logowania klienta
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


# Widok strony sukcesu po zalogowaniu
def client_home(request):
    return render(request, "clients/success.html")


# Widok strony głównej
def home(request):
    return HttpResponse("Witaj na stronie głównej aplikacji Klienci!")


# Widok rejestracji klienta (oparty na klasie)


class ClientRegistrationView(CreateView):
    template_name = 'clients/register.html'  # Ścieżka do szablonu rejestracji
    form_class = ClientRegistrationForm       # Formularz rejestracji klienta
    success_url = reverse_lazy('client_login')  # Przekierowanie na stronę logowania
