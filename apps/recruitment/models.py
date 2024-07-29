from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField
from apps.organisation.models import Town
from django.contrib.auth.models import User
from datetime import date
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField


class Vacancy(models.Model):
    title = models.CharField(max_length=255)
    functions_responsibilities = HTMLField()
    town = models.ForeignKey(Town, on_delete=models.PROTECT)
    remarks = HTMLField(blank=True)
    deadline = models.DateTimeField()
    is_public = models.BooleanField(default=False)
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
        return reverse("vacancy_detail", kwargs={"pk": self.pk})


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

    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=20, choices=STATUS.choices, default=STATUS.SUBMITTED
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    primary_contact = PhoneNumberField(
        region="NA",
        help_text="Enter a valid Namibian phone number",
    )
    secondary_contact = PhoneNumberField(
        region="NA",
        blank=True,
        help_text="Enter a valid Namibian phone number",
    )
    date_of_birth = models.DateField()

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
