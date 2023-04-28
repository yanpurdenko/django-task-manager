import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from app.models import Position, Task

INDEX_VIEW_URL = reverse("app:index")
PRIORITY_TASK_VIEW_URL = reverse("app:priority-tasks")
TODAY_TASK_VIEW_URL = reverse("app:today-task")
MY_TASK_VIEW_URL = reverse("app:my-task")


class PublicTasksListViewTests(TestCase):
    """Testing accessibility of pages for non-login users."""

    def setUp(self) -> None:
        self.client = Client()

    def test_index_login_required(self):
        response = self.client.get(INDEX_VIEW_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_priority_task_list_view_login_required(self):
        response = self.client.get(PRIORITY_TASK_VIEW_URL)

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

    def test_retrieve_critical_priority_task_page(self):
        response = self.client.get(PRIORITY_TASK_VIEW_URL + "?priority=critical")

        queryset = Task.objects.filter(
            priority="Critical", assignee=self.user, is_completed=False
        ).select_related()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["queryset"]), list(queryset))
        self.assertTemplateUsed(response, "app/priority_tasks_list.html")

    def test_retrieve_important_priority_task_page(self):
        response = self.client.get(PRIORITY_TASK_VIEW_URL + "?priority=important")

        queryset = Task.objects.filter(
            priority="Important", assignee=self.user, is_completed=False
        ).select_related()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["queryset"]), list(queryset))
        self.assertTemplateUsed(response, "app/priority_tasks_list.html")

    def test_retrieve_normal_priority_task_page(self):
        response = self.client.get(PRIORITY_TASK_VIEW_URL + "?priority=normal")

        queryset = Task.objects.filter(
            priority="Normal", assignee=self.user, is_completed=False
        ).select_related()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["queryset"]), list(queryset))
        self.assertTemplateUsed(response, "app/priority_tasks_list.html")

    def test_retrieve_low_priority_task_page(self):
        response = self.client.get(PRIORITY_TASK_VIEW_URL + "?priority=low")

        queryset = Task.objects.filter(
            priority="Low", assignee=self.user, is_completed=False
        ).select_related()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["queryset"]), list(queryset))
        self.assertTemplateUsed(response, "app/priority_tasks_list.html")

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
