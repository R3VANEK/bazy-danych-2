from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Patient


# Create your views here.
def index(request, id):

    patient = Patient.objects.get(id=1)
    events = patient.events.all()
    return render(
        request, "client_details.html", {"patient": patient, "events": events}
    )
