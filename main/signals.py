import django.dispatch
from django.db.models.signals import post_save
from django.dispatch import receiver

from main.models import User, Profile

user_done = django.dispatch.Signal()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()