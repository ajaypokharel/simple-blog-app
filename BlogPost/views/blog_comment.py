from rest_framework.permissions import IsAuthenticated

from BlogPost.models import BlogComment
from BlogPost.serializers.blog_comment import BlogCommentSerializer
from commons.mixins import RetrieveUpdateDestroyModelMixin
from user.permissions import IsUser


class BlogCommentViewSet(RetrieveUpdateDestroyModelMixin):
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'
    serializer_class = BlogCommentSerializer

    def get_queryset(self):
        return BlogComment.objects.filter(user=self.request.user)

    def get_permissions(self):
        return [IsAuthenticated()]
