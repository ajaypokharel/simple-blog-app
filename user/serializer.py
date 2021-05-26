from django.contrib.auth import get_user_model
from rest_framework import serializers

USER = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = USER
        fields = ['id', 'username', 'password', 'email']
        read_only_fields = ['id']
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


