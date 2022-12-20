from django.urls import path

from .views import index
from .views import TaskCreateView, TaskListView, TaskUpdateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("tasks/", index, name="index"),
    path("tasks/critical/", TaskListView.as_view(), name="critical-task"),
    path("tasks/create/", TaskCreateView.as_view(), name="create-task"),
    path("tasks/<int:pk>/update", TaskUpdateView.as_view(), name="update-task"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

app_name = "app"
