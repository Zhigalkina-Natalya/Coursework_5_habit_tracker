from datetime import time

from rest_framework import serializers


class HabitValidator:
    """Комплексная проверка привычки."""

    def __call__(self, attrs):

        reward = attrs.get("reward")
        related = attrs.get("related_habit")
        execution_time = attrs.get("execution_time")
        periodicity = attrs.get("periodicity")
        is_pleasant = attrs.get("is_pleasant")

        # нельзя одновременно reward и related
        if reward and related:
            raise serializers.ValidationError("Нельзя одновременно указывать вознаграждение и связанную привычку.")

        # время выполнения
        if execution_time is None:
            raise serializers.ValidationError("Укажите время выполнения.")

        if execution_time == time(0, 0, 0):
            raise serializers.ValidationError("Время выполнения не может быть 0.")

        if execution_time is not None and execution_time > time(hour=0, minute=2):
            raise serializers.ValidationError("Время выполнения привычки должно быть не больше 120 секунд.")

        # периодичность
        if periodicity is None:
            raise serializers.ValidationError("Укажите периодичность.")

        if periodicity is not None:
            if periodicity < 1:
                raise serializers.ValidationError("Периодичность должна быть не меньше 1 дня.")

            if periodicity > 7:
                raise serializers.ValidationError("Нельзя выполнять привычку реже, чем раз в 7 дней.")

        # связанная привычка должна быть приятной
        if related and not related.is_pleasant:
            raise serializers.ValidationError("Связанной может быть только приятная привычка.")

        # приятная привычка не может иметь reward или related
        if is_pleasant and (reward or related):
            raise serializers.ValidationError("Приятная привычка не может иметь награду или связанную привычку.")
