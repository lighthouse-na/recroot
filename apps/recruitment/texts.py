import requests

from config.env import env

# This URL is used for sending messages
my_uri = env("SMS_URI")

# Change these values to match your own account
my_username = str(env("SMS_USERNAME"))
my_password = str(env("SMS_PASSWORD"))


def send_vacancy_application_notification_text(instance, created):
    """
    Sends a vacancy application notification as an SMS to the primary contact
    of the applicant based on the application status.

    Args:
        instance (Application): The application instance related to the vacancy.
        created (bool): A flag indicating whether the application was just created or updated.

    Sends the following messages:
        - If the application is created and status is "submitted", a confirmation message is sent.
        - If the application status is "accepted", a success message is sent.
        - If the application status is "rejected", a rejection message with review comments is sent.
    """
    if created and instance.status == "submitted":
        recipient = str(instance.primary_contact)
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
        message_body = f"Thank you for your application for the {instance.vacancy.title} opportunity at Telecom Namibia. After a thorough review, we regret to inform you that your application does not meet the minimum criteria. Reason: {instance.review_comments} We value your interest in Telecom Namibia and encourage you to apply for future opportunities. Wishing you success in your job search."
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
    """
    Sends an interview invitation notification as an SMS to the primary contact
    of the applicant when an interview is scheduled.

    Args:
        instance (Interview): The interview instance related to the application.
        created (bool): A flag indicating whether the interview was just created or updated.

    Sends a message with an interview invitation link if the interview status is "scheduled".
    """
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
