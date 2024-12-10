from allauth.account.signals import email_confirmed
from django.dispatch import receiver


@receiver(email_confirmed)
def set_staff_status(sender, request, email_address, **kwargs):
    """
    Sets the user's 'is_staff' status to True when their email is confirmed.

    This signal handler is triggered when an email address is confirmed
    by the user. It updates the related user’s `is_staff` field to `True`,
    granting them access to the Django admin and other staff privileges.

    Args:
        sender: The sender of the signal (not used in this case).
        request: The HTTP request object associated with the signal.
        email_address: The email address object that has been confirmed.
        **kwargs: Additional keyword arguments that may be passed with the signal.
    """
    user = email_address.user
    user.is_staff = True
    user.save()
