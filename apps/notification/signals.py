from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.dispatch import receiver
from django.db.models.signals import post_save
from apps.recruitment.models import Vacancy

channel_layer = get_channel_layer()

@receiver(post_save, sender=Vacancy)
def send_vacancy_notification(sender, instance, created, **kwargs):
    if created and instance.is_published:
        vacancy = instance
        group_name = "staff-notifications"
        event = {
            "type": "vacancy_created",
            "vacancy_id": vacancy.id,
            "vacancy_slug": vacancy.slug,
            "vacancy_title": vacancy.title,
        }
        async_to_sync(channel_layer.group_send)(group_name, event)