from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default='2023-01-01T00:00:00')

    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"
