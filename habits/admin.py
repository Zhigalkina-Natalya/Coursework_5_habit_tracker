from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """Администрирование привычек."""

    list_display = ("id", "action", "owner", "time", "is_pleasant", "is_public")
    list_filter = ("is_pleasant", "is_public")
    search_fields = ("action", "place")
    list_display_links = ("id", "action")
