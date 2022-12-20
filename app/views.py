from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render

from app.models import Task, Worker, TaskType


@login_required
def index(request):
    """View function for the home page of the site."""

    all_tasks = Task.objects.all().prefetch_related()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "all_tasks": all_tasks
    }

    return render(request, "app/index.html", context=context)


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    fields = ["name", "description", "deadline", "priority", "task_type", "assignees"]
    template_name = "app/create_task_form.html"
    success_url = reverse_lazy("app:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        priorities = Task.PRIORITY_CHOICES

        context["priorities"] = [priority[1] for priority in priorities]
        context["all_workers"] = Worker.objects.all()
        context["all_task_types"] = TaskType.objects.all()
        return context


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "app/critical-tasks-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # user = self.request.user

        context["all_critical_tasks"] = Task.objects.filter(priority="Critical").prefetch_related()
        return context


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("app:index")
