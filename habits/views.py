from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.pagination import HabitPagination
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer, PublicHabitSerializer


class HabitListAPIView(generics.ListAPIView):
    """Список привычек текущего пользователя."""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Habit.objects.none()

        return Habit.objects.filter(owner=self.request.user)


class PublicHabitListAPIView(generics.ListAPIView):
    """Список публичных привычек."""

    serializer_class = PublicHabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Habit.objects.none()
        return Habit.objects.filter(is_public=True)


class HabitCreateAPIView(generics.CreateAPIView):
    """Создание новой привычки."""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Привязывает привычку к пользователю."""
        serializer.save(owner=self.request.user)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Просмотр привычки."""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    queryset = Habit.objects.all()


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Редактирование привычки."""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    queryset = Habit.objects.all()


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Удаление привычки."""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    queryset = Habit.objects.all()
