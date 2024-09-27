from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class TwitchChannel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=100)

    def __str__(self):
        return self.channel_name

class Friendship(models.Model):
    from_user = models.ForeignKey(User, related_name='friendships_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friendships_received', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')], default='pending')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    online = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} Profile"
