import logging
from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from telegram_bot.services import send_telegram_message

logger = logging.getLogger(__name__)


@shared_task
def send_habit_reminder():
    """Отправляет напоминания пользователям о выполнении привычек."""

    logger.info("Celery задача напоминаний запущена")

    now = timezone.localtime()
    start = now.replace(second=0, microsecond=0)
    end = start + timedelta(minutes=1)

    habits = Habit.objects.filter(time__range=(start.time(), end.time()))
    logger.info("Найдено привычек: %s", habits.count())

    today = now.date()

    for habit in habits:
        user = habit.owner

        if not user.telegram_chat_id:
            logger.warning("Нет chat_id у пользователя %s", user.email)
            continue

        if habit.last_run:
            delta_days = (today - habit.last_run).days
            if delta_days < habit.periodicity:
                logger.info(
                    "Пропуск habit_id=%s (прошло %s дней, нужно %s)",
                    habit.id,
                    delta_days,
                    habit.periodicity,
                )
                continue

        message = (
            f"Напоминание!\n"
            f"Действие: {habit.action}\n"
            f"Место: {habit.place}\n"
            f"Время: {habit.time.strftime('%H:%M')}"
        )

        logger.info("Отправка habit_id=%s пользователю %s", habit.id, user.email)

        send_telegram_message(user.telegram_chat_id, message)

        habit.last_run = today
        habit.save(update_fields=["last_run"])

        logger.info("Успешно отправлено habit_id=%s", habit.id)
