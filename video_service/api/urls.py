from core.urls import router_api_v1
from django.urls import include, path

from api.views import VideoViewSet

router_api_v1.register(r'videos', VideoViewSet, basename='videos')

urlpatterns = [
    path('', include(router_api_v1.urls)),
]
