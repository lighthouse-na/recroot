from allauth.account.signals import email_confirmed, user_signed_up
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(email_confirmed)
def set_staff_status(sender, request, email_address, **kwargs):
    user = email_address.user
    user.is_staff = True
    user.save()
