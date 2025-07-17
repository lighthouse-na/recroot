from datetime import timedelta

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

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
            send_vacancy_application_notification_email_task.delay(instance.id, created),
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


<<<<<<< HEAD
# ***************************************************************************************************
#                                           PERMISSIONS
# ***************************************************************************************************
# def get_permission(codename, model):
#     """Helper function to get a permission object."""
#     content_type = ContentType.objects.get_for_model(model)
#     try:
#         return Permission.objects.get(content_type=content_type, codename=codename)
#     except Permission.DoesNotExist:
#         return None


# @receiver(post_save, sender=Vacancy)
# def create_recruitment_permissions(sender, instance, created, **kwargs):
#     """
#     Assigns necessary permissions to reviewers of a Vacancy when it is created or updated.
#     """
#     # Get required permissions
#     permissions_list = [
#         get_permission("view_vacancy", Vacancy),
#         get_permission("view_application", Application),
#         get_permission("change_application", Application),
#         get_permission("view_interview", Interview),
#         get_permission("change_interview", Interview),
#     ]
#     permissions_list = [p for p in permissions_list if p]  # Remove None values

#     for reviewer in instance.reviewers.all():
#         reviewer.user_permissions.add(*permissions_list)


# @receiver(m2m_changed, sender=Vacancy.reviewers.through)
# def update_recruitment_permissions(sender, instance, action, pk_set, **kwargs):
#     """
#     Updates permissions when reviewers are added or removed from a Vacancy.
#     """

#     # Fetch permissions once to avoid multiple queries
#     permissions_list = [
#         get_permission("view_vacancy", Vacancy),
#         get_permission("view_application", Application),
#         get_permission("change_application", Application),
#         get_permission("view_interview", Interview),
#         get_permission("change_interview", Interview),
#     ]
#     permissions_list = [p for p in permissions_list if p]  # Remove None values

#     if action == "post_add":
#         # Assign permissions to newly added reviewers
#         for reviewer_id in pk_set:
#             reviewer = instance.reviewers.model.objects.get(pk=reviewer_id)
#             reviewer.user_permissions.add(*permissions_list)

#     elif action in ["post_remove", "post_clear"]:
#         # Remove permissions from reviewers
#         for reviewer_id in pk_set:
#             reviewer = instance.reviewers.model.objects.get(pk=reviewer_id)
#             reviewer.user_permissions.remove(*permissions_list)


# @receiver(post_save, sender=Application)
# def create_application_permissions(sender, instance, created, **kwargs):
#     """
#     Assigns 'view_application' and 'change_application' permissions to reviewers.

#     When an application is created, all users listed as reviewers for that application
#     will be given 'view_application' and 'change_application' permissions.

#     Args:
#         sender: The model class (Application).
#         instance: The instance of the model (Application).
#         created: Boolean flag indicating whether the instance was created or updated.
#         kwargs: Additional keyword arguments.
#     """
#     if created:
#         for reviewer in instance.reviewers.all():
#             assign_perm("view_application", reviewer, instance)
#             assign_perm("change_application", reviewer, instance)


# @receiver(post_save, sender=Interview)
# def create_interview_permissions(sender, instance, created, **kwargs):
#     """
#     Creates permissions for users and groups on the Interview instance.

#     When a new interview is created, this receiver assigns the appropriate
#     permissions (view, change, delete) for the interview to the users and
#     groups who have permissions on the related application.

#     Args:
#         sender: The model class (Interview).
#         instance: The instance of the model (Interview).
#         created: Boolean flag indicating whether the instance was created or updated.
#         kwargs: Additional keyword arguments.
#     """
#     if created:
#         content_type = ContentType.objects.get_for_model(Interview)
#         view_perm = Permission.objects.get(codename="view_interview", content_type=content_type)
#         change_perm = Permission.objects.get(codename="change_interview", content_type=content_type)
#         delete_perm = Permission.objects.get(codename="delete_interview", content_type=content_type)

#         for user in get_users_with_perms(instance.application):
#             user.user_permissions.add(view_perm, change_perm, delete_perm)
#             assign_perm("view_interview", user, instance)
#             assign_perm("change_interview", user, instance)
#             assign_perm("delete_interview", user, instance)

#         for group in get_groups_with_perms(instance.application):
#             group.permissions.add(view_perm, change_perm, delete_perm)
#             assign_perm("view_interview", group, instance)
#             assign_perm("change_interview", group, instance)
#             assign_perm("delete_interview", group, instance)


# ***************************************************************************************************
#                                           END PERMISSIONS
# ***************************************************************************************************


=======
>>>>>>> upstream/main
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
