from celery import shared_task

from .models import Application
from .signals.emails import send_vacancy_application_notification


@shared_task
def send_vacancy_application_notification_task(instance_id):
    instance = Application.objects.get(id=instance_id)
    send_vacancy_application_notification(instance, created=True)
