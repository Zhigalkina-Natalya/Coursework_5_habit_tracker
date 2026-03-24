from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from habits.models import Habit

User = get_user_model()


class BaseTestCase(TestCase):
    """Базовый класс тестов."""

    def setUp(self):
        """Создание пользователя и клиента."""

        self.client = APIClient()
        self.user = User.objects.create_user(email="test1@test.com", password="123456")
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")


class HabitTestCase(BaseTestCase):
    """Тесты привычек."""

    def test_create_habit(self):
        """Создание привычки."""

        response = self.client.post(
            "/api/habits/create/",
            {"place": "Дом", "time": "08:00", "action": "Вода", "execution_time": 60, "periodicity": 1},
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Habit.objects.count(), 1)

    def test_habit_list(self):
        """Получение списка привычек."""

        Habit.objects.create(owner=self.user, place="Дом", time="08:00", action="Тест", execution_time=60)
        response = self.client.get("/api/habits/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)

    def test_public_habits(self):
        """Публичные привычки."""

        Habit.objects.create(
            owner=self.user, place="Дом", time="08:00", action="Публичная", execution_time=60, is_public=True
        )
        response = self.client.get("/api/habits/public/")
        self.assertEqual(response.status_code, 200)

    def test_delete_habit(self):
        """Удаление привычки."""

        habit = Habit.objects.create(owner=self.user, place="Дом", time="08:00", action="Удалить", execution_time=60)
        response = self.client.delete(f"/api/habits/{habit.id}/delete/")
        self.assertEqual(response.status_code, 204)

    def test_permission_denied(self):
        """Нельзя редактировать чужую привычку."""

        User = get_user_model()

        other_user = User.objects.create_user(email="other@test.com", password="123456")
        habit = Habit.objects.create(owner=other_user, place="Дом", time="08:00", action="Чужая", execution_time=60)
        response = self.client.patch(f"/api/habits/{habit.id}/update/", {"action": "Новое"})
        self.assertEqual(response.status_code, 403)

    def test_execution_time_none_error(self):
        """Ошибка если execution_time не указан."""

        response = self.client.post(
            "/api/habits/create/",
            {
                "place": "Дом",
                "time": "08:00",
                "action": "Ошибка",
                "periodicity": 1,
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_execution_time_limit(self):
        """Время выполнения не больше 120 сек."""

        response = self.client.post(
            "/api/habits/create/",
            {"place": "Дом", "time": "08:00:00", "action": "Ошибка", "execution_time": 200, "periodicity": 1},
        )
        self.assertEqual(response.status_code, 400)

    def test_reward_and_related_error(self):
        """Нельзя одновременно указывать reward и related_habit."""
        habit = Habit.objects.create(owner=self.user, place="Дом", time="08:00", action="test", execution_time=60)

        response = self.client.post(
            "/api/habits/create/",
            {
                "place": "Дом",
                "time": "08:00",
                "action": "Ошибка",
                "execution_time": 60,
                "reward": "конфета",
                "related_habit": habit.id,
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_related_must_be_pleasant(self):
        """Связанная привычка должна быть приятной."""

        bad_habit = Habit.objects.create(
            owner=self.user,
            place="Дом",
            time="08:00",
            action="Плохая",
            execution_time=60,
            is_pleasant=False,
        )

        response = self.client.post(
            "/api/habits/create/",
            {
                "place": "Дом",
                "time": "08:00",
                "action": "Ошибка",
                "execution_time": 60,
                "related_habit": bad_habit.id,
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_pagination(self):
        """Проверка пагинации — не более 5 привычек на страницу."""

        for i in range(7):
            Habit.objects.create(owner=self.user, place="Дом", time="08:00", action=f"test {i}", execution_time=60)

        response = self.client.get("/api/habits/")
        self.assertEqual(len(response.data["results"]), 5)

    def test_execution_time_zero_error(self):
        """Ошибка если execution_time = 0."""

        response = self.client.post(
            "/api/habits/create/",
            {"place": "Дом", "time": "08:00", "action": "Ошибка", "execution_time": 0, "periodicity": 1},
        )
        self.assertEqual(response.status_code, 400)

    def test_periodicity_none_error(self):
        """Ошибка если periodicity не указана."""

        response = self.client.post(
            "/api/habits/create/",
            {
                "place": "Дом",
                "time": "08:00",
                "action": "Ошибка",
                "execution_time": 60,
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_periodicity_limit_error(self):
        """Ошибка если periodicity > 7."""

        response = self.client.post(
            "/api/habits/create/",
            {"place": "Дом", "time": "08:00", "action": "Ошибка", "execution_time": 60, "periodicity": 10},
        )
        self.assertEqual(response.status_code, 400)

    def test_periodicity_zero_error(self):
        """Ошибка если periodicity < 1."""

        response = self.client.post(
            "/api/habits/create/",
            {"place": "Дом", "time": "08:00", "action": "Ошибка", "execution_time": 60, "periodicity": 0},
        )
        self.assertEqual(response.status_code, 400)

    def test_pleasant_habit_restrictions(self):
        """Приятная привычка не может иметь reward или related."""

        response = self.client.post(
            "/api/habits/create/",
            {
                "place": "Дом",
                "time": "08:00",
                "action": "Ошибка",
                "execution_time": 60,
                "periodicity": 1,
                "is_pleasant": True,
                "reward": "конфета",
            },
        )
        self.assertEqual(response.status_code, 400)
