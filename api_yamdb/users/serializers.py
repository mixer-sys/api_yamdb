import re
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

    def validate_username(self, value):
        if re.search(r'^[a-zA-Z][a-zA-Z0-9-_]{2,25}$', value) is None:
            raise serializers.ValidationError(
                'Некорректное поле username!'
            )
        return value


class UserConfirmationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'username',
        )


class ConfirmationCodeSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)
