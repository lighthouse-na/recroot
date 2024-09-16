import requests
import base64
import os
from config.env import BASE_DIR, env
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models import Interview

env.read_env(os.path.join(BASE_DIR, ".env"))

# This URL is used for sending messages
my_uri = "https://api.bulksms.com/v1/messages"

# Change these values to match your own account
my_username = env("SMS_USERNAME")
my_password = env("SMS_PASSWORD")


@receiver(post_save, sender=Interview)
def send_interview_notification_email(sender, instance, created, **kwargs):
    if not created and instance.status == "scheduled":
        my_data = {
            "to": str(instance.application.primary_contact),
            "body": f"<Company Name> invites you to {instance.application.vacancy.title} Interview, please check your email({instance.application.email}) for further details.",
            "encoding": "UNICODE",
            "longMessageMaxParts": "30",
        }

        # Encode credentials to Base64
        credentials = f"{my_username}:{my_password}"
        encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode(
            "utf-8"
        )

        # Headers for the request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_credentials}",
        }

        # Make the POST request
        try:
            response = requests.post(my_uri, json=my_data, headers=headers)
            # Check if the request was successful
            response.raise_for_status()
            # Print the response from the API
            print(response.text)

        except requests.exceptions.RequestException as ex:
            # Show the general message
            print("An error occurred: {}".format(ex))
            # Print the detail that comes with the error if available
            if ex.response is not None:
                print("Error details: {}".format(ex.response.text))
