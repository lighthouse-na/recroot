from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    username = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    primary_contact = PhoneNumberField(
        region="NA",
        help_text="Enter a valid Namibian phone number",
    )
    secondary_contact = PhoneNumberField(
        region="NA",
        blank=True,
        help_text="Enter a valid Namibian phone number",
    )

    USERNAME_FIELD = "email"  # Set email as the authentication field
    REQUIRED_FIELDS = []  # No additional required fields

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        """Ensure a default password is set if no password exists."""
        if not self.pk and not self.password:  # Only set password for new users
            default_password = "Password1"
            self.set_password(default_password)
        super().save(*args, **kwargs)  # Call the original save method
