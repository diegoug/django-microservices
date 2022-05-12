
import json
import requests

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response


class BFFUserViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, 
                     mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        if self.action == "list":
            return ["list.html"]

    def list(self, request, *args, **kwargs):
        """
        Return a list of all users.
        """
        cookies = {
            'sessionid': request.session.session_key
        }
        
        headers = {
            'remote-user': request.user.get_username(),
            'authorization': "{} {}".format(
                'Bearer', request.user.oauth_access_token)
        }
        
        url = 'http://user-ms:8084/api/v1/user/'
        request_data = requests.get(url=url, cookies=cookies, headers=headers)

        return Response(json.loads(request_data.text))
