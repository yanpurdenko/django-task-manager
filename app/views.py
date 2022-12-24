import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.views.generic import ListView

from app.forms import WorkerCreationForm, AllTasksSearchForm
from app.models import Task, Worker, TaskType, Position


@login_required
def index(request):
    """View function for the home page of the site."""

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "all_tasks": Task.objects.all().select_related(),
        "all_priorities": [priority[1] for priority in Task.PRIORITY_CHOICES],
        "all_workers_without_user": Worker.objects.exclude(first_name=request.user.first_name).select_related(),
        "all_task_types": TaskType.objects.all(),
        "search_form": AllTasksSearchForm()
    }

    return render(request, "app/index.html", context=context)


class CriticalTaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "app/critical-task-list.html"

    def get(self, request, *args, **kwargs):
        context = {
            "all_critical_tasks": Task.objects.filter(priority="Critical", assignees=request.user).select_related()
        }

        return render(request, self.template_name, context=context)

    def get_queryset(self):
        name = self.request.GET.get("name")

        if name:
            return self.queryset.filter(name__icontains=name)

        return self.queryset


class ImportantTaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "app/important-task-list.html"

    def get(self, request, *args, **kwargs):
        context = {
            "all_important_tasks": Task.objects.filter(priority="Important", assignees=request.user).select_related()
        }

        return render(request, self.template_name, context=context)


class NormalTaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "app/normal-task-list.html"

    def get(self, request, *args, **kwargs):
        context = {
            "all_normal_tasks": Task.objects.filter(priority="Normal", assignees=request.user).select_related()
        }

        return render(request, self.template_name, context=context)


class LowTaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "app/low-task-list.html"

    def get(self, request, *args, **kwargs):
        context = {
            "all_critical_tasks": Task.objects.filter(priority="Low", assignees=request.user).select_related()
        }

        return render(request, self.template_name, context=context)


class TodayTaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "app/today-task-list.html"

    def get(self, request, *args, **kwargs):
        context = {
            "today_tasks": Task.objects.filter(
                deadline=datetime.date.today(), assignees=request.user
            ).select_related()
        }

        return render(request, self.template_name, context=context)


class MyTaskListView(LoginRequiredMixin, ListView):
    template_name = "app/my-task-list.html"

    def get(self, request, *args, **kwargs):
        context = {
            "my_tasks": Task.objects.filter(assignees=request.user)
        }

        return render(request, self.template_name, context=context)

    def get_queryset(self):
        name = self.request.GET.get("name")

        if name:
            return self.queryset.filter(name__icontains=name)

        return self.queryset


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    fields = ["name", "description", "deadline", "priority", "task_type", "assignees"]
    template_name = "app/task_form.html"
    success_url = reverse_lazy("app:index")

    def get_context_data(self, **kwargs):
        context = super(TaskCreateView, self).get_context_data(**kwargs)
        all_priorities = [priority[1] for priority in Task.PRIORITY_CHOICES]
        all_workers = Worker.objects.all()
        all_task_types = TaskType.objects.all()

        context["priorities"] = all_priorities
        context["all_workers"] = all_workers
        context["all_task_types"] = all_task_types

        return context


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = ["name", "description", "deadline", "priority", "task_type", "assignees"]
    success_url = reverse_lazy("app:index")

    def get_context_data(self, **kwargs):
        context = super(TaskUpdateView, self).get_context_data(**kwargs)
        all_priorities = [priority[1] for priority in Task.PRIORITY_CHOICES]
        all_workers = Worker.objects.all()
        all_task_types = TaskType.objects.all()

        context["priorities"] = all_priorities
        context["all_workers"] = all_workers
        context["all_task_types"] = all_task_types

        return context


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("app:index")


class WorkerCreateView(generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    template_name = "registration/sign-up.html"
    success_url = reverse_lazy("app:index")

    def get_context_data(self, **kwargs):
        context = super(WorkerCreateView, self).get_context_data(**kwargs)
        positions = Position.objects.all()

        context["positions"] = positions

        return context
