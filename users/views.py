from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from app.models import Worker
from users.forms import UpdateUserForm, UpdateProfileForm


@login_required()
def profile_view(request):
    worker = Worker.objects.get(id=request.user.id)
    profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

    return render(request, "users/profile.html", {"worker": worker, "profile_form": profile_form})


@login_required
def update_profile_view(request):
    worker = Worker.objects.get(id=request.user.id)

    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile is updated successfully")
            return redirect("users:worker-profile")

        return render(request, "users/update_profile.html", {
            "user_form": user_form, "profile_form": profile_form, "worker": worker
        })
    return render(request, "users/update_profile.html", {"worker": worker})
