from django.db import models
from django.contrib.auth.models import User

class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(blank=True, null=True)  # Firebase URL
