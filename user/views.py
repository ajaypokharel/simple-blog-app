from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from user.permissions import IsUser
from user.serializer import UserSerializer

USER = get_user_model()


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.action in ['destroy', 'update', 'partial_update']:
            return USER.objects.all(username=self.request.user.username)
        return USER.objects.all()

    def get_permissions(self):
        permission_classes = []
        if self.action in ['list', 'retrieve', 'create']:
            permission_classes = [AllowAny]
        if self.action in ['destroy', 'update', 'partial_update']:
            permission_classes = [IsUser]
        return [permission() for permission in permission_classes]