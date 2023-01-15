from django.db import models
from PIL import Image
from app.models import Worker
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    worker = models.OneToOneField(Worker, on_delete=models.CASCADE)
    avatar = models.ImageField(default="default.png", upload_to="profile_images")
    phone = PhoneNumberField(blank=True, null=True, help_text="Mobile phone number")
    main_programming_language = models.CharField(max_length=255)

    def __str__(self):
        return self.worker.username

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
