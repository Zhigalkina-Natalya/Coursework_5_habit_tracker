from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Менеджер пользователя с авторизацией по email."""

    def create_user(self, email, password=None, **extra_fields):
        """Создание обычного пользователя."""

        if not email:
            raise ValueError("Email обязателен")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создание суперпользователя."""

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Кастомный пользователь системы с уникальным email"""

    username = None

    email = models.EmailField(unique=True, verbose_name="Email", help_text="Укажите электронную почту пользователя")

    objects = UserManager()

    telegram_chat_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="ID чата Telegram",
        help_text="ID Telegram-чата для отправки напоминаний",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]

    def __str__(self):
        """Строковое представление пользователя."""
        return self.email
