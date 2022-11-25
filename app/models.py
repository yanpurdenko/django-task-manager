from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    POSITION_CHOICES = (
        ("developer", "Developer"),
        ("pm", "Project Manager"),
        ("designer", "Designer"),
        ("devops", "DevOps"),
        ("qa", "QA"),
    )

    name = models.CharField(max_length=255, choices=POSITION_CHOICES)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class TaskType(models.Model):
    TASK_TYPE_CHOICES = (
        ("bug", "bug"),
        ("new_feature", "new feature"),
        ("refactoring", "refactoring"),
        ("QA", "QA"),
    )

    name = models.CharField(
        max_length=255, choices=TASK_TYPE_CHOICES, blank=True, null=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position, on_delete=models.SET_NULL, related_name="workers", null=True
    )

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def __str__(self):
        return (
            f"{self.username} (position: {self.position}, "
            f"name: {self.first_name} {self.last_name})"
        )


class Task(models.Model):
    PRIORITY_CHOICES = (
        ("critical", "Critical"),
        ("important", "Important"),
        ("normal", "Normal"),
        ("low", "Low"),
    )

    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField(
        auto_now=False, auto_now_add=False, blank=True, null=True
    )
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=9, choices=PRIORITY_CHOICES)
    task_type = models.ForeignKey(
        TaskType, on_delete=models.SET_NULL, related_name="tasks", null=True
    )
    assignees = models.ManyToManyField(Worker, related_name="assignees")

    class Meta:
        verbose_name = "task"
        verbose_name_plural = "tasks"

    def __str__(self):
        return self.name
