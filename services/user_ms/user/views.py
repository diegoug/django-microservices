
from oauth2_provider.contrib.rest_framework import OAuth2Authentication, \
    IsAuthenticatedOrTokenHasScope

from django.contrib.auth import login
from django.core.exceptions import PermissionDenied

from rest_framework import status, viewsets, filters, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, DjangoModelPermissions
from rest_framework.authentication import SessionAuthentication

from profiles.models import User

from .serializers import UserModelSerializer, UserUpdateModelSerializer, \
    UserLoginSerializer, UserSignUpSerializer, UserGetOAuthCredentials, \
    UserGetOAuthToken


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
         Remove CSRF check
    """
    def enforce_csrf(self, request):
        return None


class UserViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, 
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
    ):

    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    
    authentication_classes = [
        CsrfExemptSessionAuthentication, OAuth2Authentication]
    permission_classes = [
        IsAuthenticatedOrTokenHasScope, DjangoModelPermissions]
    
    search_fields = ['email', 'first_name', 'last_name']
    filter_backends = [filters.SearchFilter]

    lookup_field = 'email'
    lookup_value_regex = '[\w.@+-]+'

    required_scopes = ['read', 'write', 'groups', 'introspection']
    
    def get_permissions(self):
        if 'post' in self.action_map:
            if self.action_map['post'] in ['signup', 'login']:
                return []
        return super(UserViewSet, self).get_permissions()
    
    def get_serializer_class(self):
        if self.action == 'signup':
            return UserSignUpSerializer
        if self.action == 'login':
            return UserLoginSerializer
        if self.action == 'update':
            return UserUpdateModelSerializer
        return super(UserViewSet, self).get_serializer_class()

    def create(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied()
        return super(UserViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user_to_delete = self.get_object()
        if user_to_delete != request.user and not request.user.is_superuser:
            raise PermissionDenied()
        return super(UserViewSet, self).update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        user_to_delete = self.get_object()
        if user_to_delete != request.user and not request.user.is_superuser:
            raise PermissionDenied()
        return super(UserViewSet, self).destroy(request, *args, **kwargs)

    # custom actions ----------------------------------------------------------
    @action(methods=['post'], detail=False, permission_classes=[AllowAny])
    def req_signup(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False, permission_classes=[AllowAny])
    def req_login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, grant_type, client_secret, client_id = serializer.save()
        login(request, user)
        data = {
            'user': UserModelSerializer(user).data,
            'grant_type': grant_type,
            'client_secret': client_secret,
            'client_id': client_id
        }
        return Response(data, status=status.HTTP_201_CREATED)
    
    @action(methods=['get'], detail=False)
    def oauth_credentials(self, request):
        serializer = UserGetOAuthCredentials(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        grant_type, client_secret, client_id = serializer.save()
        data = {
            'grant_type': grant_type,
            'client_secret': client_secret,
            'client_id': client_id
        }
        return Response(data, status=status.HTTP_201_CREATED)
    
    @action(methods=['post'], detail=False)
    def oauth_active_token(self, request):
        serializer = UserGetOAuthToken(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        access_token = serializer.save()
        if not access_token:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = {
            'access_token': access_token
        }
        return Response(data, status=status.HTTP_200_OK)
