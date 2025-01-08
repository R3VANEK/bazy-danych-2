
from django.shortcuts import render

def driver_rides_manage(request):
    return render(
        request,
        "drivers/rides.html",
    )
