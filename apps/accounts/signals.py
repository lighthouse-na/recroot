from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up, email_confirmed
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(email_confirmed)
def set_staff_status(sender, request, email_address, **kwargs):
    user = email_address.user
    user.is_staff = True
    user.save()
