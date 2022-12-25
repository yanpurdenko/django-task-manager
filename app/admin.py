from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from app.models import Task, Worker, Position, TaskType, Profile


@admin.register(Task)
class AdminTask(admin.ModelAdmin):
    list_display = ["name", "deadline", "is_completed", "priority"]
    list_filter = ("assignees", "priority", "task_type",)


@admin.register(Worker)
class AdminWorker(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)


@admin.register(Position)
class AdminPosition(admin.ModelAdmin):
    pass


@admin.register(TaskType)
class AdminTaskType(admin.ModelAdmin):
    pass


@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    pass
