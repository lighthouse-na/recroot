import os

from django.core.mail import EmailMessage, send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from jinja2 import Environment, FileSystemLoader

from ..models import Application, Interview, Subscriber, Vacancy

env = Environment(loader=FileSystemLoader("templates/emails/"))
email = "recruitment@email.com"
message = None


@receiver(post_save, sender=Vacancy)
def send_vacancy_notification(sender, instance, created, **kwargs):
    if instance.is_public and instance.is_published:
        vacancy_type = instance.vacancy_type
        subscribers = Subscriber.objects.filter(
            subscribed=True, vacancy_types__type=vacancy_type
        )
        subject = f"New Vacancy: {instance.title}"
        message = f"Check out our new vacancy: {instance.title}. Deadline: {instance.deadline}"
        from_email = email
        for subscriber in subscribers:
            send_mail(subject, message, from_email, [subscriber.email])


def send_email_notification(
    subject, template_name, instance, recipient_name, recipient_list
):
    from_email = "careers@telecom.na"
    template = env.get_template(template_name)
    message = template.render(instance=instance, recipient_name=recipient_name)

    send_email = EmailMessage(
        subject=subject,
        body=message,
        from_email=from_email,
        to=recipient_list,
    )
    send_email.content_subtype = "html"
    send_email.send()


def send_vacancy_application_notification_email(instance, created):
    first_name = getattr(instance, "first_name", None)
    last_name = getattr(instance, "last_name", None)
    recipient_list = [instance.email]

    recipient_name = (
        f"{first_name} {last_name}" if first_name and last_name else "Applicant"
    )

    if created and instance.status == "submitted":
        send_email_notification(
            subject="Application Submitted",
            template_name="submitted.html",
            instance=instance,
            recipient_name=recipient_name,
            recipient_list=recipient_list,
        )
    elif not created and instance.status == "accepted":
        send_email_notification(
            subject="Application Accepted",
            template_name="accepted.html",
            instance=instance,
            recipient_name=recipient_name,
            recipient_list=recipient_list,
        )
    elif not created and instance.status == "rejected":
        send_email_notification(
            subject="Application Rejected",
            template_name="rejected.html",
            instance=instance,
            recipient_name=recipient_name,
            recipient_list=recipient_list,
        )


# @receiver(post_save, sender=Application)
# def send_vacancy_application_notification(sender, instance, created, **kwargs):
#     subject = f"{instance.vacancy} Application Status"
#     from_email = "careers@telecom.na"

#     first_name = getattr(instance, "first_name", None)
#     last_name = getattr(instance, "last_name", None)
#     recipient_list = [instance.email]

#     recipient_name = (
#         f"{first_name} {last_name}" if first_name and last_name else "Applicant"
#     )

#     if created and instance.status == "submitted":
#         template = env.get_template("submitted.html")
#         subject = "Do not reply."
#         message = template.render(instance=instance, recipient_name=recipient_name)
#         send_email = EmailMessage(
#             subject=subject,
#             body=message,
#             from_email=from_email,
#             to=recipient_list,
#         )
#         send_email.content_subtype = "html"
#         send_email.send()

#     elif not created and instance.status == "accepted":
#         template = env.get_template("accepted.html")
#         subject = "Do not reply."
#         message = template.render(instance=instance, recipient_name=recipient_name)
#         send_email = EmailMessage(
#             subject=subject,
#             body=message,
#             from_email=from_email,
#             to=recipient_list,
#         )
#         send_email.content_subtype = "html"
#         send_email.send()

#     elif not created and instance.status == "rejected":
#         template = env.get_template("rejected.html")
#         subject = "Do not reply."
#         message = template.render(instance=instance, recipient_name=recipient_name)
#         send_email = EmailMessage(
#             subject=subject,
#             body=message,
#             from_email=from_email,
#             to=recipient_list,
#         )
#         send_email.content_subtype = "html"
#         send_email.send()

#     # send_mail(subject, message, from_email, recipient_list)


# @receiver(post_save, sender=Interview)
# def send_interview_notification_email(sender, instance, created, **kwargs):
def send_interview_notification_email(instance, created):
    subject = f"{instance.application.vacancy} Application Interview"
    from_email = "careers@telecom.na"

    first_name = getattr(instance.application, "first_name", None)
    last_name = getattr(instance.application, "last_name", None)
    recipient_list = [instance.application.email]

    recipient_name = (
        f"{first_name} {last_name}" if first_name and last_name else "Applicant"
    )

    if not created and instance.status == "scheduled":
        if recipient_list:
            invitation_link = reverse(
                "recruitment:interview_invitation", kwargs={"pk": instance.pk}
            )
            invitation_url = f"https://telecom.na/{invitation_link}"

            template = env.get_template("interview.html")
            subject = "Do not reply."
            message = template.render(
                instance=instance,
                recipient_name=recipient_name,
                invitation_url=invitation_url,
            )
            send_email = EmailMessage(
                subject=subject,
                body=message,
                from_email=from_email,
                to=recipient_list,
            )
            send_email.content_subtype = "html"
            send_email.send()
        # send_mail(subject, message, from_email, recipient_list)
