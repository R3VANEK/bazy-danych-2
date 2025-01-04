from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path("", login_required(views.client_home), name="client_home"),
    path("login/", views.client_login, name="client_login"),
    path("courses", views.courses_rest_view, name="client_courses_filter"),
    path("ride/book", views.book_ride_endpoint, name="book_ride"),
    path("register", views.ClientRegistrationView.as_view(), name="client_register"),
]
