from django import forms
from django.contrib.auth.forms import UserCreationForm

from app.models import Worker


class WorkerCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + ("email", "first_name", "last_name", "position",)


class TasksSearchForm(forms.Form):
    name = forms.CharField(max_length=255, required=True)
