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
            'role'
        )


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
