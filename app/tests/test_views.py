import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from app.models import Position, Task

INDEX_VIEW_URL = reverse("app:index")
CRITICAL_TASK_VIEW_URL = reverse("app:critical-task")
IMPORTANT_TASK_VIEW_URL = reverse("app:important-task")
NORMAL_TASK_VIEW_URL = reverse("app:normal-task")
LOW_TASK_VIEW_URL = reverse("app:low-task")
TODAY_TASK_VIEW_URL = reverse("app:today-task")
MY_TASK_VIEW_URL = reverse("app:my-task")


class PublicTasksListViewTests(TestCase):
    """Testing accessibility of pages for non-login users."""

    def setUp(self) -> None:
        self.client = Client()

    def test_index_login_required(self):
        response = self.client.get(INDEX_VIEW_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_critical_task_list_view_login_required(self):
        response = self.client.get(CRITICAL_TASK_VIEW_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_important_task_list_view_login_required(self):
        response = self.client.get(IMPORTANT_TASK_VIEW_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_normal_task_list_view_login_required(self):
        response = self.client.get(NORMAL_TASK_VIEW_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_low_task_list_view_login_required(self):
        response = self.client.get(LOW_TASK_VIEW_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_today_task_list_view_login_required(self):
        response = self.client.get(TODAY_TASK_VIEW_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_my_task_list_view_login_required(self):
        response = self.client.get(MY_TASK_VIEW_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateTasksListViewTests(TestCase):
    """Testing accessibility of pages for logged users."""

    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create(
            username="test1",
            password="123098Qwe",
            email="test@test.com",
            first_name="Test first",
            last_name="Test last",
            position=Position.objects.create(name="Develop")
        )
        self.client.force_login(self.user)

    def test_retrieve_index_page(self):
        response = self.client.get(INDEX_VIEW_URL)
        tasks = Task.objects.filter(is_completed=False).select_related()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["tasks"]), list(tasks))
        self.assertTemplateUsed(response, "app/index.html")

    def test_retrieve_critical_task_page(self):
        response = self.client.get(CRITICAL_TASK_VIEW_URL)

        critical_tasks = Task.objects.filter(
            priority="Critical", assignee=self.user, is_completed=False
        ).select_related()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["critical_tasks"]), list(critical_tasks))
        self.assertTemplateUsed(response, "app/critical_task_list.html")

    def test_retrieve_important_task_page(self):
        response = self.client.get(IMPORTANT_TASK_VIEW_URL)

        important_tasks = Task.objects.filter(
            priority="Important", assignee=self.user, is_completed=False
        ).select_related()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["important_tasks"]), list(important_tasks))
        self.assertTemplateUsed(response, "app/important_task_list.html")

    def test_retrieve_normal_task_page(self):
        response = self.client.get(NORMAL_TASK_VIEW_URL)

        normal_tasks = Task.objects.filter(priority="Normal", assignee=self.user, is_completed=False).select_related()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["normal_tasks"]), list(normal_tasks))
        self.assertTemplateUsed(response, "app/normal_task_list.html")

    def test_retrieve_low_task_page(self):
        response = self.client.get(LOW_TASK_VIEW_URL)

        low_tasks = Task.objects.filter(priority="Low", assignee=self.user, is_completed=False).select_related()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["low_tasks"]), list(low_tasks))
        self.assertTemplateUsed(response, "app/low_task_list.html")

    def test_retrieve_today_task_page(self):
        response = self.client.get(TODAY_TASK_VIEW_URL)

        today_tasks = Task.objects.filter(
            deadline=datetime.date.today(), assignee=self.user, is_completed=False
        ).select_related()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["today_tasks"]), list(today_tasks))
        self.assertTemplateUsed(response, "app/today_task_list.html")

    def test_retrieve_my_task_page(self):
        response = self.client.get(MY_TASK_VIEW_URL)

        my_tasks = Task.objects.filter(assignee=self.user, is_completed=False).select_related()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["my_tasks"]), list(my_tasks))
        self.assertTemplateUsed(response, "app/my_task_list.html")
