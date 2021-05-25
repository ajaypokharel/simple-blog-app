from rest_framework.routers import DefaultRouter
from .views import Blog

r = DefaultRouter()
r.register('blog', Blog, basename='blog')

urlpatterns = [

] + r.urls
