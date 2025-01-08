
from django.shortcuts import render

def driver_courses_manage(request):
    return render(
        request,
        "drivers/courses.html",
    )
