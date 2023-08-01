import re
from rest_framework import serializers
from users.models import User

EMAIL_EXIST_MESSAGE = 'Пользователь с таким email существует!'
USERNAME_EXIST_MESSAGE = 'Пользователь с таким username существует!'
EMAIL_ERROR_MESSAGE = 'Некорректное значение email'
USERNAME_ERROR_MESSAGE = 'Некорректное поле username!'
REGULAR_EXPRESSION = r'^[a-zA-Z0-9_.-]*$'


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role',)


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role',)

    def validate_username(self, value):
        if (
            re.search(REGULAR_EXPRESSION, value) is None
            or len(value) > 150
        ):
            raise serializers.ValidationError(
                USERNAME_ERROR_MESSAGE
            )
        users = User.objects.all()
        for user in users:
            if value == user.username:
                raise serializers.ValidationError(
                    USERNAME_EXIST_MESSAGE
                )
        return value

    def validate_email(self, value):
        if len(value) > 254:
            raise serializers.ValidationError(
                EMAIL_ERROR_MESSAGE
            )
        users = User.objects.all()
        for user in users:
            if value == user.email:
                raise serializers.ValidationError(
                    EMAIL_EXIST_MESSAGE
                )
        return value


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role',)


class UsersNoRoleSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',)

    def validate_username(self, value):
        if (
            re.search(REGULAR_EXPRESSION, value) is None
            or len(value) > 150
        ):
            raise serializers.ValidationError(
                USERNAME_ERROR_MESSAGE
            )
        return value

    def validate_email(self, value):
        if len(value) > 254:
            raise serializers.ValidationError(
                EMAIL_ERROR_MESSAGE
            )
        return value


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'username',)

    def validate_username(self, value):
        if (
            re.search(REGULAR_EXPRESSION, value) is None
            or len(value) > 150
            or value == 'me'
        ):
            raise serializers.ValidationError(
                USERNAME_ERROR_MESSAGE
            )
        users = User.objects.all()
        for user in users:
            if value == user.username:
                raise serializers.ValidationError(
                    USERNAME_EXIST_MESSAGE
                )
        return value

    def validate_email(self, value):
        if len(value) > 254:
            raise serializers.ValidationError(
                EMAIL_ERROR_MESSAGE
            )
        users = User.objects.all()
        for user in users:
            if value == user.email:
                raise serializers.ValidationError(
                    EMAIL_EXIST_MESSAGE
                )
        return value


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code',)
