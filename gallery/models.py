from django.db import models
from django.contrib.auth.models import User


class Gallery(models.Model):
    image = models.ImageField(upload_to="gallery/")
    caption = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)  # 👈 add this

    def __str__(self):
        return self.caption



class Photo(models.Model):
    image = models.ImageField(upload_to="gallery/")
    caption = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)  # 👈 add here

    def __str__(self):
        return self.caption
