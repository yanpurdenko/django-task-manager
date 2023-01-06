from django.urls import path

from .views import (
    profile_view,
    update_profile_view,
    WorkersListView,
    ChangePasswordView,
    WorkerProfileDetailView,
)

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("user/profile/", profile_view, name="profile"),
    path("user/profile/<int:pk>", WorkerProfileDetailView.as_view(), name="worker-profile-detail"),
    path("user/profile/update/", update_profile_view, name="update-profile"),
    path("tasks/workers-profile/", WorkersListView.as_view(), name="workers-profiles"),
    path("tasks/password-change/", ChangePasswordView.as_view(), name="password-change"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

app_name = "users"
