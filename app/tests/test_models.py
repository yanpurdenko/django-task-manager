from unittest import TestCase

from django.contrib.auth import get_user_model

from app.models import Position, TaskType, Task


class ModelsTests(TestCase):
    def test_position_str(self):
        """Testing str method in model Position."""

        position = Position.objects.create(name="test")

        self.assertEqual(str(position), position.name)

    def test_worker_str(self):
        """Testing str method in model Worker."""

        worker = get_user_model().objects.create_user(
            username="test",
            password="123098Qwe",
            first_name="Test first",
            last_name="Test last",
        )

        self.assertEqual(str(worker), f"{worker.first_name} {worker.last_name}")

    def test_task_str(self):
        """Testing str method in model Task."""

        task_type = TaskType.objects.create(name="test")
        worker = get_user_model().objects.create_user(
            username="test1",
            password="123098Qwe",
            first_name="Test first",
            last_name="Test last",
        )
        task = Task.objects.create(
            name="test",
            deadline="2023-01-23",
            priority="test",
            task_type=task_type,
            assignee=worker
        )

        self.assertEqual(str(task), task.name)

    def test_task_type_str(self):
        """Testing str method in model TaskType."""

        task_type = TaskType.objects.create(name="Bug")

        self.assertEqual(str(task_type.name), task_type.name)
