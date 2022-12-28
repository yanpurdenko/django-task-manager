from django.urls import path

from .views import profile_view, update_profile_view, workers_profiles_list_view

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("user/profile/", profile_view, name="profile"),
    path("user/profile/update/", update_profile_view, name="update-profile"),
    path("tasks/workers-profile/", workers_profiles_list_view, name="workers-profiles"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

app_name = "users"
