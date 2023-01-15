from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from app.models import Task, Worker, Position, TaskType
from users.models import Profile


@admin.register(Task)
class AdminTask(admin.ModelAdmin):
    """
    Register class for model Task to admin page. In this class
    add a several custom fields to list_display and list_filter
    """

    list_display = ["is_completed", "name", "deadline", "task_type", "priority", "assignees", "created_date"]
    list_filter = ("assignees", "priority", "task_type",)
    search_fields = ["name"]


@admin.register(Worker)
class AdminWorker(UserAdmin):
    """
    Register class for model Worker to admin page. In this class
    add one custom field to list_display and add custom 'Additional info'
    area with field 'position'
    """

    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (("Additional info", {"fields": ("position",)}),)


@admin.register(Position)
class AdminPosition(admin.ModelAdmin):
    """Register class for model Position to admin page."""

    pass


@admin.register(TaskType)
class AdminTaskType(admin.ModelAdmin):
    """Register class for model TaskType to admin page."""

    pass


@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    """Register class for model Profile to admin page."""

    pass
