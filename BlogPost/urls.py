from rest_framework.routers import DefaultRouter
from .views import BlogViewSet

r = DefaultRouter()
r.register('blog', BlogViewSet, basename='blog')

urlpatterns = [

] + r.urls
