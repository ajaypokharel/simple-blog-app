from rest_framework import serializers
from .models import BlogModel, BlogEvent


class BlogPostSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = BlogModel
        fields = ['id', 'title', 'content', 'image', 'creator']


class BlogEventModelSerializer(serializers.ModelSerializer):
    blog = BlogPostSerializer(read_only=True)

    class Meta:
        model = BlogEvent
        fields = ['id', 'blog', 'name']
        read_only_fields = ['id', 'blog']
