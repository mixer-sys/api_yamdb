from rest_framework import viewsets, filters, generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import api_view


from users.models import User
from users.utils import send_mail_with_code
from users.serializers import (UserSerializer, UserConfirmationSerializer,
                               ConfirmationCodeSerializer)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    permission_classes = (IsAdminUser,)


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserConfirmationSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        if not request.user.is_staff:
            try:
                user = User.objects.get(
                    username=request.data['username'],
                    email=request.data['email'],
                )
                confirmation_code = default_token_generator.make_token(user)
                send_mail_with_code(
                    request.data['username'],
                    confirmation_code,
                    request.data['email']
                )
                return Response(
                    request.data,
                    status=status.HTTP_200_OK
                )
            except Exception:
                on_create_serializer = UserConfirmationSerializer(
                    data=request.data
                )
                if on_create_serializer.is_valid():
                    on_create_serializer.save()
                    user = get_object_or_404(
                        User,
                        username=request.data['username'],
                        email=request.data['email'],
                    )
                    confirmation_code = default_token_generator.make_token(user)
                    send_mail_with_code(
                        request.data['username'],
                        confirmation_code,
                        request.data['email'],
                    )
                    return Response(
                        on_create_serializer.data,
                        status=status.HTTP_200_OK
                    )
                return Response(
                    on_create_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            user = User.objects.get(
                username=request.data['username'],
                email=request.data['email'],
            )
            serializer = UserConfirmationSerializer(
                data=request.data
            )
            serializer.save()
            return Response(
                on_create_serializer.data,
                status=status.HTTP_201_CREATED
            )


@api_view(['POST'])
def get_token_jwt(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, email=email)
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        response = {
            'token': str(token)
        }
        return Response(response, status=status.HTTP_200_OK)
    response = {'confirmation_code': 'Код подтверждения не соответствует!'}
    return Response(response, status=status.HTTP_400_BAD_REQUEST)
