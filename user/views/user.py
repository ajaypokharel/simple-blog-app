from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from BlogPost.models import Bookmark
from BlogPost.serializers.blog import BookmarkSerializer
from user.permissions import IsUser
from user.serializers.user import UserSerializer

USER = get_user_model()


class UserViewSet(ModelViewSet):
    lookup_field = 'username'
    lookup_url_kwarg = 'username'
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        if self.action in ['destroy', 'update', 'partial_update']:
            return USER.objects.all(username=self.request.user.username)
        if self.action in ['bookmarks']:
            return Bookmark.objects.filter(user=self.request.user)
        return USER.objects.all()

    def get_permissions(self):
        permission_classes = []
        if self.action in ['list', 'retrieve', 'create']:
            permission_classes = [AllowAny]
        if self.action in ['destroy', 'update', 'partial_update', 'bookmarks']:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['bookmarks']:
            return BookmarkSerializer
        return UserSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        if self.action in ['update', 'partial_update']:
            kwargs['fields'] = ['email', 'first_name', 'last_name', 'gender']
        return serializer_class(*args, **kwargs)

    @action(detail=False, methods=['get'])
    def bookmarks(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
