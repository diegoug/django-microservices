import pytz

from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.middleware import RemoteUserMiddleware


class TimezoneMiddleware(MiddlewareMixin):
    def process_request(self, request):
        timezone.activate(pytz.timezone('America/Bogota'))


class CustomHeaderMiddleware(RemoteUserMiddleware):
    header = 'HTTP_REMOTE_USER'


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        if not request.user.is_anonymous and not request.session.session_key:
            request.session.cycle_key()
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
