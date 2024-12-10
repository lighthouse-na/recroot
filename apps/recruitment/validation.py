from apps.utils import validators
from django.http import HttpResponse


# Name validations
def first_name_validation(request) -> HttpResponse:
    """
    Validates the 'first_name' field in the request.

    Args:
        request (HttpRequest): The HTTP request containing the data to validate.

    Returns:
        HttpResponse: A response indicating whether the validation was successful or failed.
    """
    return validators.validate_name(request, "first_name")


def middle_name_validation(request) -> HttpResponse:
    """
    Validates the 'middle_name' field in the request.

    Args:
        request (HttpRequest): The HTTP request containing the data to validate.

    Returns:
        HttpResponse: A response indicating whether the validation was successful or failed.
    """
    return validators.validate_name(request, "middle_name")


def last_name_validation(request) -> HttpResponse:
    """
    Validates the 'last_name' field in the request.

    Args:
        request (HttpRequest): The HTTP request containing the data to validate.

    Returns:
        HttpResponse: A response indicating whether the validation was successful or failed.
    """
    return validators.validate_name(request, "last_name")


# Contact validations
def primary_contact_validation(request) -> HttpResponse:
    """
    Validates the 'primary_contact' field in the request.

    Args:
        request (HttpRequest): The HTTP request containing the data to validate.

    Returns:
        HttpResponse: A response indicating whether the validation was successful or failed.
    """
    return validators.validate_contact(request, "primary_contact")


def secondary_contact_validation(request) -> HttpResponse:
    """
    Validates the 'secondary_contact' field in the request.

    Args:
        request (HttpRequest): The HTTP request containing the data to validate.

    Returns:
        HttpResponse: A response indicating whether the validation was successful or failed.
    """
    return validators.validate_contact(request, "secondary_contact")
