from django.conf import settings
from django.db import models


class Habit(models.Model):
    """Модель привычки пользователя."""

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Пользователь",
        help_text="Пользователь, создавший привычку",
    )

    place = models.CharField(max_length=255, verbose_name="Место", help_text="Место выполнения привычки")

    time = models.TimeField(verbose_name="Время", help_text="Время выполнения привычки")

    action = models.CharField(max_length=255, verbose_name="Действие", help_text="Описание привычки")

    is_pleasant = models.BooleanField(
        default=False, verbose_name="Приятная привычка", help_text="Является ли привычка приятной"
    )

    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Связанная привычка",
        help_text="Приятная привычка, связанная с полезной",
        related_name="related_habits",
    )

    periodicity = models.PositiveIntegerField(
        default=1, verbose_name="Периодичность", help_text="Периодичность выполнения в днях"
    )

    last_run = models.DateField(null=True, blank=True, verbose_name="Дата последнего выполнения")

    reward = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Вознаграждение",
        help_text="Вознаграждение после выполнения привычки",
    )

    execution_time = models.PositiveIntegerField(
        verbose_name="Время выполнения", help_text="Время выполнения привычки в секундах"
    )

    is_public = models.BooleanField(
        default=False, verbose_name="Публичная привычка", help_text="Доступна ли привычка другим пользователям"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["-created_at"]

    def __str__(self):
        """Строковое представление привычки."""
        return f"{self.action} ({self.owner})"
