from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ..models import Application, Interview


@receiver(post_save, sender=Application)
def create_interview(sender, instance, **kwargs):
    if instance.status == Application.STATUS.ACCEPTED:
        scheduled_time = timezone.now() + timedelta(days=2)

        if scheduled_time < instance.vacancy.deadline:
            raise ValidationError(
                _("Interview cannot be scheduled before the vacancy's deadline.")
            )

        if scheduled_time.weekday() >= 5:
            scheduled_time += timedelta(days=(7 - scheduled_time.weekday()))

        Interview.objects.create(
            application=instance,
            schedule_datetime=scheduled_time,
        )
