from django.db import models
import secrets
print(secrets.token_urlsafe(50))


# users/models.py
from django.db import models
from django.contrib.auth.models import User

class ActiveChannel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Reference to the logged-in user
    channel_name = models.CharField(max_length=50, unique=True)  # Twitch channel name
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.channel_name
