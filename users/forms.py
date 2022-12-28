from django import forms

from app.models import Worker
from .models import Profile


class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    username = forms.CharField(max_length=100, required=True)

    class Meta:
        model = Worker
        fields = ["first_name", "last_name", "username"]


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={
        "class": "btn btn-primary addButtonTask m-0", "placeholder": "", "value": ""
    }))
    phone = forms.CharField(max_length=255)
    main_programming_language = forms.CharField(max_length=255)

    class Meta:
        model = Profile
        fields = ["avatar", "phone", "main_programming_language"]
