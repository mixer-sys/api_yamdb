from rest_framework import viewsets, filters, generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404


from users.models import User
from users.serializers import UserSerializer, UserConfirmationSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserConfirmationSerializer

    def create(self, request):
        on_create_serializer = UserConfirmationSerializer(data=request.data)
        if on_create_serializer.is_valid():
            on_create_serializer.save()
            user = get_object_or_404(
                User,
                username=request.data['username']
            )
            confirmation_code = default_token_generator.make_token(user)
            user_email = request.data['email']
            send_mail(
                subject='Код подтверждения',
                message=f'Ваш код подтверждения: {confirmation_code}',
                from_email='from@example.com',
                recipient_list=[user_email],
                fail_silently=True,
            )
            return Response(
                on_create_serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            on_create_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
