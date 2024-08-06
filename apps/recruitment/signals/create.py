from datetime import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import Application, Interview


@receiver(post_save, sender=Application)
def create_interview(sender, instance, **kwargs):
    if instance.status == Application.STATUS.ACCEPTED:
        Interview.objects.create(
            application=instance,
            # created_at=datetime(2000, 1, 1),
            schedule_datetime=datetime(2000, 1, 1),
        )
