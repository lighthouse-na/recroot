from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from tinymce.models import HTMLField

from apps.organisation.models import CostCentre, Position


class User(AbstractUser):
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    primary_contact = PhoneNumberField(
        region="NA",
        help_text="Enter a valid Namibian phone number",
    )
    secondary_contact = PhoneNumberField(
        region="NA",
        blank=True,
        help_text="Enter a valid Namibian phone number",
    )
    salary_reference_number = models.PositiveIntegerField(blank=True, null=True)
    position = models.ForeignKey(
        Position,
        on_delete=models.PROTECT,
        related_name="users",
        blank=True,
        null=True,
    )
    cost_centre = models.ForeignKey(
        CostCentre,
        on_delete=models.PROTECT,
        related_name="users",
        blank=True,
        null=True,
    )
    gender = models.CharField(
        max_length=6,
        choices=[("male", "Male"), ("female", "Female")],
        blank=True,
        null=True,
    )
    date_appointed = models.DateField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
