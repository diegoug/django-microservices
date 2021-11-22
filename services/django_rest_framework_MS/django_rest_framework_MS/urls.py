"""django_rest_framework_MS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views

from rest_framework.renderers import TemplateHTMLRenderer

from .views import OAuthAplication

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^oauth/aplication/', 
        OAuthAplication.as_view({
            'get': 'retireve'
        }, renderer_classes=[TemplateHTMLRenderer]), 
        name='oauth_client_credentials'),
    url(r'^$', auth_views.LoginView.as_view(
        template_name='authentication/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
         next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    re_path(r'^library/', include('library.urls')),
]
