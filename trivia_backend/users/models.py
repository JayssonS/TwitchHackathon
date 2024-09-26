from django.db import models
from django.contrib.auth.models import User

class TwitchChannel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Establish a link to the Django user
    channel_name = models.CharField(max_length=255)  # The Twitch channel name

    def __str__(self):
        return self.channel_name
