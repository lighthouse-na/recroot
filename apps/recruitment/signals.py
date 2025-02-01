from datetime import timedelta

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from guardian.shortcuts import assign_perm, get_groups_with_perms, get_users_with_perms

from .models import Application, Interview
from .tasks import (
    send_interview_notification_email_task,
    send_interview_notification_text_task,
    send_vacancy_application_notification_email_task,
    send_vacancy_application_notification_text_task,
)


@receiver(post_save, sender=Application)
def send_application_notification_tasks(sender, instance, created, **kwargs):
    """
    Sends notification tasks (email and text) when an application is saved.

    This receiver listens for the post_save signal on the Application model
    and triggers email and text message notifications about the application
    status.

    Args:
        sender: The model class (Application).
        instance: The instance of the model (Application).
        created: Boolean flag indicating whether the instance was created or updated.
        kwargs: Additional keyword arguments.
    """
    transaction.on_commit(
        lambda: (
            send_vacancy_application_notification_email_task.delay(
                instance.id, created
            ),
            send_vacancy_application_notification_text_task.delay(instance.id, created),
        )
    )


@receiver(post_save, sender=Interview)
def send_interview_notification_tasks(sender, instance, created, **kwargs):
    """
    Sends notification tasks (email and text) when an interview is saved.

    This receiver listens for the post_save signal on the Interview model
    and triggers email and text message notifications about the interview
    status.

    Args:
        sender: The model class (Interview).
        instance: The instance of the model (Interview).
        created: Boolean flag indicating whether the instance was created or updated.
        kwargs: Additional keyword arguments.
    """
    transaction.on_commit(
        lambda: (
            send_interview_notification_email_task.delay(instance.id, created),
            send_interview_notification_text_task.delay(instance.id, created),
        )
    )


@receiver(post_save, sender=Application)
def create_application_permissions(sender, instance, created, **kwargs):
    """
    Creates permissions for users and groups based on vacancy permissions.

    When a new application is created, this receiver assigns the appropriate
    permissions (view, change, delete) to users and groups who have permissions
    on the related vacancy.

    Args:
        sender: The model class (Application).
        instance: The instance of the model (Application).
        created: Boolean flag indicating whether the instance was created or updated.
        kwargs: Additional keyword arguments.
    """
    if created:
        vacancy = instance.vacancy
        users_with_perms = get_users_with_perms(vacancy, attach_perms=True)
        groups_with_perms = get_groups_with_perms(vacancy, attach_perms=True)

        for user, perms in users_with_perms.items():
            if "view_vacancy" in perms:
                assign_perm("view_application", user, instance)
            if "change_vacancy" in perms:
                assign_perm("change_application", user, instance)
            if "delete_vacancy" in perms:
                assign_perm("delete_application", user, instance)

        for group, perms in groups_with_perms.items():
            if "view_vacancy" in perms:
                assign_perm("view_application", group, instance)
            if "change_vacancy" in perms:
                assign_perm("change_application", group, instance)
            if "delete_vacancy" in perms:
                assign_perm("delete_application", group, instance)


@receiver(post_save, sender=Interview)
def create_interview_permissions(sender, instance, created, **kwargs):
    """
    Creates permissions for users and groups on the Interview instance.

    When a new interview is created, this receiver assigns the appropriate
    permissions (view, change, delete) for the interview to the users and
    groups who have permissions on the related application.

    Args:
        sender: The model class (Interview).
        instance: The instance of the model (Interview).
        created: Boolean flag indicating whether the instance was created or updated.
        kwargs: Additional keyword arguments.
    """
    if created:
        content_type = ContentType.objects.get_for_model(Interview)
        view_perm = Permission.objects.get(
            codename="view_interview", content_type=content_type
        )
        change_perm = Permission.objects.get(
            codename="change_interview", content_type=content_type
        )
        delete_perm = Permission.objects.get(
            codename="delete_interview", content_type=content_type
        )

        for user in get_users_with_perms(instance.application):
            user.user_permissions.add(view_perm, change_perm, delete_perm)
            assign_perm("view_interview", user, instance)
            assign_perm("change_interview", user, instance)
            assign_perm("delete_interview", user, instance)

        for group in get_groups_with_perms(instance.application):
            group.permissions.add(view_perm, change_perm, delete_perm)
            assign_perm("view_interview", group, instance)
            assign_perm("change_interview", group, instance)
            assign_perm("delete_interview", group, instance)


@receiver(post_save, sender=Application)
def create_interview(sender, instance, **kwargs):
    """
    Creates an interview when an application is accepted.

    When an application is marked as accepted, this receiver schedules an interview
    by creating an Interview instance with a default schedule time.

    Args:
        sender: The model class (Application).
        instance: The instance of the model (Application).
        kwargs: Additional keyword arguments.
    """
    if instance.status == Application.STATUS.ACCEPTED:
        scheduled_time = timezone.now() + timedelta(days=2)

        # if scheduled_time < instance.vacancy.deadline:
        #     raise ValidationError(
        #         _("Interview cannot be scheduled before the vacancy's deadline.")
        #     )

        if scheduled_time.weekday() >= 5:
            scheduled_time += timedelta(days=(7 - scheduled_time.weekday()))

        Interview.objects.create(
            application=instance,
            schedule_datetime=scheduled_time,
        )


@receiver(post_save, sender=Application)
def add_reviewers_to_application(sender, instance, created, **kwargs):
    """
    Adds reviewers to an application upon creation.

    When a new application is created, this receiver automatically adds the
    reviewers from the related vacancy to the application's `reviewed_by` field.

    Args:
        sender: The model class (Application).
        instance: The instance of the model (Application).
        created: Boolean flag indicating whether the instance was created or updated.
        kwargs: Additional keyword arguments.
    """
    if created:
        vacancy = instance.vacancy
        reviewers = vacancy.reviewers.all()

        for reviewer in reviewers:
            instance.reviewers.add(reviewer)

        instance.save()
