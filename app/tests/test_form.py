import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from app.forms import WorkerCreationForm, CreateTaskForm, UpdateTaskForm
from app.models import Position, TaskType


class FormsTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.task_type = TaskType.objects.create(name="test")
        self.worker = get_user_model().objects.create_user(
            username="test1",
            password="123098Qwe",
            first_name="Test first",
            last_name="Test last",
            position=Position.objects.create(name="Develop")
        )
        self.client.force_login(self.worker)

    def test_worker_creation_form_with_email_first_name_last_name_position_is_valid(self):
        """Testing validity of WorkerCreationForm with additional fields(email, first_name, last_name, position)."""

        form_data = {
            "username": "test",
            "password1": "123098Qwe",
            "password2": "123098Qwe",
            "email": "test@test.com",
            "first_name": "Test first",
            "last_name": "Test last",
            "position": Position.objects.create(name="Develop")
        }
        form = WorkerCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_task_creation_form_is_valid(self):
        """Testing validity of CreateTaskForm"""

        form_data = {
            "name": "test",
            "description": "",
            "deadline": datetime.date.today(),
            "priority": "Critical",
            "task_type": self.task_type,
            "assignees": self.worker
        }
        task_form = CreateTaskForm(data=form_data)

        self.assertTrue(task_form.is_valid())
        self.assertEqual(task_form.cleaned_data, form_data)

    def test_task_update_form_is_valid(self):
        """Testing validity of UpdateTaskForm"""

        form_data = {
            "name": "test",
            "description": "",
            "deadline": datetime.date.today(),
            "priority": "Critical",
            "task_type": self.task_type,
            "assignees": self.worker
        }
        task_form = UpdateTaskForm(data=form_data)

        self.assertTrue(task_form.is_valid())
        self.assertEqual(task_form.cleaned_data, form_data)

