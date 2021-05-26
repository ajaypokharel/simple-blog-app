from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import BlogModel
from .permissions import IsBlogOwner
from .serializer import BlogPostSerializer, BlogEventModelSerializer


class Blog(ModelViewSet):

    def get_queryset(self):
        if self.action in ['events_create'] and self.request.user.is_authenticated:
            return BlogModel.objects.filter(creator=self.request.user)
        return BlogModel.objects.all()

    def get_permissions(self):
        permission_classes = []
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        if self.action in ['create']:
            permission_classes = [IsAuthenticated]
        if self.action in ['destroy', 'update', 'partial_update']:
            permission_classes = [IsBlogOwner]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['events', 'events_create']:
            return BlogEventModelSerializer
        return BlogPostSerializer

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
