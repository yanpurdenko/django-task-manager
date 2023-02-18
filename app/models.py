from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Position(models.Model):
    POSITION_CHOICES = (
        ("Developer", "Developer"),
        ("Project manager", "Project Manager"),
        ("Designer", "Designer"),
        ("Devops", "DevOps"),
        ("QA", "QA"),
    )

    name = models.CharField(max_length=255, choices=POSITION_CHOICES)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class TaskType(models.Model):
    TASK_TYPE_CHOICES = (
        ("Bug", "Bug"),
        ("New Feature", "New Feature"),
        ("Refactoring", "Refactoring"),
        ("QA", "QA"),
    )

    name = models.CharField(
        max_length=255, choices=TASK_TYPE_CHOICES
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position, on_delete=models.CASCADE, related_name="workers", null=True, blank=True
    )

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("app:worker-detail", kwargs={"pk": self.pk})


class Task(models.Model):
    PRIORITY_CHOICES = (
        ("Critical", "Critical"),
        ("Important", "Important"),
        ("Normal", "Normal"),
        ("Low", "Low"),
    )

    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True
    )
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=9, choices=PRIORITY_CHOICES, blank=False, null=False
    )
    task_type = models.ForeignKey(
        TaskType, on_delete=models.CASCADE, related_name="task_types", blank=False, null=False
    )
    assignee = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name="tasks")
    created_date = models.DateField(auto_now_add=True, blank=False, null=False)

    class Meta:
        verbose_name = "task"
        verbose_name_plural = "tasks"
        ordering = ["created_date"]

    def __str__(self):
        return self.name
