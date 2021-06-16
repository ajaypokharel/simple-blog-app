import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from commons.constants import GENDER_CHOICES
from commons.models import TimeStampModel


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.UUIDField(
        max_length=100,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': 'A user with that username already exists.',
        },
        default=uuid.uuid4
    )
    email = models.EmailField(
        unique=True, max_length=50,
        error_messages={
            'unique': 'A user with that email already exists.',
        },
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    @property
    def display_name(self):
        return f'{self.first_name} {self.last_name}'
