from django.http import HttpResponse
from django.views.generic import View


class HealthCheck(View):
    def get(self, request, *args, **kwargs):
        # TODO: check if database engine is working
        return HttpResponse(status=204)
