from django.urls import re_path

from rest_framework.renderers import TemplateHTMLRenderer
from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasReadWriteScope
from rest_framework import  permissions

from .views import BookListAPI

def conf_view(type):
    conf = { 
        'api': {
            'authentication_classes':[OAuth2Authentication], 
            'permission_classes':[
                permissions.IsAuthenticated, TokenHasReadWriteScope]
        },
        'web': {
            'renderer_classes': [TemplateHTMLRenderer]
        }
    }
    return conf[type]

app_name = 'books'
urlpatterns = [
    re_path(
        r'^v1/book/', 
        BookListAPI.as_view({
            'get': 'list'
        }, **(conf_view('web')) ), name='web-bookings-list'),
    
    re_path(
        r'^api/v1/book/', 
        BookListAPI.as_view({
            'get': 'list'
        }, **(conf_view('api')) ), name='api-bookings-list')
]