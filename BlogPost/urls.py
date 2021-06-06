from rest_framework.routers import DefaultRouter

from BlogPost.views.blog import BlogViewSet
from BlogPost.views.blog_comment import BlogCommentViewSet

r = DefaultRouter()
r.register('blog', BlogViewSet, basename='blog')
r.register('comment', BlogCommentViewSet, basename='blog-comment')

urlpatterns = [

] + r.urls
