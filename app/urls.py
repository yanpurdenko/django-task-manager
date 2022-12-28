from django.urls import path

from .views import index
from .views import (
    TaskCreateView,
    CriticalTaskListView,
    ImportantTaskListView,
    NormalTaskListView,
    LowTaskListView,
    TaskUpdateView,
    TaskDeleteView,
    TodayTaskListView,
    WorkerCreateView,
    MyTaskListView,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("tasks/", index, name="index"),
    path("tasks/critical/", CriticalTaskListView.as_view(), name="critical-task"),
    path("tasks/important/", ImportantTaskListView.as_view(), name="important-task"),
    path("tasks/normal/", NormalTaskListView.as_view(), name="normal-task"),
    path("tasks/today/", TodayTaskListView.as_view(), name="today-task"),
    path("tasks/low/", LowTaskListView.as_view(), name="low-task"),
    path("tasks/my/", MyTaskListView.as_view(), name="my-task"),
    path("tasks/create/", TaskCreateView.as_view(), name="create-task"),
    path("tasks/<int:pk>/update", TaskUpdateView.as_view(), name="update-task"),
    path("tasks/<int:pk>/delete", TaskDeleteView.as_view(), name="delete-task"),
    path("tasks/create", WorkerCreateView.as_view(), name="create-worker"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

app_name = "app"
