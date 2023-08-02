from rest_framework import filters, generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404

from users.models import User
from api.permissions import IsAdmin
from users.utils import send_mail_with_code
from users.serializers import (UsersSerializer, SignupSerializer,
                               ConfirmationCodeSerializer,
                               UsersNoRoleSerializer,
                               UserCreateSerializer,
                               UserUpdateSerializer)

CONFIRMATION_CODE_ERROR = 'Код подтверждения не соответствует!'


class SelfGenericView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    http_method_names = ('get', 'patch')

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UsersSerializer
        else:
            return UsersNoRoleSerializer


class UserGenericView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdmin,)
    http_method_names = ('get', 'post')
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UsersSerializer
        return UserCreateSerializer


class UserDetailGenericView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    lookup_url_kwarg = 'username'
    http_method_names = ('get', 'patch', 'delete')

    def get_serializer_class(self):
        if (
            self.request.method == 'GET'
            or self.request.method == 'DELETE'
        ):
            return UsersSerializer
        return UserUpdateSerializer


class SignUpUserGenericView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    http_method_names = ('post')

    def create(self, request):
        try:
            user = User.objects.get(
                username=request.data.get('username'),
                email=request.data.get('email'),
            )
            confirmation_code = default_token_generator.make_token(user)
            send_mail_with_code(
                request.data.get('username'),
                confirmation_code,
                request.data.get('email')
            )
            return Response(
                request.data,
                status=status.HTTP_200_OK
            )
        except Exception:
            on_create_serializer = SignupSerializer(
                data=request.data
            )
            if on_create_serializer.is_valid():
                on_create_serializer.save()
                user = get_object_or_404(
                    User,
                    username=request.data.get('username'),
                    email=request.data.get('email'),
                )
                confirmation_code = default_token_generator.make_token(user)
                send_mail_with_code(
                    request.data.get('username'),
                    confirmation_code,
                    request.data.get('email'),
                )
                return Response(
                    on_create_serializer.data,
                    status=status.HTTP_200_OK
                )
            return Response(
                on_create_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['POST'])
def get_token_jwt(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)

    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        response = {
            'token': str(token)
        }
        return Response(response, status=status.HTTP_200_OK)
    response = {'confirmation_code': CONFIRMATION_CODE_ERROR}
    return Response(response, status=status.HTTP_400_BAD_REQUEST)
