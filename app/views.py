from django.shortcuts import render

from app.models import Task


def index(request):
    """View function for the home page of the site."""

    all_tasks = Task.objects.all().prefetch_related()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "all_tasks": all_tasks
    }

    return render(request, "app/index.html", context=context)
