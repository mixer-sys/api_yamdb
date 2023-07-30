import re
from rest_framework import serializers

from users.models import User


class UsersSerializer(serializers.ModelSerializer):

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


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

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
        if (
            re.search(r'^[a-zA-Z0-9_.-]*$', value) is None
            or len(value) > 150
        ):
            raise serializers.ValidationError(
                'Некорректное поле username!'
            )
        users = User.objects.all()
        for user in users:
            if value == user.username:
                raise serializers.ValidationError(
                    'Пользователь с таким username существует!'
                )
        return value

    def validate_email(self, value):
        if len(value) > 254:
            raise serializers.ValidationError(
                'Некорректное значение email'
            )
        users = User.objects.all()
        for user in users:
            if value == user.email:
                raise serializers.ValidationError(
                    'Пользователь с таким email существует!'
                )
        return value


class UserUpdateSerializer(serializers.ModelSerializer):

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


class UsersNoRoleSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
        )

    def validate_username(self, value):
        if (
            re.search(r'^[a-zA-Z0-9_.-]*$', value) is None
            or len(value) > 150
        ):
            raise serializers.ValidationError(
                'Некорректное поле username!'
            )
        return value

    def validate_email(self, value):
        if len(value) > 254:
            raise serializers.ValidationError(
                'Некорректное значение email'
            )
        return value


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'email',
            'username',
        )

    def validate_username(self, value):
        if (
            re.search(r'^[a-zA-Z0-9_.-]*$', value) is None
            or len(value) > 150
            or value == 'me'
        ):
            raise serializers.ValidationError(
                'Некорректное поле username!'
            )
        users = User.objects.all()
        for user in users:
            if value == user.username:
                raise serializers.ValidationError(
                    'Пользователь с таким username существует!'
                )
        return value

    def validate_email(self, value):
        if len(value) > 254:
            raise serializers.ValidationError(
                'Некорректное значение email'
            )
        users = User.objects.all()
        for user in users:
            if value == user.email:
                raise serializers.ValidationError(
                    'Пользователь с таким email существует!'
                )
        return value


class ConfirmationCodeSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'email',
            'confirmation_code',
        )
