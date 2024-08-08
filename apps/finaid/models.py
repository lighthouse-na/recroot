import datetime
import uuid
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, MaxValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import AutoSlugField
from phonenumber_field.modelfields import PhoneNumberField
from tinymce.models import HTMLField

from apps.accounts.models import Profile
from apps.utils.validators import FileValidator


class Bursary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    advert = models.FileField(
        upload_to="adverts/bursary",
        validators=[
            FileExtensionValidator(allowed_extensions=["pdf"]),
            MaxValueValidator(limit_value=10 * 1024 * 1024),
        ],
        blank=True,
        help_text="Please upload a PDF file, maximum size 10MB.",
    )
    remarks = HTMLField(
        blank=True, help_text="Enter any additional remarks about the vacancy."
    )
    deadline = models.DateTimeField(help_text="Enter the deadline for the bursary.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BursaryApplications(models.Model):
    class STATUS(models.TextChoices):
        SUBMITTED = "submitted"
        ACCEPTED = "accepted"
        REJECTED = "rejected"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bursary = models.ForeignKey(
        Bursary, on_delete=models.PROTECT, related_name="applications"
    )
    status = models.CharField(
        max_length=20, choices=STATUS.choices, default=STATUS.SUBMITTED
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=255, help_text="Enter your first name")
    middle_name = models.CharField(
        max_length=255, blank=True, null=True, help_text="Enter your middle name"
    )
    last_name = models.CharField(max_length=255, help_text="Enter your last name")
    id_number = models.PositiveBigIntegerField()
    date_of_birth = models.DateField()
    email = models.EmailField(help_text="Enter your email address")
    primary_contact = PhoneNumberField(
        region="NA",
        help_text="Enter a valid Namibian phone number",
    )
    secondary_contact = PhoneNumberField(
        region="NA",
        blank=True,
        help_text="Enter a valid Namibian phone number",
    )
    date_of_birth = models.DateField(help_text="Enter your data if birth")
    documents = models.FileField(
        upload_to="bursary/documents",
        validators=[
            FileExtensionValidator(allowed_extensions=["pdf", "docx"]),
            FileValidator(max_size=10 * 1024 * 1024),
        ],
        help_text="Please upload a PDF/DOCX file, maximum size 10MB.",
    )
    motivation_letter = models.TextField(blank=True, null=True)
    is_citizen = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["bursary", "id_number"],
                name="unique_bursary_id_number",
            ),
        ]

    def clean(self):
        if datetime.date.today() - timedelta(days=16 * 365.25) > self.date_of_birth:
            raise ValidationError(
                {"date_of_birth": _("Applicant must be at least 16 years old.")}
            )

        if self.id_number and self.date_of_birth:
            try:
                id_number = int(id_number)
            except ValueError:
                raise ValidationError(
                    {"id_number": [_("ID number must be a valid number")]}
                )

            id_str = str(id_number)

            # Validate the length of id_number
            if len(id_str) != 11:
                raise ValidationError(
                    {"id_number": [_("ID number must be 11 digits long")]}
                )

            # Extract year, month, and day from the ID number
            id_year = int(id_str[:2])
            id_month = int(id_str[2:4])
            id_day = int(id_str[4:6])

            if self.date_of_birth:
                date_month = self.date_of_birth.month
                date_day = self.date_of_birth.day
                date_year = (
                    self.date_of_birth.year % 100
                )  # Extract last two digits of the year

                # Compare the extracted values
                if id_month != date_month or id_day != date_day or id_year != date_year:
                    raise ValidationError(
                        {"id_number": [_("ID number does not match date of birth")]}
                    )
        return super().clean()


class FinancialAssistance(models.Model):
    YEAR_CHOICES = [
        (year, str(year)) for year in range(datetime.date.today().year, 2100)
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    year = models.CharField(max_length=4, choices=YEAR_CHOICES, unique=True)
    deadline = models.DateTimeField()
    remarks = models.TextField(blank=True, null=True)
    is_visible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Financial Assistance for {self.year}"


class FinancialAssistanceApplication(models.Model):

    class STATUS(models.TextChoices):
        PENDING = "pending"
        RECOMMENDED = "recommended"
        REJECTED = "rejected"

    FIELDS = [
        ("business", "Business"),
        ("engineering", "Engineering"),
        ("computer_sciences", "Computer Sciences"),
        ("social_sciences", "Social Sciences"),
        ("natural_sciences", "Natural Sciences"),
        ("humanities", "Humanities"),
        ("education", "Education"),
        ("law", "Law"),
    ]

    QUALIFICATION_TYPE = [
        ("phd", "Doctorate(PHD)"),
        ("masters", "Masters"),
        ("honours", "Honours"),
        ("bachelors", "Bachelors"),
        ("diploma", "Diploma"),
        ("certificate", "Certificate"),
        ("grade12", "Grade 12"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assistance = models.ForeignKey(
        FinancialAssistance, on_delete=models.PROTECT, related_name="applications"
    )
    applicant = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT,
        related_name="financial_assistance_applications",
    )
    highest_qualification_type = models.CharField(
        max_length=50, choices=QUALIFICATION_TYPE
    )
    highest_qualification_title = models.CharField(
        max_length=255, help_text="eg Computer Science"
    )
    intended_institution_for_studies = models.CharField(
        max_length=255, help_text="eg University of Namibia"
    )
    intended_field_of_study = models.CharField(max_length=50, choices=FIELDS)
    study_mode = models.CharField(
        max_length=5,
        choices=[
            ("ft", "Full Time"),
            ("pt", "Part Time"),
            ("d", "Distance"),
            ("h", "Hybrid"),
        ],
    )
    aspired_qualification_type = models.CharField(
        max_length=50, choices=QUALIFICATION_TYPE
    )
    aspired_qualification_title = models.CharField(max_length=255, help_text="eg CCNA")
    estimated_total_loan_amount_per_annum = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Amount must be in Namibian Dollars (NAD/N$)",
    )
    motivation = models.TextField(blank=False, null=False)
    status = models.CharField(
        max_length=50, choices=STATUS.choices, default=STATUS.PENDING
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("assistance", "applicant")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse(
            "financial_assistance_application_detail", kwargs={"pk": self.pk}
        )

    def save(self, *args, **kwargs):
        self.status = self.STATUS.PENDING
        super().save(*args, **kwargs)
