"""user_ms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import re_path, include
from django.urls import path
from django.contrib import admin
from django.shortcuts import redirect
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required

import oauth2_provider.views as oauth2_views

from .views import OAuthAplication, OAuthActiveToken, ApiVerify, HealthCheck

admin.site_header = 'Admin'
admin.site_title = 'Admin'
admin.index_title = 'Administration'
admin.empty_value_display = '**Empty**'


urlpatterns = [
    path('admin/', 
        admin.site.urls),
    re_path(r'^$', 
        lambda _: redirect('admin:index'), name='index'),
    re_path(r'^o/token/$', 
        oauth2_views.TokenView.as_view(), name="o_token"),
    re_path(r'^o/verify/', 
        ApiVerify.as_view(), name="o_verify"),
    re_path(r'^oauth/token/', 
        login_required(oauth2_views.TokenView.as_view()), name="oauth_token"),
    re_path(r'^health_check/', 
        HealthCheck.as_view()),
    re_path(r'^oauth/aplication/', 
        OAuthAplication.as_view()),
    re_path(r'^oauth/active_token/', 
        OAuthActiveToken.as_view()),
    # app
    re_path(r'^user/', 
        include('user.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
