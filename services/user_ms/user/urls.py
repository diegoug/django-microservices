
from django.urls import re_path

from .views import UserViewSet

app_name = 'users'
urlpatterns = [
    re_path(
        r'^api/v1/user/', 
        UserViewSet.as_view({
            'get': 'list',
            'post': 'create'
        }), name='api-user'),
    re_path(
        r'^api/v1/user/(?P<email>[\w.@+-]+)/$', 
        UserViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }, lookup_field='email'), name='api-user'),
    re_path(
        r'^api/v1/user/(?P<pk>[0-9]+)/$', 
        UserViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }), name='api-user')
]
