from django.core.exceptions import ValidationError
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
