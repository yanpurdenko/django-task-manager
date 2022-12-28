from django.db import models
from PIL import Image
from app.models import Worker


class Profile(models.Model):
    worker = models.OneToOneField(Worker, on_delete=models.CASCADE)
    avatar = models.ImageField(default="default.jpg", upload_to="profile_images")
    phone = models.CharField(max_length=255)
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
