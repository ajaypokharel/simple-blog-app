from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from BlogPost.models import Blog
from BlogPost.permissions import IsBlogOwner
from BlogPost.serializers.blog import BlogEventModelSerializer, BlogPostSerializer
from BlogPost.serializers.blog_comment import BlogCommentSerializer


class BlogViewSet(ModelViewSet):
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        if self.action in ['events_create'] and self.request.user.is_authenticated:
            return Blog.objects.filter(creator=self.request.user)
        if self.action in ['like', 'unlike']:
            return Blog.objects.exclude(creator=self.request.user)
        return Blog.objects.all()

    def get_permissions(self):
        permission_classes = []
        if self.action in ['list', 'retrieve', 'comment']:
            permission_classes = [AllowAny]
        if self.action in ['create', 'like', 'unlike', 'do_comment']:
            permission_classes = [IsAuthenticated]
        if self.action in ['destroy', 'update', 'partial_update']:
            permission_classes = [IsBlogOwner]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['events', 'events_create']:
            return BlogEventModelSerializer
        if self.action in ['comment', 'do_comment']:
            return BlogCommentSerializer
        return BlogPostSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        lookup_url_kwargs = self.lookup_url_kwarg or self.lookup_field
        if self.action == 'do_comment':
            if lookup_url_kwargs in self.kwargs:
                context['blog'] = self.get_object()
        return context

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        if self.action in ['update', 'partial_update', 'create']:
            kwargs['fields'] = ['title', 'content', 'image']
        if self.action in ['do_comment']:
            kwargs['fields'] = ['text']
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
        Blog.objects.filter(id=blog.id).update(likes=new_like)
        return Response({'detail': 'Post liked'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def unlike(self, request, *args, **kwargs):
        blog = self.get_object()
        likes = blog.likes
        new_like = likes - 1
        Blog.objects.filter(id=blog.id).update(likes=new_like)
        return Response({'detail': 'Post Disliked'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def comment(self, request, *args, **kwargs):
        instance = self.get_object()
        queryset = instance.blog_comment.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @comment.mapping.post
    def do_comment(self, request, *args, **kwargs):
        _ = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


