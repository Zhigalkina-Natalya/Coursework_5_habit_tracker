# Курсовая работа №5 Трекер привычек


## Описание проекта

Backend-часть SPA-приложения для отслеживания полезных привычек.

Проект реализован на Django REST Framework с использованием:

  - JWT авторизации
  - Celery для фоновых задач
  - Telegram для отправки напоминаний

---

## Структура

  - `config/` - настройки проекта
  - `habits/` - приложение привычек
  - `telegram_bot/` - приложение телеграм_бот
  - `users/` - приложение пользователей
  - `manage.py` - Django management

---

## Установка и настройка

1. Клонировать репозиторий

```
https://github.com/Zhigalkina-Natalya/Coursework_5_habit_tracker
```

2. Установите зависимости проекта

```
poetry install
```
или, если вы используете pip:
```
pip install -r requirements.txt
```

3. Настройте базу данных PostgreSQL

```
Убедитесь, что у вас установлен и запущен сервер PostgreSQL.
```

4. Создать `.env` по образцу: `.env.sample`
Пример файла `.env.sample` находится в репозитории.

**Переменные окружения (.env)**
```
SECRET_KEY=your_secret_key
DEBUG=True

NAME=postgres
USER=postgres
PASSWORD=postgres
HOST=localhost  
PORT=5432

TELEGRAM_TOKEN=your_token

CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

5. Применить миграции:

```
python manage.py migrate
```

6. Создать суперпользователя:

```
python manage.py createadmin
```

7. Запустить сервер:

```
python manage.py runserver
```

8. Использование:

   - Интерфейс: http://127.0.0.1:8000/
   - Админ: http://127.0.0.1:8000/admin/

9. Проверка Celery

```
celery -A config inspect active
```

10. Запуск Celery

```
celery -A config worker -l info
```

11. Запуск Celery Beat

```
celery -A config beat -l info
```

12. Запуск Redis
```
redis-server
```
13. Swagger
```
http://127.0.0.1:8000/api/docs/swagger/
```

---

## Функциональность

**Пользователи**

- Регистрация
  - Авторизация (JWT)
  - Обновление токена

**Привычки**

- Создание привычки
  - Редактирование
  - Удаление
  - Просмотр списка своих привычек
  - Просмотр публичных привычек

**Напоминания**

- Отправка уведомлений в Telegram
  - Использование Celery и Redis

---

## Логика привычек
Привычка включает:

- место выполнения
  - время
  - действие
  - вознаграждение или связанную привычку
  - периодичность (не реже 1 раза в 7 дней)
  - время выполнения (до 120 секунд)

---

## Telegram

1. Создать бота через BotFather
2. Получить токен
3. Написать боту в Telegram
4. Получить chat_id

---

## Примеры API

Регистрация
```
POST http://127.0.0.1:8000/api/users/register/

Body:

{
  "email": "test@test.com",
  "password": "123456",
  "telegram_chat_id": "123456789"
}
```
Авторизация
```
POST http://127.0.0.1:8000/api/users/login/
```

### Авторизация

Все защищённые эндпоинты требуют заголовок:
```
Authorization: Bearer <access_token>
```

### Обновление токена
```
POST http://127.0.0.1:8000/api/users/token/refresh/

Body:
{
  "refresh": "<refresh_token>"
}
```

### Пример создания привычки

```
POST http://127.0.0.1:8000/api/habits/create/

Headers:
Authorization: Bearer <access_token>

Body:
{
  "place": "Дом",
  "time": "08:00",
  "action": "Выпить воду",
  "execution_time": 60,
  "periodicity": 1,
  "is_public": true
}
```

### Публичные привычки
```
GET http://127.0.0.1:8000/api/habits/public/
```
Доступ без авторизации.

Позволяет смотреть привычки других пользователей и использовать их как пример.

### Пагинация
```
GET /api/habits/?page=1

- page_size по умолчанию: 5
- max_page_size: 10
```

### Проверка работы уведомлений

1. Убедитесь, что Redis запущен
2. Запустите Celery worker
3. Запустите Celery beat
4. Создайте привычку с текущим временем
5. Дождитесь выполнения задачи (каждую минуту)

Логи:
- Celery задача напоминаний запущена
- Найдено привычек: 1
- Отправка...

---

## Безопасность (CORS)

Для подключения фронтенда необходимо настроить CORS:
```
CORS_ALLOWED_ORIGINS = [
    '<http://localhost:8000>',  # Замените на адрес вашего фронтенд-сервера
]

CSRF_TRUSTED_ORIGINS = [
    "https://read-and-write.example.com", #  Замените на адрес вашего фронтенд-сервера и добавьте адрес бэкенд-сервера
]

CORS_ALLOW_ALL_ORIGINS = False

```

---

## Логирование

Проект использует встроенный logging Django:

- Логи пишутся в файл `logs/app.log`
- Также выводятся в консоль
- Используется уровень INFO

Пример логов:
```
[2026-03-24 12:34:00] INFO telegram_bot.tasks: Найдено привычек: 2
[2026-03-24 12:34:00] INFO telegram_bot.tasks: Отправка habit_id=23 пользователю test@test.com
```

---

## Тестирование

```
coverage run manage.py test
coverage report
```

---

## Технологии

  - Python 3.13
  - Django
  - Django REST Framework
  - PostgreSQL
  - Redis
  - Celery
  - SimpleJWT
  - drf-spectacular

---

Автор

Наталья Жигалкина