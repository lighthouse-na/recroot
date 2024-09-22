from django.core.mail import EmailMessage
from django.urls import reverse
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates/emails/"))
email = "recruitment@email.com"
message = None


def send_email_notification(
    subject, template_name, instance, recipient_name, recipient_list
):
    from_email = email
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


def send_interview_notification_email(instance, created):

    subject = f"{instance.application.vacancy} Application Interview"
    from_email = email

    first_name = getattr(instance.application, "first_name", None)
    last_name = getattr(instance.application, "last_name", None)
    recipient_list = [instance.application.email]

    recipient_name = (
        f"{first_name} {last_name}" if first_name and last_name else "Applicant"
    )

    if not created and instance.status == "scheduled":

        invitation_link = reverse(
            "recruitment:interview_invitation", kwargs={"pk": instance.pk}
        ).lstrip("/")
        invitation_url = f"http://training.telecom.na/{invitation_link}"

        template = env.get_template("interview.html")

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
