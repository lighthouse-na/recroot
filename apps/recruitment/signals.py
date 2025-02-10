from datetime import timedelta

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Application, Interview
from .tasks import (
    send_interview_notification_email_task,
    send_interview_notification_text_task,
    send_vacancy_application_notification_email_task,
    send_vacancy_application_notification_text_task,
)


@receiver(post_save, sender=Application)
def send_application_notification_tasks(sender, instance, created, **kwargs):
    """
    Sends notification tasks (email and text) when an application is saved.

    This receiver listens for the post_save signal on the Application model
    and triggers email and text message notifications about the application
    status.

    Args:
        sender: The model class (Application).
        instance: The instance of the model (Application).
        created: Boolean flag indicating whether the instance was created or updated.
        kwargs: Additional keyword arguments.
    """
    transaction.on_commit(
        lambda: (
            send_vacancy_application_notification_email_task.delay(instance.id, created),
            send_vacancy_application_notification_text_task.delay(instance.id, created),
        )
    )


@receiver(post_save, sender=Interview)
def send_interview_notification_tasks(sender, instance, created, **kwargs):
    """
    Sends notification tasks (email and text) when an interview is saved.

    This receiver listens for the post_save signal on the Interview model
    and triggers email and text message notifications about the interview
    status.

    Args:
        sender: The model class (Interview).
        instance: The instance of the model (Interview).
        created: Boolean flag indicating whether the instance was created or updated.
        kwargs: Additional keyword arguments.
    """
    transaction.on_commit(
        lambda: (
            send_interview_notification_email_task.delay(instance.id, created),
            send_interview_notification_text_task.delay(instance.id, created),
        )
    )


@receiver(post_save, sender=Application)
def create_interview(sender, instance, **kwargs):
    """
    Creates an interview when an application is accepted.

    When an application is marked as accepted, this receiver schedules an interview
    by creating an Interview instance with a default schedule time.

    Args:
        sender: The model class (Application).
        instance: The instance of the model (Application).
        kwargs: Additional keyword arguments.
    """
    if instance.status == Application.STATUS.ACCEPTED:
        scheduled_time = timezone.now() + timedelta(days=2)

        # if scheduled_time < instance.vacancy.deadline:
        #     raise ValidationError(
        #         _("Interview cannot be scheduled before the vacancy's deadline.")
        #     )

        if scheduled_time.weekday() >= 5:
            scheduled_time += timedelta(days=(7 - scheduled_time.weekday()))

        Interview.objects.create(
            application=instance,
            schedule_datetime=scheduled_time,
        )
