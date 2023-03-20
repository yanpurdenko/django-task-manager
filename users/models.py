from __future__ import annotations

import os
import uuid

from django.db import models
from django.utils.text import slugify

from app.models import Worker
from phonenumber_field.modelfields import PhoneNumberField


def avatar_image_file_path(instance: Profile, filename: str) -> str:
    _, ext = os.path.splitext(filename)

    filename = f"{slugify(instance.avatar)}-{uuid.uuid4()}.{ext}"

    return os.path.join("profile_images/", filename)


class Profile(models.Model):
    worker = models.OneToOneField(Worker, on_delete=models.CASCADE)
    avatar = models.ImageField(
        default="https://res.cloudinary.com/***REMOVED***/image/upload/v1679338671/media/default.png",
        upload_to=avatar_image_file_path
    )
    phone = PhoneNumberField(blank=True, null=True, help_text="Mobile phone number")
    main_programming_language = models.CharField(max_length=255)

    def __str__(self):
        return self.worker.username

    def save(self, *args, **kwargs):
        super().save()
