from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail

from rest_framework import (
    filters, permissions, status, viewsets,
)
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .paginators import APIPagination
from .permissions import IsAdmin
from .serializers import (
    APIUserSerializer,
    ConfirmationSerializer,
    CustomUserSerializer,
)


@action(detail=True, methods=['POST'])
class APIAuthCodeRequestViewSet(viewsets.ModelViewSet):
    """Регистрация нового пользователя."""
    permission_classes = (permissions.AllowAny, )
    serializer_class = CustomUserSerializer

    def perform_create(self, serializer):
        """Отправка кода, создание пользователя."""
        email = serializer.validated_data['email']
        username = email.split('@')[0]
        user = CustomUser.objects.create_user(
            email,
            email,
            first_name=username,
            description='Registered from API'
        )
        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        user.set_password(confirmation_code)
        serializer = CustomUserSerializer(user)
        user.save()
        send_mail(f'YAMDB confirmation code for {username}',
                  f'Hi, {username}!\n\n'
                  + f'You confirmation code is: {confirmation_code}\n\n'
                  + '---\nYAMDB',
                  settings.EMAIL_AUTH, [email])
        return Response(
            {'status': 'The authorization letter was sent by email.'}
        )


@action(detail=True, methods=['POST'])
class APIAuthConfirm(viewsets.ModelViewSet):
    """Выдача JWT-токена."""
    permission_classes = (permissions.AllowAny, )
    serializer_class = ConfirmationSerializer

    def create(self, request):
        serializer = ConfirmationSerializer(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            user = CustomUser.objects.filter(email=email).first()
            if user is not None:
                confirm_code = serializer.validated_data['confirmation_code']
                if confirm_code == user.confirmation_code:
                    refresh = RefreshToken.for_user(user)
                    JWT = {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                    }
                    return Response(JWT, status=status.HTTP_200_OK)


class APIUserProfileViewSet(viewsets.ModelViewSet):
    """Управление пользователями."""
    permission_classes = (IsAdmin, )
    queryset = CustomUser.objects.all()
    serializer_class = APIUserSerializer
    pagination_class = APIPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        serializer_class=APIUserSerializer,
        permission_classes=[permissions.IsAuthenticated],
        url_path='me'
    )
    def me(self, request, pk=None):
        user = CustomUser.objects.filter(id=self.request.user.id).first()
        serializer = APIUserSerializer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            if self.request.method == 'PATCH':
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
