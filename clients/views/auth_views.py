from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from ..forms import ClientLoginForm

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
