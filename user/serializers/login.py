from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from user.serializers.user import UserSerializer

USER = get_user_model()


class LoginSerializer(UserSerializer):
    groups = serializers.SerializerMethodField()

    class Meta:
        model = USER
        fields = ['email', 'first_name', 'last_name', 'gender', 'username', 'groups']

    def validate(self, attrs):
        USER.objects.get(email=attrs['email'])
        if USER.DoesNotExist:
            raise serializers.ValidationError({'detail': 'User does not exist'})
        return attrs

    @staticmethod
    def get_groups(obj):
        return obj.groups.all().values_list('name', flat=True)


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label="email")
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            try:
                USER.objects.get(email=attrs['email'])
            except USER.DoesNotExist:
                raise serializers.ValidationError({'detail': "User doesn't exist. Please enter correct username"})
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            if not user:
                msg = 'Please enter correct email or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
