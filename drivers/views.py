from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import DriverLoginForm
from .forms import DriverRegistrationForm

def driver_login(request):
    if request.method == 'POST':
        form = DriverLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, 'Invalid login credentials.')
    else:
        form = DriverLoginForm()


    return render(request, 'drivers/driver_login.html', {'form': form})

def driver_register(request):
    if request.method == 'POST':
        form = DriverRegistrationForm(request.POST)
        if form.is_valid():
            # Zapisz nowego kierowcę (Driver) i użytkownika (User)
            form.save()
            return redirect('driver_login')  # Po rejestracji przekierowujemy do strony logowania
    else:
        form = DriverRegistrationForm()

    return render(request, 'drivers/driver_register.html', {'form': form})

def dashboard_view(request):

    if request.user.is_authenticated:
        return render(request, 'drivers/dashboard.html')
    else:
        return redirect('driver_login')