from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField
from apps.organisation.models import Town
from django.contrib.auth.models import User
from datetime import date
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
from django_extensions.db.fields import AutoSlugField
from django.core.validators import FileExtensionValidator, MaxValueValidator


class Vacancy(models.Model):
    advert = models.FileField(
        upload_to="adverts",
        validators=[
            FileExtensionValidator(allowed_extensions=["pdf"]),
            MaxValueValidator(limit_value=10 * 1024 * 1024),
        ],
        blank=True,
        help_text="Please upload a PDF file, maximum size 10MB.",
    )
    title = models.CharField(
        max_length=255, help_text="Enter the title of the vacancy."
    )
    functions_responsibilities = HTMLField(
        help_text="Enter the functions and responsibilities of the vacancy."
    )
    town = models.ForeignKey(
        Town,
        on_delete=models.PROTECT,
        help_text="Select the town where the vacancy is located.",
    )
    remarks = HTMLField(
        blank=True, help_text="Enter any additional remarks about the vacancy."
    )
    deadline = models.DateTimeField(help_text="Enter the deadline for the vacancy.")
    is_public = models.BooleanField(default=False)
    slug = AutoSlugField(unique=True, populate_from=["title", "id"])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("can_add_vacancy", "Can add vacancy"),
            ("can_change_vacancy", "Can change vacancy"),
            ("can_delete_vacancy", "Can delete vacancy"),
        ]
        verbose_name_plural = "Vacancies"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("vacancy_detail", args=[self.slug])


class MinimumRequirement(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name="Requirement")

    def __str__(self):
        return self.title


class Application(models.Model):
    class STATUS(models.TextChoices):
        SUBMITTED = "submitted"
        ACCEPTED = "accepted"
        REJECTED = "rejected"

    vacancy = models.ForeignKey(Vacancy, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=20, choices=STATUS.choices, default=STATUS.SUBMITTED
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=255, help_text="Enter your first name")
    middle_name = models.CharField(max_length=255, help_text="Enter your middle name")
    last_name = models.CharField(max_length=255, help_text="Enter your last name")
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
    cv = models.FileField(
        upload_to="cv/",
        validators=[
            FileExtensionValidator(allowed_extensions=["pdf", "docx"]),
            MaxValueValidator(limit_value=10 * 1024 * 1024),
        ],
        help_text="Please upload a PDF/DOCX file, maximum size 10MB.",
    )

    class Meta:
        permissions = [
            ("can_change_vacancy", "Can change vacancy"),
            ("can_delete_vacancy", "Can delete vacancy"),
        ]

    def __str__(self):
        return self.vacancy

    def clean(self):
        if self.date_of_birth:
            today = date.today()
            age = (
                today.year
                - self.date_of_birth.year
                - (
                    (today.month, today.day)
                    < (self.date_of_birth.month, self.date_of_birth.day)
                )
            )
            if age < 18:
                raise ValidationError("Applicant must be at least 18 years old")

    def get_absolute_url(self):
        return reverse("application_detail", kwargs={"pk": self.pk})


class ApplicationRequirementAnswer(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    requirement = models.ForeignKey(MinimumRequirement, on_delete=models.CASCADE)
    answer = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.application} - {self.requirement}"
