from celery import shared_task

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
    instance = Application.objects.get(id=instance_id)
    send_vacancy_application_notification_email(instance, created)


@shared_task
def send_vacancy_application_notification_text_task(instance_id, created):
    instance = Application.objects.get(id=instance_id)
    send_vacancy_application_notification_text(instance, created)


@shared_task
def send_interview_notification_email_task(instance_id, created):
    instance = Interview.objects.get(id=instance_id)
    send_interview_notification_email(instance, created)


@shared_task
def send_interview_notification_text_task(instance_id, created):
    instance = Interview.objects.get(id=instance_id)
    send_vacancy_interview_notification_text(instance, created)
