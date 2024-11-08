from apps.utils import validators

from . import models


# Name validations
def first_name_validation(request):
    return validators.validate_name(request, "first_name")


def middle_name_validation(request):
    return validators.validate_name(request, "middle_name")


def last_name_validation(request):
    return validators.validate_name(request, "last_name")


# Contact validations
def primary_contact_validation(request):
    return validators.validate_contact(request, "primary_contact")


def secondary_contact_validation(request):
    return validators.validate_contact(request, "secondary_contact")
