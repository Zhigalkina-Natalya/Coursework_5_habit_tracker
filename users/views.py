from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import CustomTokenObtainPairSerializer

from .models import User
from .serializers import UserRegisterSerializer


class RegisterAPIView(generics.CreateAPIView):
    """Регистрация пользователя."""

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class LoginAPIView(TokenObtainPairView):
    """JWT авторизация пользователя."""

    serializer_class = CustomTokenObtainPairSerializer
