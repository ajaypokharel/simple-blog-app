from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, AbstractUser
from django.db import models


class BlogUser(AbstractUser):
    email = models.EmailField()

    def __str__(self):
        return self.username
