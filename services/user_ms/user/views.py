import json

from math import ceil
from decimal import Decimal
from oauth2_provider.views.generic import ProtectedResourceView
from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasReadWriteScope

from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseForbidden
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models.fields.related import ManyToManyField

from rest_framework import viewsets, filters
from rest_framework import mixins

from profiles.models import User

class UserViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, 
                  mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    View to users in the system.
    """
    queryset = User.objects.all()
    authentication_classes = OAuth2Authentication
    search_fields = ['email', 'first_name', 'last_name']
    filter_backends = [filters.SearchFilter]
    
    def list(self, request, *args, **kwargs):
        """
        Return a list of all users.
        """
        # here you can place business logic
        # I suggest importing a function from ./businnes.py
        return super().list(request, *args, **kwargs)
