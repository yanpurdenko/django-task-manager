from django.contrib import admin
from users.models import Profile


@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    """Register class for model Profile to admin page."""

    pass
