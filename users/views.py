from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from app.models import Worker
from users.forms import UpdateUserForm, UpdateProfileForm


@login_required()
def profile_view(request):
    """View function for users profiles pages."""

    worker = Worker.objects.get(id=request.user.id)
    update_profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

    return render(request, "users/profile.html", {"worker": worker, "update_profile_form": update_profile_form})


@login_required
def update_profile_view(request):
    """View function for updating users profiles datas with validation."""

    worker = Worker.objects.get(id=request.user.id)

    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        update_profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and update_profile_form.is_valid():
            user_form.save()
            update_profile_form.save()
            messages.success(request, "Your profile is updated successfully")
            return redirect("users:profile")

        return render(request, "users/update_profile.html", {
            "user_form": user_form, "update_profile_form": update_profile_form, "worker": worker
        })
    return render(request, "users/update_profile.html", {"worker": worker})


class WorkersListView(LoginRequiredMixin, generic.ListView):
    """
    ListView class for page with full list of
    users profiles without current login user.
    """

    model = Worker
    template_name = "users/workers_profiles.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkersListView, self).get_context_data(**kwargs)

        context["workers"] = Worker.objects.exclude(id=self.request.user.id).select_related()

        return context


class WorkerProfileDetailView(LoginRequiredMixin, generic.DetailView):
    """DetailView class for user profile page."""

    model = Worker
    template_name = "users/worker_profile_detail.html"


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    """
    PasswordResetView class for reset user account password.
    If user email exist in database, he will receive link
    on this email for password reset.
    """

    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.html"
    subject_template_name = "users/password_reset_subject"
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy("login")


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    """
    PasswordChangeView class for changing password.
    User will need to input old password and new password.
    If the password is incorrect, a notification will be raised.
    """

    template_name = "users/change_password.html"
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy("users:profile")
