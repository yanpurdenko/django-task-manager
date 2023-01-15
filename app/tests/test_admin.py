from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from app.models import Position


class AdminSiteTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="test admin",
            password="123098AdminTest",
            email="admin@test.com",
            first_name="Test first",
            last_name="Test last",
            position=Position.objects.create(name="Develop")
        )
        self.client.force_login(self.admin_user)
        self.worker = get_user_model().objects.create_user(
            username="test",
            password="123098Qwe",
            email="test@test.com",
            first_name="Test first",
            last_name="Test last",
            position=Position.objects.create(name="Develop")
        )

    def test_worker_position_listed(self):
        """Testing the presence of the position field on list_display."""

        url = reverse("admin:app_worker_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.worker.position)

    def test_worker_detailed_position_listed(self):
        """Testing the presence of the position field in fieldsets on worker detail page."""

        url = reverse("admin:app_worker_change", args=[self.worker.id])
        response = self.client.get(url)

        self.assertContains(response, self.worker.position)
