# Generated by Django 3.1.7 on 2021-06-16 06:19

import django.contrib.auth.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.UUIDField(default=uuid.uuid4, error_messages={'unique': 'A user with that username already exists.'}, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()]),
        ),
    ]