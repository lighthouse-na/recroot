from django.core.mail import EmailMessage
from django.urls import reverse
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates/emails/"))
email = "training@telecom.na"
message = None


def send_email_notification(subject, template_name, instance, recipient_name, recipient_list):
    """
    Sends an email notification with the provided subject, template, and recipient details.

    Args:
        subject (str): The subject of the email.
        template_name (str): The name of the email template to be used.
        instance (object): The object instance to be passed to the template for rendering.
        recipient_name (str): The name of the email recipient.
        recipient_list (list): A list of email addresses to send the notification to.
    """
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
    """
    Sends a vacancy application status notification email based on the application's status.

    Args:
        instance (object): The application instance to be used for rendering the email.
        created (bool): A flag indicating whether the application was just created or updated.
    """
    first_name = getattr(instance, "first_name", None)
    last_name = getattr(instance, "last_name", None)
    recipient_list = [instance.email]

    recipient_name = f"{first_name} {last_name}" if first_name and last_name else "Applicant"

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
    elif not created and instance.status == "acknowledgement_with_timeline":
        send_email_notification(
            subject="Acknowlegement with timeline",
            template_name="acknowledgement_with_timeline.html",
            instance=instance,
            recipient_name=recipient_name,
            recipient_list=recipient_list,
        )
    elif not created and instance.status == "on_hold":
        send_email_notification(
            subject="Application on hold",
            template_name="on_hold.html",
            instance=instance,
            recipient_name=recipient_name,
            recipient_list=recipient_list,
        )



def send_interview_notification_email(instance, created):
    """
    Sends an email notification for an interview invitation if the interview is scheduled.

    Args:
        instance (object): The interview instance to be used for rendering the email.
        created (bool): A flag indicating whether the interview was just created or updated.
    """
    subject = f"{instance.application.vacancy} Application Interview"
    from_email = email

    first_name = getattr(instance.application, "first_name", None)
    last_name = getattr(instance.application, "last_name", None)
    recipient_list = [instance.application.email]

    recipient_name = f"{first_name} {last_name}" if first_name and last_name else "Applicant"

    if not created and instance.status == "scheduled":
        invitation_link = reverse("recruitment:interview_invitation", kwargs={"pk": instance.pk}).lstrip("/")
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
