from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models

from commons.constants import GENDER_CHOICES
from commons.models import TimeStampModel


class User(AbstractUser):
    email = models.EmailField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.username

    @property
    def display_name(self):
        return f'{self.first_name} {self.last_name}'
