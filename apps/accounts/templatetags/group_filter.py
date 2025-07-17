from django import template

register = template.Library()


@register.filter(name="is_in_group")
def is_in_group(user, group_name):
    """
    Checks whether a user belongs to a specified group.

    This template filter verifies if the given user is a member of the group
    identified by the provided group name.

    Args:
        user (User): The Django User object to check.
        group_name (str): The name of the group to verify membership.

    Returns:
        bool: True if the user is in the specified group, otherwise False.
    """
    return user.groups.filter(name=group_name).exists()
