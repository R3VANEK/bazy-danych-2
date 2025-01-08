from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from clients.utils import get_courses

@csrf_exempt
def courses_rest_view(request):
    body = json.loads(request.body)
    filtered_courses = get_courses(
        client=request.user.client,
        destination_id=body.get("destination"),
        driver_grade=body.get("grade"),
        max_price=body.get("maxPrice"),
        time_for_departure=body.get("timeForDeparture"),
        driver_is_male=body.get("driverGender"),
    )
    return JsonResponse(list(filtered_courses.values()), safe=False)