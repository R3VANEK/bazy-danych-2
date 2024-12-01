# drivers/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.driver_register, name='driver_register'),  # URL do rejestracji
    path('login/', views.driver_login, name='driver_login'),  # Ścieżka do formularza logowania
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
