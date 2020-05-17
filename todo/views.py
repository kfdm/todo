from collections import defaultdict

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView, Response
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import RedirectView, TemplateView

from todo import caldav, models
from todo.caldav import ET


class WellKnownCaldav(APIView):
    http_method_names = ["get", "head", "options", "propfind"]
    permission_classes = [AllowAny]

    def get(self, request):
        return redirect("discovery")

    def propfind(self, request):
        return redirect("discovery")


# https://www.webdavsystem.com/server/creating_caldav_carddav/discovery/#nav_featuressupportdiscovery
class CaldavView(APIView):
    def options(self, request, *args, **kwargs):
        """Handle responding to requests for the OPTIONS HTTP verb."""
        response = HttpResponse()
        response["Allow"] = ", ".join(self._allowed_methods())
        response["Content-Length"] = "0"
        response["DAV"] = "1, 2, 3, calendar-access, addressbook, extended-mkcol"
        return response


class Principal(CaldavView):
    http_method_names = ["options", "propfind", "mkcalendar", "put", "proppatch"]
    # DELETE, GET, HEAD, MKCALENDAR, MKCOL, MOVE, OPTIONS, PROPFIND, PROPPATCH, PUT, REPORT

    def propfind(self, request, user):
        propstats = caldav.Propstats()
        for prop, value in request.data.get("{DAV:}prop", {}).items():
            status, value = caldav.propfind(request, prop, value, request.user)
            propstats[status].append(value)
        return propstats.render(request)

    def proppatch(self, request, user):
        propstats = caldav.Propstats()
        set_request = request.data.get("{DAV:}set", {})

        for prop, value in set_request.get("{DAV:}prop", {}).items():
            status, result = caldav.proppatch(request, prop, value, None)
            propstats[status].append(result)

        return propstats.render(request)


class Calendar(CaldavView):
    http_method_names = ["options", "mkcalendar", "proppatch", "delete"]

    def delete(self, request, user, calendar):
        calendar = get_object_or_404(models, Calendar, owner=request.user, id=calendar)
        return HttpResponse(status=400)

    def proppatch(self, request, user, calendar):
        calendar = get_object_or_404(models, Calendar, owner=request.user, id=calendar)

        propstats = caldav.Propstats()
        set_request = request.data.get("{DAV:}set", {})

        for prop, value in set_request.get("{DAV:}prop", {}).items():
            status, result = caldav.proppatch(request, prop, value, calendar)
            propstats[status].append(result)

        if propstats[200]:
            calendar.save()

        return propstats.render(request)

    def mkcalendar(self, request, user, calendar):
        calendar = models.Calendar(owner=request.user, id=calendar)

        propstats = caldav.Propstats()
        set_request = request.data.get("{DAV:}set", {})

        for prop, value in set_request.get("{DAV:}prop", {}).items():
            status, result = caldav.proppatch(request, prop, value, calendar)
            propstats[status].append(result)

        if propstats[200]:
            calendar.save()
            return HttpResponse(status=201)

        return HttpResponse(status=400)


# https://www.webdavsystem.com/server/creating_caldav_carddav/discovery/#nav_currentuserprincipaldiscovery
class UserPrincipalDiscovery(CaldavView):
    http_method_names = ["options", "propfind"]

    def propfind(self, request):
        propstats = caldav.Propstats()
        for prop,value in request.data.get("{DAV:}prop", {}).items():
            status, result = caldav.propfind(request, prop, value)
            propstats[status].append(result)

        return propstats.render(request)