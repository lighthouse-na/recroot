import os

import requests
from django.db.models.signals import post_save
from django.dispatch import receiver

from config.env import BASE_DIR, env

from ..models import Interview, Application

env.read_env(os.path.join(BASE_DIR, ".env"))

# This URL is used for sending messages
my_uri = env("SMS_URI")

# Change these values to match your own account
my_username = str(env("SMS_USERNAME"))
my_password = str(env("SMS_PASSWORD"))


@receiver(post_save, sender=Application)
def send_vacancy_application_notification(sender, instance, created, **kwargs):
    if created and instance.status == "submitted":
        recipient = str(instance.primary_contact)
        message_body = f"Your application has been received by Telecom Namibia."
        http_req = (
            f"{my_uri}/api?action=sendmessage"
            f"&username={my_username}"
            f"&password={my_password}"
            f"&recipient={recipient}"
            f"&messagetype=SMS:TEXT"
            f"&messagedata={message_body}"
        )
        try:
            response = requests.post(http_req)
            response.raise_for_status()
            print("Message sent")

        except requests.exceptions.RequestException as ex:
            print("An error occurred: {}".format(ex))
            if ex.response is not None:
                print("Error details: {}".format(ex.response.text))

    if not created and instance.status == "accepted":
        recipient = str(instance.primary_contact)
        message_body = f"Your application for the {instance.vacancy.title} at Telecom Namibia has been accepted. Please check your email({instance.email}) inbox or spam folder for more information. Thank you for choosing Telecom Namibia."
        http_req = (
            f"{my_uri}/api?action=sendmessage"
            f"&username={my_username}"
            f"&password={my_password}"
            f"&recipient={recipient}"
            f"&messagetype=SMS:TEXT"
            f"&messagedata={message_body}"
        )
        try:
            response = requests.post(http_req)
            response.raise_for_status()
            print("Message sent")

        except requests.exceptions.RequestException as ex:
            print("An error occurred: {}".format(ex))
            if ex.response is not None:
                print("Error details: {}".format(ex.response.text))

    if not created and instance.status == "rejected":
        recipient = str(instance.primary_contact)
        message_body = f"Your application for the {instance.vacancy.title} at Telecom Namibia has been rejected. Please check your email({instance.email}) inbox or spam folder for more information."
        http_req = (
            f"{my_uri}/api?action=sendmessage"
            f"&username={my_username}"
            f"&password={my_password}"
            f"&recipient={recipient}"
            f"&messagetype=SMS:TEXT"
            f"&messagedata={message_body}"
        )
        try:
            response = requests.post(http_req)
            response.raise_for_status()
            print("Message sent")

        except requests.exceptions.RequestException as ex:
            print("An error occurred: {}".format(ex))
            if ex.response is not None:
                print("Error details: {}".format(ex.response.text))


@receiver(post_save, sender=Interview)
def send_vacancy_interview_notification(sender, instance, created, **kwargs):
    if created and instance.status == "scheduled":
        recipient = str(instance.primary_contact)
        message_body = f"Telecom Namibia invites you for a {instance.application.vacancy.title} interview, please check your email inbox or spam folder for more information."
        http_req = (
            f"{my_uri}/api?action=sendmessage"
            f"&username={my_username}"
            f"&password={my_password}"
            f"&recipient={recipient}"
            f"&messagetype=SMS:TEXT"
            f"&messagedata={message_body}"
        )
        try:
            response = requests.post(http_req)
            response.raise_for_status()
            print("Message sent")

        except requests.exceptions.RequestException as ex:
            print("An error occurred: {}".format(ex))
            if ex.response is not None:
                print("Error details: {}".format(ex.response.text))
