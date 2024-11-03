import re

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.utils.deconstruct import deconstructible


@deconstructible
class FileValidator:
    def __init__(self, max_size=None):
        self.max_size = max_size

    def __call__(self, value):
        if self.max_size is not None and value.size > self.max_size:
            raise ValidationError(
                f"File size exceeds the maximum allowed ({self.max_size} bytes)"
            )

    def __eq__(self, other):
        return self.max_size == other.max_size


# Name validation
invalid_name_response = HttpResponse(
    "<p class='text-red-500 text-xs mt-1'>Invalid: Only letters and spaces allowed</p>"
)

name_pattern = re.compile(r"^[a-zA-Z\s]+$")


def validate_name(request, field_name):
    name = request.POST.get(field_name)

    if not name:
        return HttpResponse("")

    if not name_pattern.match(name):
        return invalid_name_response

    return HttpResponse("")


# Contact validation
invalid_contact_response = HttpResponse(
    "<p class='text-red-500 text-xs mt-1'>Invalid: Enter Valid Namibian Phone Number</p>"
)


# Compile the regex pattern once for better performance
namibian_phone_regex = re.compile(r"^(?:\+264|0)(81|82|85|86|87|88)[0-9]{7}$")


def validate_contact(request, field_name):
    contact = request.POST.get(field_name)

    if not contact:
        return HttpResponse("")

    if not namibian_phone_regex.match(contact):
        return invalid_contact_response

    return HttpResponse("")
