
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import UserViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls))
]
