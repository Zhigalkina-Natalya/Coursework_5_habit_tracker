from rest_framework import serializers

from habits.models import Habit
from habits.validators import HabitValidator


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор привычки."""

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("owner",)

        validators = [HabitValidator()]

    def validate(self, attrs):
        """Дополнительная проверка."""
        instance = self.instance
        related = attrs.get("related_habit")

        if instance and related == instance:
            raise serializers.ValidationError("Привычка не может ссылаться сама на себя")

        return attrs


class PublicHabitSerializer(serializers.ModelSerializer):
    """Сериализатор публичных привычек (без owner)."""
    class Meta:
        model = Habit
        exclude = ("owner", "last_run")
