from django.test import TestCase
from rest_framework.test import APIClient

from users.models import User


class UserTestCase(TestCase):
    """Тесты пользователей."""

    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        """Тест регистрации."""

        response = self.client.post("/api/users/register/", {"email": "new@mail.com", "password": "123456"})

        self.assertEqual(response.status_code, 201)

    def test_user_login(self):
        """Тест JWT авторизации."""

        User.objects.create_user(email="test@test.com", password="123456")

        response = self.client.post("/api/users/login/", {"email": "test@test.com", "password": "123456"})

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_user_registration_duplicate(self):
        """Ошибка при регистрации с уже существующим email."""

        self.client.post("/api/users/register/", {"email": "test@test.com", "password": "123456"})

        response = self.client.post("/api/users/register/", {"email": "test@test.com", "password": "123456"})

        self.assertEqual(response.status_code, 400)

    def test_user_login_invalid_password(self):
        """Ошибка при неверном пароле."""

        User.objects.create_user(email="test@test.com", password="123456")

        response = self.client.post("/api/users/login/", {"email": "test@test.com", "password": "wrong"})

        self.assertEqual(response.status_code, 401)

    def test_user_login_invalid_email(self):
        """Ошибка при несуществующем пользователе."""

        response = self.client.post("/api/users/login/", {"email": "wrong@mail.com", "password": "123456"})

        self.assertEqual(response.status_code, 401)

    def test_token_refresh(self):
        """Проверка обновления access токена."""

        User.objects.create_user(email="test@test.com", password="123456")

        # получаем токены
        response = self.client.post("/api/users/login/", {"email": "test@test.com", "password": "123456"})
        refresh = response.data["refresh"]

        # обновляем access
        response = self.client.post("/api/users/token/refresh/", {"refresh": refresh})

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)

    def test_token_refresh_invalid(self):
        """Ошибка при неверном refresh токене."""

        response = self.client.post("/api/users/token/refresh/", {"refresh": "invalid_token"})

        self.assertEqual(response.status_code, 401)
