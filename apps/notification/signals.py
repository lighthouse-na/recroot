from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.recruitment.models import Vacancy

from .models import Notification
from .types import NOTIFICATION_TYPES


@receiver(post_save, sender=Vacancy)
def new_vacancy_notification(sender, instance, created, **kwargs):
    users = User.objects.filter(is_active=True)
    if instance.is_published:
        content_type = ContentType.objects.get_for_model(instance)
        for user in users:
            Notification.objects.create(
                user=user,
                notification_type=NOTIFICATION_TYPES.NEW_VACANCY,
                content_type=content_type,
                object_id=instance.pk,
                message=f"New {instance.vacancy_type.type.lower()} vacancy",
                created_at=instance.created_at,
            )


@receiver(post_save, sender=Notification)
def send_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        group_name = f"notifications-{instance.user.id}"
        event = {
            "type": "created",
            "id": instance.id,
            "user": instance.user.id,
            "object_id": instance.object_id,
            "message": instance.message,
            "read": instance.read,
            "created_at": instance.created_at,
        }
        async_to_sync(channel_layer.group_send)(group_name, event)
