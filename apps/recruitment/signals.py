from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Subscriber, Vacancy

email = "recruitment@email.com"


@receiver(post_save, sender=Vacancy)
def send_vacancy_notification(sender, instance, created, **kwargs):
    if created and instance.is_public:
        vacancy_type = instance.vacancy_type
        subscribers = Subscriber.objects.filter(
            subscribed=True, vacancy_types__type=vacancy_type
        )
        subject = f"New Vacancy: {instance.title}"
        message = f"Check out our new vacancy: {instance.title}. Deadline: {instance.deadline}"
        from_email = email
        for subscriber in subscribers:
            send_mail(subject, message, from_email, [subscriber.email])
