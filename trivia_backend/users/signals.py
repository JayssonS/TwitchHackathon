from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import UserProfile

@receiver(user_logged_in)
def set_online_status(sender, user, request, **kwargs):
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.online = True
    profile.save()

@receiver(user_logged_out)
def set_offline_status(sender, user, request, **kwargs):
    profile = UserProfile.objects.get(user=user)
    profile.online = False
    profile.save()
