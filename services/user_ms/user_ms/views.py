
import json
from datetime import datetime

from oauth2_provider.views.generic import ProtectedResourceView
from oauth2_provider.models import Application, AccessToken

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name='dispatch')
class OAuthAplication(View):
    def get(self, request, *args, **kwargs):
        
        oauth_data = {
            'user': request.user,
            'authorization_grant_type': 'client-credentials'
        }
        
        if not Application.objects.filter(**oauth_data).exists():
            oauth_application = Application(**oauth_data)
            oauth_application.save()
        
        oauth_application = Application.objects.get(**oauth_data)

        response = {
            'client_secret': oauth_application.client_secret,
            'client_id': oauth_application.client_id
        }

        return JsonResponse(response)


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class OAuthActiveToken(View):
    def post(self, request, *args, **kwargs):
        access_token = False

        body = request.body
        json_data = json.loads(body)

        data_model = {
            'application__client_secret': json_data['client_secret'],
            'application__client_id': json_data['client_id'],
            'expires__gte': datetime.now()
        }

        access_token_object = AccessToken.objects.filter(**data_model)

        if access_token_object.exists():
            access_token = access_token_object.first().token

        return JsonResponse({'access_token':access_token})


class ApiVerify(ProtectedResourceView, View):
    def get(self, request, *args, **kwargs):
        user = request.resource_owner
        response = {
            'user': {
                'email': user.email,
            },
            'csrf_token': get_token(request),
        }

        return JsonResponse(response)


class HealthCheck(View):
    def get(self, request, *args, **kwargs):
        # TODO: check if database engine is working
        return HttpResponse(status=204)
