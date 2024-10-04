import os

import requests

from config.env import BASE_DIR, env

# env.read_env(os.path.join(BASE_DIR, ".env"))

# This URL is used for sending messages
my_uri = env("SMS_URI")

# Change these values to match your own account
my_username = str(env("SMS_USERNAME"))
my_password = str(env("SMS_PASSWORD"))


def send_vacancy_application_notification_text(instance, created):
    if created and instance.status == "submitted":
        recipient = str(instance.primary_contact)
        # message_body = f"Your application for the {instance.vacancy.title} position at Telecom Namibia has been received. Thank you for choosing Telecom Namibia."
        message_body = f"Thank you for submitting your application for the {instance.vacancy.title} opportunity at Telecom Namibia. We acknowledge receipt of your application and will carefully assess your qualifications. You will be notified once the review process has been completed.Thank you for your interest in joining Telecom Namibia."
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
        # message_body = f"Congratulations! Your application for the {instance.vacancy.title} position at Telecom Namibia has been successful. We'll be in touch soon with more details. Thank you for choosing Telecom Namibia."
        message_body = f"Thank you for submitting your application for the {instance.vacancy.title} opportunity at Telecom Namibia. Your application has successfully met the minimum criteria for further assessment. We will review your submission and inform you of the next steps in due course. We appreciate your interest in a career with Telecom Namibia."
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
        # message_body = f"Unfortunately, your application for the {instance.vacancy.title} position hasn't been selected. We appreciate you considering Telecom Namibia. We wish you all the best in your job search."
        message_body = f"Thank you for your application for the {instance.vacancy.title} opportunity at Telecom Namibia. After a thorough review, we regret to inform you that your application does not meet the minimum criteria. We value your interest in Telecom Namibia and encourage you to apply for future opportunities. Wishing you success in your job search."
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


def send_vacancy_interview_notification_text(instance, created):
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
