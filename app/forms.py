from bootstrap_datepicker_plus.widgets import DatePickerInput
from django import forms
from django.contrib.auth.forms import UserCreationForm

from app.models import Worker, Task


class WorkerCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + ("email", "first_name", "last_name", "position",)


class CreateTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ("name", "description", "deadline", "priority", "task_type", "assignees",)
        widgets = {
            "deadline": DatePickerInput(),
            "description": forms.widgets.Textarea(attrs={"rows": "3"}),
        }


class UpdateTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ("name", "description", "deadline", "priority", "task_type", "assignees",)
        widgets = {
            "deadline": DatePickerInput(),
            "description": forms.widgets.Textarea(attrs={"rows": "3"}),
        }
