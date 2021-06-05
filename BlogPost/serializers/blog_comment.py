from BlogPost.models import BlogComment
from BlogPost.serializers.blog import BlogPostSerializer
from commons.serializers import DynamicFieldsModelSerializer
from user.serializers.user import UserSerializer


class BlogCommentSerializer(DynamicFieldsModelSerializer):
    user = UserSerializer(fields=['display_name', 'email'], read_only=True)
    blog = BlogPostSerializer(fields=['title', 'content', 'image', 'creator', 'likes'], read_only=True)

    class Meta:
        model = BlogComment
        fields = ['uuid', 'user', 'text', 'upvotes', 'blog']
        read_only_fields = ['uuid', 'upvotes', 'user', 'blog']

    def create(self, validated_data):
        validated_data['blog'] = self.context.get('blog')
        validated_data['user'] = self.request.user
        instance = super().create(validated_data)
        return instance
