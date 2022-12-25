import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.views.generic import ListView

from app.forms import WorkerCreationForm, TasksSearchForm
from app.models import Task, Worker, TaskType, Position


@login_required
def index(request):
    """View function for the home page of the site."""

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "tasks": Task.objects.all().select_related(),
        "priorities": [priority[1] for priority in Task.PRIORITY_CHOICES],
        "workers_without_user": Worker.objects.exclude(first_name=request.user.first_name).select_related(),
        "task_types": TaskType.objects.all(),
        "search_form": TasksSearchForm()
    }

    return render(request, "app/index.html", context=context)


class CriticalTaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "app/critical-task-list.html"
    queryset = Task.objects.all().select_related()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CriticalTaskListView, self).get_context_data(**kwargs)
        user = self.request.user

        context["critical_tasks"] = Task.objects.filter(priority="Critical", assignees=user).select_related()

        return context

    def get_queryset(self):
        name = self.request.GET.get("name")

        if name:
            return self.queryset.filter(name__icontains=name)

        return self.queryset


class ImportantTaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "app/important-task-list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ImportantTaskListView, self).get_context_data(**kwargs)
        user = self.request.user

        context["important_tasks"] = Task.objects.filter(priority="Important", assignees=user).select_related()

        return context


class NormalTaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "app/normal-task-list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NormalTaskListView, self).get_context_data(**kwargs)
        user = self.request.user

        context["normal_tasks"] = Task.objects.filter(priority="Normal", assignees=user).select_related()

        return context


class LowTaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "app/low-task-list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LowTaskListView, self).get_context_data(**kwargs)
        user = self.request.user

        context["low_tasks"] = Task.objects.filter(priority="Low", assignees=user).select_related()

        return context


class TodayTaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "app/today-task-list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TodayTaskListView, self).get_context_data(**kwargs)
        user = self.request.user

        context["today_tasks"] = Task.objects.filter(
            deadline=datetime.date.today(), assignees=user
        ).select_related()

        return context


class MyTaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "app/my-task-list.html"
    queryset = Task.objects.all().select_related()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MyTaskListView, self).get_context_data(**kwargs)
        user = self.request.user

        context["my_tasks"] = Task.objects.filter(assignees=user).select_related()
        context["search_form"] = TasksSearchForm()

        return context

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

        context["priorities"] = [priority[1] for priority in Task.PRIORITY_CHOICES]
        context["workers"] = Worker.objects.all()
        context["task_types"] = TaskType.objects.all()

        return context


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = ["name", "description", "deadline", "priority", "task_type", "assignees"]
    success_url = reverse_lazy("app:index")

    def get_context_data(self, **kwargs):
        context = super(TaskUpdateView, self).get_context_data(**kwargs)

        context["priorities"] = [priority[1] for priority in Task.PRIORITY_CHOICES]
        context["workers"] = Worker.objects.all()
        context["task_types"] = TaskType.objects.all().select_related()

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
        positions = Position.objects.all().select_related()

        context["positions"] = positions

        return context


@login_required()
def profile_view(request):
    worker = Worker.objects.get(id=request.user.id)

    context = {
        "worker": worker
    }

    return render(request, "app/profile.html", context=context)

# @login_required
# def profile(request):
#     if request.method == 'POST':
#         user_form = UpdateUserForm(request.POST, instance=request.user)
#         profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
#
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, 'Your profile is updated successfully')
#             return redirect(to='users-profile')
#     else:
#         user_form = UpdateUserForm(instance=request.user)
#         profile_form = UpdateProfileForm(instance=request.user.profile)
#
#     return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})
