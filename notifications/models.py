from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(User, related_name="notifications")
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.message}"
