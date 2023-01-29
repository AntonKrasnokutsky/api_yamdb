from rest_framework import serializers
from django.core import validators

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role',
                  )


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[validators.MaxLengthValidator(limit_value=254)]
    )
    username = serializers.CharField(
        required=True,
        validators=[
            validators.MaxLengthValidator(limit_value=150),
            validators.RegexValidator(regex=r'^[\w.@+\- ]+$')
        ]
    )

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, attrs):
        if attrs.get('username') == 'me':
            raise serializers.ValidationError(
                'Sorry this nickname is forbidden'
            )
        if User.objects.filter(email=attrs.get('email')) == attrs and not \
                User.objects.filter(username=attrs.get('username')).exist():
            raise serializers.ValidationError(
                'Sorry this email or username already exists.'
            )
        return attrs


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code', )
