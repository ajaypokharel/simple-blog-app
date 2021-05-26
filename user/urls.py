from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user.views import UserViewSet

r = DefaultRouter()
r.register('user', UserViewSet, basename='user')

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
] + r.urls
