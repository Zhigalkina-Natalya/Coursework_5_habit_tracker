from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя."""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "telegram_chat_id")

    def create(self, validated_data):
        """Создаёт пользователя с хешированием пароля."""

        user = User.objects.create(
            email=validated_data["email"],
            telegram_chat_id=validated_data.get("telegram_chat_id"),
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """JWT авторизация по email."""

    username_field = "email"

    def validate(self, attrs):
        """Добавляем email в ответ."""

        data = super().validate(attrs)

        data["email"] = self.user.email

        return data
