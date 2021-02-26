from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели CustomUser."""

    class Meta:
        model = CustomUser
        fields = ['email', ]


class ConfirmationSerializer(serializers.Serializer):
    """Сериалайзер для views авторизации, выдача JWT-token."""
    email = serializers.EmailField(max_length=60)
    confirmation_code = serializers.CharField(max_length=24)

    class Meta:
        fields = ['email', 'confirmation_code', ]


class APIUserSerializer(serializers.ModelSerializer):
    """Сериалайзер для views создания и редактирования профиля."""

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name',
                  'username', 'bio', 'email', 'role']
