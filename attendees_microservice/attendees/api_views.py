from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Attendee, ConferenceVO
# from events.models import Conference
# from events.api_views import ConferenceListEncoder
from common.json import ModelEncoder
import json


class ConferenceVODetailEncoder(ModelEncoder):
    model = ConferenceVO
    properties = ["name", "import_href"]


class AttendeeListEncoder(ModelEncoder):
    model = Attendee
    properties = [
        "name",
    ]


class AttendeeDetailEncoder(ModelEncoder):
    model = Attendee
    # changing the position of the properties changes the order they display
    properties = [
        "email",
        "name",
        "company_name",
        "created",
        "conference",  # in this case, the name is required to display this data
    ]
    # uses import to pull all the data from the list
    encoders = {
        "conference": ConferenceVODetailEncoder()
    }


@require_http_methods(["GET", "POST"])
def api_list_attendees(request, conference_vo_id=None):
    if request.method == "GET":
        attendees = Attendee.objects.filter(conference=conference_vo_id)
        return JsonResponse(
            {"attendees": attendees},
            encoder=AttendeeListEncoder,
        )
    else:
        content = json.loads(request.body)
        try:
            conference_href = content["conference"]
            conference = ConferenceVO.objects.get(import_href=conference_href)
            content["conference"] = conference
        except ConferenceVO.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid conference id"},
                status=400,
            )

        attendee = Attendee.objects.create(**content)
        return JsonResponse(
            attendee,
            encoder=AttendeeDetailEncoder,
            safe=False,
        )
    # """
    # Lists the attendees names and the link to the attendee
    # for the specified conference id.

    # Returns a dictionary with a single key "attendees" which
    # is a list of attendee names and URLS. Each entry in the list
    # is a dictionary that contains the name of the attendee and
    # the link to the attendee's information.

    # {
    #     "attendees": [
    #         {
    #             "name": attendee's name,
    #             "href": URL to the attendee,
    #         },
    #         ...
    #     ]
    # }
    # """
    # response = []
    # attendees = Attendee.objects.all()
    # for attendee in attendees:
    #     response.append(
    #         {
    #             "name": attendee.name,
    #             "href": attendee.get_api_url(),
    #         }
    #     )
    # return JsonResponse({"attendees": response})


@require_http_methods(["GET", "PUT", "DELETE"])
def api_show_attendee(request, pk):
    if request.method == "GET":
        attendee = Attendee.objects.get(id=pk)
        return JsonResponse(
            attendee,
            encoder=AttendeeDetailEncoder,
            safe=False,
        )
    elif request.method == "DELETE":
        count, _ = Attendee.objects.filter(id=pk).delete()
        return JsonResponse({"deleted": count > 0})
    else:
        content = json.loads(request.body)
        try:
            if "conference" in content:
                conference = Conference.objects.get(id=content["conference"])
                content["conference"] = conference
        except Conference.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid conference id"},
                status=400,
            )

        Attendee.objects.filter(id=pk).update(**content)
        attendee = Attendee.objects.get(id=pk)
        return JsonResponse(
            attendee,
            encoder=AttendeeDetailEncoder,
            safe=False,
        )
    # """
    # Returns the details for the Attendee model specified
    # by the pk parameter.

    # This should return a dictionary with email, name,
    # company name, created, and conference properties for
    # the specified Attendee instance.

    # {
    #     "email": the attendee's email,
    #     "name": the attendee's name,
    #     "company_name": the attendee's company's name,
    #     "created": the date/time when the record was created,
    #     "conference": {
    #         "name": the name of the conference,
    #         "href": the URL to the conference,
    #     }
    # }
    # """
    # attendee = Attendee.objects.get(id=pk)
    # return JsonResponse(
    #     {
    #         "email": attendee.email,
    #         "name": attendee.name,
    #         "company_name": attendee.company_name,
    #         "created": attendee.created,
    #         "conference": {
    #             "name": attendee.conference.name,
    #             "href": attendee.conference.get_api_url(),
    #         },
    #     }
    # )
