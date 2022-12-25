from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app.models import Worker


@login_required()
def profile_view(request):
    worker = Worker.objects.get(id=request.user.id)

    context = {
        "worker": worker,
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
