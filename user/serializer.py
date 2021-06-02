from django.contrib.auth import get_user_model
from rest_framework import serializers

from commons.constants import GENDER_CHOICES
from commons.serializers import DynamicFieldsModelSerializer

USER = get_user_model()


class UserSerializer(DynamicFieldsModelSerializer):
    gender = serializers.ChoiceField(choices=GENDER_CHOICES, allow_blank=True, allow_null=True)

    class Meta:
        model = USER
        fields = ['email', 'first_name', 'last_name', 'gender', 'username']
        read_only_fields = ['username', 'display_name']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = USER.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


