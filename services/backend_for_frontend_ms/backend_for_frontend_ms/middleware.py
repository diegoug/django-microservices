
import pytz
import json
import requests

from django.utils import timezone
from django.http import Http404
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


class TimezoneMiddleware(MiddlewareMixin):
    def process_request(self, request):
        timezone.activate(pytz.timezone('America/Bogota'))


class SetOautClientCredentials(MiddlewareMixin):
    def process_request(self, request):
        
        if request.user.is_anonymous:
            return
        
        cookies = {
            'sessionid': request.session.session_key
        }

        headers = {
            'remote-user': request.user.get_username()
        }

        url = '{}/api/v1/user/oauth_credentials/'.format(settings.USER_MS_HOST)

        oauth_credentilas = requests.get(
            url=url, cookies=cookies, headers=headers)

        if oauth_credentilas.status_code != 201:
                raise Http404
        
        oauth_credentilas = json.loads(oauth_credentilas.text)

        url ='{}/api/v1/user/oauth_active_token/'.format(settings.USER_MS_HOST)
        
        request_token = requests.post(
            url=url, cookies=cookies, data=oauth_credentilas, headers=headers)

        if request_token.status_code == 404:

            headers = {
                'content-type': "application/x-www-form-urlencoded",
                'cache-control': "no-cache",
            }

            url = '{}/oauth/token/'.format(settings.USER_MS_HOST)
            
            request_token = requests.post(
                url=url, cookies=cookies, data=oauth_credentilas, 
                headers=headers)

            if request_token.status_code != 200:
                raise Http404
        
        if request_token.status_code != 200:
            raise Http404
        
        request_token = json.loads(request_token.text)

        request.user.oauth_access_token = request_token['access_token']

        return
