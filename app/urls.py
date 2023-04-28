from django.urls import path

from .views import (
    index,
    TaskCreateView,
    PriorityTaskListView,
    TaskUpdateView,
    TaskDeleteView,
    TodayTaskListView,
    WorkerCreateView,
    MyTaskListView,
    complete_task,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", index, name="index"),
    path("tasks/priority/", PriorityTaskListView.as_view(), name="priority-tasks"),
    path("tasks/today/", TodayTaskListView.as_view(), name="today-task"),
    path("tasks/my/", MyTaskListView.as_view(), name="my-task"),
    path("tasks/create/", TaskCreateView.as_view(), name="create-task"),
    path("tasks/<int:pk>/complete", complete_task, name="complete-task"),
    path("tasks/<int:pk>/update", TaskUpdateView.as_view(), name="update-task"),
    path("tasks/<int:pk>/delete", TaskDeleteView.as_view(), name="delete-task"),
    path("tasks/create", WorkerCreateView.as_view(), name="create-worker"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

app_name = "app"
