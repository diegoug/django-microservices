from django.urls import path
from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasReadWriteScope
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework import permissions

from .views import BFFUserViewSet

view_config = {
    "api": {
            "authentication_classes": [OAuth2Authentication],
            'permission_classes':[
                permissions.IsAuthenticated, TokenHasReadWriteScope]
        },
    "web": {
            'permission_classes':[permissions.IsAuthenticated],
            'renderer_classes': [TemplateHTMLRenderer]
        }
}

urlpatterns = [
    # api
    path("api/v1/", BFFUserViewSet.as_view({
        "get": "list",
        "post": "create"
    }, **view_config["api"])),
    path("api/v1/<str:pk>", BFFUserViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy"
    }, **view_config["api"])),
    # web
    path("v1/", BFFUserViewSet.as_view({
        "get": "list",
        "post": "create"
    }, **view_config["web"]), name="main"),
    path("v1/<str:pk>", BFFUserViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy"
    }, **view_config["web"]), name="main")
]
