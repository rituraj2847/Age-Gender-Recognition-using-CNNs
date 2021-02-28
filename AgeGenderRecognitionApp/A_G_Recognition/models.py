from django.db import models


class UploadedImage(models.Model):
    image = models.ImageField(upload_to="profile_picture/", blank=True)
