import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render

from app.forms import WorkerCreationForm, CreateTaskForm, UpdateTaskForm
from app.models import Task, Worker


@login_required
def complete_task(request, pk):
    """Function for the home page of the site."""

    queryset = Task.objects.filter(is_completed=False).select_related()
    task = Task.objects.get(id=pk)
    task.is_completed = True
    task.save()

    if "tasks" in request.headers["Referer"]:
        queryset = Task.objects.filter(is_completed=False).select_related()

    if "critical" in request.headers["Referer"]:
        queryset = Task.objects.filter(
            priority="Critical", assignee=request.user, is_completed=False
        ).select_related()

    if "important" in request.headers["Referer"]:
        queryset = Task.objects.filter(
            priority="Important", assignee=request.user, is_completed=False
        ).select_related()

    if "normal" in request.headers["Referer"]:
        queryset = Task.objects.filter(
            priority="Normal", assignee=request.user, is_completed=False
        ).select_related()

    if "low" in request.headers["Referer"]:
        queryset = Task.objects.filter(
            priority="Low", assignee=request.user, is_completed=False
        ).select_related()

    if "today" in request.headers["Referer"]:
        queryset = Task.objects.filter(
            deadline=datetime.date.today(), assignee=request.user, is_completed=False
        ).select_related()

    if "my" in request.headers["Referer"]:
        queryset = Task.objects.filter(assignee=request.user, is_completed=False).select_related()

    context = {
        "tasks": queryset,
        "today_date": datetime.date.today()
    }

    return render(request, "app/complete_task.html", context=context)


@login_required
def index(request):
    """View function for the home page of the site."""

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    queryset = Task.objects.filter(is_completed=False).select_related()
    today_date = datetime.date.today()

    if request.GET.get("name") is not None:
        queryset = queryset.filter(name__icontains=request.GET["name"], is_completed=False)

    context = {"tasks": queryset, "today_date": today_date}

    return render(request, "app/index.html", context=context)


class PriorityTaskListView(LoginRequiredMixin, generic.ListView):
    """ListView class only for critical tasks."""

    model = Task
    template_name = "app/priority_tasks_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PriorityTaskListView, self).get_context_data(**kwargs)
        user = self.request.user
        queryset = Task.objects.filter(assignee=user, is_completed=False).select_related()
        priority = None

        if "critical" == self.request.GET["priority"]:
            queryset = Task.objects.filter(priority="Critical", assignee=user, is_completed=False).select_related()
            priority = "Critical"

        if "important" == self.request.GET["priority"]:
            queryset = Task.objects.filter(priority="Important", assignee=user, is_completed=False).select_related()
            priority = "Important"

        if "normal" == self.request.GET["priority"]:
            queryset = Task.objects.filter(priority="Normal", assignee=user, is_completed=False).select_related()
            priority = "Normal"

        if "low" == self.request.GET["priority"]:
            queryset = Task.objects.filter(priority="Low", assignee=user, is_completed=False).select_related()
            priority = "Low"

        if self.request.GET.get("name") is not None:
            queryset = queryset.filter(name__icontains=self.request.GET["name"], is_completed=False)

        context["queryset"] = queryset
        context["today_date"] = datetime.date.today()
        context["priority"] = priority

        return context


class TodayTaskListView(LoginRequiredMixin, generic.ListView):
    """ListView class only for tasks which deadline is today."""

    model = Task
    template_name = "app/today_task_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TodayTaskListView, self).get_context_data(**kwargs)
        user = self.request.user
        today_tasks = Task.objects.filter(
            deadline=datetime.date.today(), assignee=user, is_completed=False
        ).select_related()

        if self.request.GET.get("name") is not None:
            today_tasks = today_tasks.filter(name__icontains=self.request.GET["name"], is_completed=False)

        context["today_tasks"] = today_tasks

        return context


class MyTaskListView(LoginRequiredMixin, generic.ListView):
    """ListView class only for tasks where executor is current login user."""

    model = Task
    template_name = "app/my_task_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MyTaskListView, self).get_context_data(**kwargs)
        user = self.request.user
        my_tasks = Task.objects.filter(assignee=user, is_completed=False).select_related()

        if self.request.GET.get("name") is not None:
            my_tasks = my_tasks.filter(name__icontains=self.request.GET["name"], is_completed=False)

        context["my_tasks"] = my_tasks
        context["today_date"] = datetime.date.today()

        return context


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    """CreateView class for creating tasks."""

    model = Task
    form_class = CreateTaskForm
    template_name = "app/task_form.html"
    success_url = reverse_lazy("app:index")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    """UpdateView class for updating tasks."""
    model = Task
    form_class = UpdateTaskForm
    success_url = reverse_lazy("app:index")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    """DeleteView class for delete tasks."""

    model = Task
    success_url = reverse_lazy("app:index")


class WorkerCreateView(generic.CreateView):
    """CreateView class for sign up and create new users."""

    model = Worker
    form_class = WorkerCreationForm
    template_name = "registration/sign_up.html"
    success_url = reverse_lazy("app:index")
