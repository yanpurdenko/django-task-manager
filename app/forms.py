from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.auth.forms import UserCreationForm

from app.models import Worker, Task
from task_manager import settings


class WorkerCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + ("email", "first_name", "last_name", "position",)


class CreateTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ("name", "description", "deadline", "priority", "task_type", "assignees",)
        deadline = forms.DateField(widget=forms.DateInput(format="%d/%m/%Y"), input_formats=settings.DATE_INPUT_FORMATS)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.fields["description"].widget.attrs = {"rows": 3}
        self.fields["deadline"].widget.attrs = {"type": "date"}


class UpdateTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ("name", "description", "deadline", "priority", "task_type", "assignees",)
        deadline = forms.DateField(widget=forms.DateInput(format="%d/%m/%Y"), input_formats=settings.DATE_INPUT_FORMATS)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.fields["description"].widget.attrs = {"rows": 3}
        self.fields["deadline"].widget.attrs = {"type": "date"}
