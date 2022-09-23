from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """
    Profile model to keep track of paid status and order history
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experimentalist_uid = models.CharField(max_length=50, default="")
    laboratory_uid = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
