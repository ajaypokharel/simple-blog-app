from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import BlogModel
from .permissions import IsBlogOwner
from .serializer import BlogPostSerializer, BlogEventModelSerializer


class BlogViewSet(ModelViewSet):

    def get_queryset(self):
        if self.action in ['events_create'] and self.request.user.is_authenticated:
            return BlogModel.objects.filter(creator=self.request.user)
        if self.action in ['like', 'unlike']:
            return BlogModel.objects.exclude(creator=self.request.user)
        return BlogModel.objects.all()

    def get_permissions(self):
        permission_classes = []
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        if self.action in ['create', 'like', 'unlike']:
            permission_classes = [IsAuthenticated]
        if self.action in ['destroy', 'update', 'partial_update']:
            permission_classes = [IsBlogOwner]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['events', 'events_create']:
            return BlogEventModelSerializer
        return BlogPostSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(creator=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['GET'])
    def events(self, request, *args, **kwargs):
        blog_obj = self.get_object()
        queryset = blog_obj.blog_events.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @events.mapping.post
    def events_create(self, request, *args, **kwargs):
        _ = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['post'])
    def like(self, request, *args, **kwargs):
        blog = self.get_object()
        likes = blog.likes
        new_like = likes + 1
        BlogModel.objects.filter(id=blog.id).update(likes=new_like)
        return Response({'detail': 'Post liked'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def unlike(self, request, *args, **kwargs):
        blog = self.get_object()
        likes = blog.likes
        new_like = likes - 1
        BlogModel.objects.filter(id=blog.id).update(likes=new_like)
        return Response({'detail': 'Post Disliked'}, status=status.HTTP_201_CREATED)