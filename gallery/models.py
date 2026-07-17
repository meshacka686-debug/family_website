from django.db import models
from django.contrib.auth.models import User


class Photo(models.Model):
    image = models.ImageField(upload_to="photos/")
    caption = models.CharField(max_length=255)
