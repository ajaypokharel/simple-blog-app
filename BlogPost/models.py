from django.contrib.auth import get_user_model
from django.db import models


USER = get_user_model()


class BlogModel(models.Model):
    title = models.CharField(max_length=150, blank=False)
    content = models.TextField(null=True)
    image = models.ImageField(default='default.jpg', upload_to='blog/')
    creator = models.ForeignKey(USER, related_name='blogs', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.title


class BlogEvent(models.Model):
    blog = models.ForeignKey(BlogModel, on_delete=models.CASCADE, related_name="blog_events")
    name = models.CharField(max_length=125)

    def __str__(self):
        return self.name
