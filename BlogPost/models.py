from django.contrib.auth import get_user_model
from django.db import models

from commons.models import UUIDBaseModel

USER = get_user_model()


class Blog(UUIDBaseModel):
    title = models.CharField(max_length=150, blank=False)
    content = models.TextField()
    image = models.ImageField(default='default.jpg', upload_to='blog/')
    creator = models.ForeignKey(USER, on_delete=models.CASCADE, related_name='blog_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.title


class BlogEvent(UUIDBaseModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="blog_events")
    name = models.CharField(max_length=125)

    def __str__(self):
        return self.name


class Bookmark(UUIDBaseModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='fav_blog')
    user = models.ForeignKey(USER, on_delete=models.CASCADE, related_name='user_fav')


class BlogComment(UUIDBaseModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_comment')
    user = models.ForeignKey(USER, on_delete=models.CASCADE, related_name='comment_user')
    text = models.TextField()
    upvotes = models.IntegerField(default=0)
