from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rides.models import Ride

@csrf_exempt
def book_ride_endpoint(request):
    body = json.loads(request.body)
    departure_id = int(body.get("departureId"))
    course_id = int(body.get("courseId"))

    try:
        _, created = Ride.objects.get_or_create(
            course_id=course_id,
            departure_id=departure_id,
            client_id=request.user.client.id,
        )
    except Exception:
        return JsonResponse(
            {
                "type": "error",
                "text": "Some unexpected error occured, please try again",
            },
            safe=False,
        )

    if not created:
        type = "error"
        text = "You already booked this ride!"
    else:
        type = "success"
        text = "Successfully booked a ride!"

    return JsonResponse(
        {
            "type": type,
            "text": text,
        },
        safe=False,
    )
