from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from tinymce.models import HTMLField

from apps.organisation.models import CostCentre, Position


class User(AbstractUser):
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


class Qualification(models.Model):

    QUALIFICATION_TYPE = [
        ("phd", "Doctorate(PHD)"),
        ("md", "Doctor of Medicine (MD)"),
        ("jd", "Juris Doctor (JD)"),
        ("fellowship", "Fellowship"),
        ("masters", "Masters"),
        ("postgraduate_diploma", "Postgraduate Diploma"),
        ("graduate_certificate", "Graduate Certificate"),
        ("honours", "Honours"),
        ("bachelors", "Bachelors"),
        ("associate_degree", "Associate Degree"),
        ("advanced_diploma", "Advanced Diploma"),
        ("diploma", "Diploma"),
        ("certificate", "Certificate"),
        ("trade_certificate", "Trade Certificate"),
        ("vocational_qualification", "Vocational Qualification"),
        ("technical_diploma", "Technical Diploma"),
        ("artisan", "Artisan"),
        ("apprenticeship", "Apprenticeship"),
        ("continuing_education", "Continuing Education"),
        ("executive_education", "Executive Education"),
        ("high_school_diploma", "High School Diploma"),
        ("ged", "General Educational Development (GED)"),
        ("professional_certification", "Professional Certification"),
        ("licensure", "Licensure"),
        ("grade12", "Grade 12"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="qualifications"
    )
    qualification_type = models.CharField(max_length=50, choices=QUALIFICATION_TYPE)
    title = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    year_started = models.PositiveSmallIntegerField()
    year_ended = models.PositiveSmallIntegerField()
    file = models.FileField(upload_to="accounts/qualifications")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.qualification_type} {self.title}"


class Certification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="certifications"
    )
    title = models.CharField(max_length=255)
    institute = models.CharField(max_length=255)
    obtained_date = models.DateField()
    expiry_date = models.DateField(blank=True, null=True)
    file = models.FileField(upload_to="accounts/certifications")
    certification_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class Experience(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="experience"
    )
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    company_reference = models.CharField(max_length=255, blank=True, null=True)
    description = HTMLField(
        help_text="Job Description.",
    )
    url = models.URLField(blank=True, null=True)
    file = models.FileField(upload_to="accounts/experience/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.job_title

    # def clean(self):
    #     super().clean()
    #     if self.is_present:
    #         if self.end_date is not None:
    #             raise ValidationError(
    #                 {
    #                     "end_date": "End date should not be provided if the experience is marked as present."
    #                 }
    #             )
    #     else:
    #         if self.end_date is None:
    #             raise ValidationError(
    #                 {
    #                     "end_date": "End date must be provided if the experience is not marked as present."
    #                 }
    #             )
