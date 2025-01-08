from django.urls import path
from django.contrib.auth.decorators import login_required
from .views.auth_views import client_login
from .views.home import client_home
from .views.courses import courses_rest_view
from .views.ride import book_ride_endpoint
from .views.registration_views import ClientRegistrationView

urlpatterns = [
    path("login/", client_login, name="client_login"),
    path("", login_required(client_home), name="client_home"), 
    path("courses", courses_rest_view, name="courses_rest"),
    path("ride/book", book_ride_endpoint, name="book_ride"),
    path("register/", ClientRegistrationView.as_view(), name="client_register"),
]
