from celery import shared_task
from django.shortcuts import get_object_or_404

from .emails import (
    send_interview_notification_email,
    send_vacancy_application_notification_email,
)
from .models import Application, Interview
from .texts import (
    send_vacancy_application_notification_text,
    send_vacancy_interview_notification_text,
)


@shared_task
def send_vacancy_application_notification_email_task(instance_id, created):
    """
    A Celery task to send a vacancy application notification email.

    This task retrieves the Application instance using the provided instance ID
    and calls the function to send an application notification email.

    Args:
        instance_id (int): The ID of the Application instance.
        created (bool): A flag indicating whether the application was just created or updated.
    """
    instance = get_object_or_404(Application, pk=instance_id)
    send_vacancy_application_notification_email(instance, created)


@shared_task
def send_vacancy_application_notification_text_task(instance_id, created):
    """
    A Celery task to send a vacancy application notification text.

    This task retrieves the Application instance using the provided instance ID
    and calls the function to send an application notification text.

    Args:
        instance_id (int): The ID of the Application instance.
        created (bool): A flag indicating whether the application was just created or updated.
    """
    instance = get_object_or_404(Application, pk=instance_id)
    send_vacancy_application_notification_text(instance, created)


@shared_task
def send_interview_notification_email_task(instance_id, created):
    """
    A Celery task to send an interview notification email.

    This task retrieves the Interview instance using the provided instance ID
    and calls the function to send an interview notification email.

    Args:
        instance_id (int): The ID of the Interview instance.
        created (bool): A flag indicating whether the interview was just created or updated.
    """
    instance = get_object_or_404(Interview, pk=instance_id)
    send_interview_notification_email(instance, created)


@shared_task
def send_interview_notification_text_task(instance_id, created):
    """
    A Celery task to send an interview notification text.

    This task retrieves the Interview instance using the provided instance ID
    and calls the function to send an interview notification text.

    Args:
        instance_id (int): The ID of the Interview instance.
        created (bool): A flag indicating whether the interview was just created or updated.
    """
    instance = get_object_or_404(Interview, pk=instance_id)
    send_vacancy_interview_notification_text(instance, created)
