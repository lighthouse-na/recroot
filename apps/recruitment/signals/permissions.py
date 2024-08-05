from django.db.models.signals import post_save
from django.dispatch import receiver
from guardian.shortcuts import assign_perm, get_groups_with_perms, get_users_with_perms

from ..models import Application


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
