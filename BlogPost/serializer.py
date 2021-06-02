from rest_framework import serializers

from commons.serializers import DynamicFieldsModelSerializer
from user.serializer import UserSerializer
from .models import Blog, BlogEvent, Bookmark


class BlogPostSerializer(DynamicFieldsModelSerializer):
    creator = UserSerializer(fields=['email', 'display_name'], read_only=True)

    class Meta:
        model = Blog
        fields = ['uuid', 'title', 'content', 'image', 'creator', 'likes', 'created_at', 'updated_at']
        read_only_fields = ['creator,' 'uuid', 'created_at', 'updated_at']


class BlogEventModelSerializer(DynamicFieldsModelSerializer):
    blog = BlogPostSerializer(fields=['title', 'image', 'creator', 'content'], read_only=True)

    class Meta:
        model = BlogEvent
        fields = ['uuid', 'blog', 'name']
        read_only_fields = ['blog', 'uuid']


class BookmarkSerializer(DynamicFieldsModelSerializer):
    blog = BlogPostSerializer(fields=['title', 'content', 'image', 'creator', 'likes'], read_only=True)
    user = UserSerializer(fields=['email', 'display_name'], read_only=True)

    class Meta:
        model = Bookmark
        fields = ['uuid', 'blog', 'user']
        read_only_fields = ['uuid']
