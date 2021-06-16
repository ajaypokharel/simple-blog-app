from django.urls import path, include
from knox import views as knoxViews

from rest_framework.routers import DefaultRouter

from user.views.login import KnoxLoginView
from user.views.user import UserViewSet

r = DefaultRouter()
r.register('user', UserViewSet, basename='user')

urlpatterns = [
    path('accounts/', include('rest_framework.urls')),
    path('auth/login/', KnoxLoginView.as_view(), name='knox_login'),
    path('auth/logout/', knoxViews.LogoutView.as_view(), name='knox_logout'),
] + r.urls
