from datetime import timedelta

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
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
    transaction.on_commit(
        lambda: (
            send_vacancy_application_notification_email_task.delay(
                instance.id, created
            ),
            send_vacancy_application_notification_text_task.delay(instance.id, created),
        )
    )
    # transaction.on_commit(
    #     lambda: send_vacancy_application_notification_email_task.delay(
    #         instance.id, created
    #     ),
    # )
    # transaction.on_commit(
    #     lambda: send_vacancy_application_notification_text_task.delay(
    #         instance.id, created
    #     ),
    # )
    # send_vacancy_application_notification_email_task.delay(instance.id, created)
    # send_vacancy_application_notification_text_task.delay(instance.id, created)


@receiver(post_save, sender=Interview)
def send_interview_notification_tasks(sender, instance, created, **kwargs):
    transaction.on_commit(
        lambda: (
            send_interview_notification_email_task.delay(instance.id, created),
            send_interview_notification_text_task.delay(instance.id, created),
        )
    )


@receiver(post_save, sender=Application)
def create_application_permissions(sender, instance, created, **kwargs):
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
