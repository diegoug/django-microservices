from oauth2_provider.models import Application

from rest_framework import serializers
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response


class OutputOauthApplication(serializers.ModelSerializer):
        class Meta:
            model = Application
            fields = ['client_secret', 'client_id']


class OAuthAplication(GenericViewSet):

    serializer_class = OutputOauthApplication
    pagination_class = []

    def get_template_names(self):
        if self.action == 'retireve':
            return ['oauth_client_credentials.html']
    
    def retireve(self, request, *args, **kwargs):
        """
        Return a OAuth client credentials.
        """
        oauth_data = {
            'user': request.user,
            'authorization_grant_type': 'client-credentials'
        }

        if not Application.objects.filter(**oauth_data).exists():
            oauth_application = Application(**oauth_data)
            oauth_application.save()

        self.queryset = Application.objects.get(**oauth_data)
        
        return Response(self.get_serializer(self.queryset).data)
