from django.urls import path
from django.contrib.auth.decorators import login_required
from .views.auth_views import client_login
from .views.ride_views import client_home
from .views.ride_views import book_ride_endpoint, courses_rest_view
from .views.registration_views import ClientRegistrationView

urlpatterns = [
    path("login/", client_login, name="client_login"),
    path("", login_required(client_home), name="client_home"), 
    path("ride/book", book_ride_endpoint, name="book_ride"),
    path("courses", courses_rest_view, name="courses_rest_view"),
    path("register/", ClientRegistrationView.as_view(), name="client_register"),
]
