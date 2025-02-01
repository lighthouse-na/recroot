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


class Qualification(models.Model):
    class QualificationType(models.TextChoices):
        PHD = "phd", "Doctorate(PHD)"
        MD = "md", "Doctor of Medicine (MD)"
        JD = "jd", "Juris Doctor (JD)"
        FELLOWSHIP = "fellowship", "Fellowship"
        MASTERS = "masters", "Masters"
        POSTGRADUATE_DIPLOMA = "postgraduate_diploma", "Postgraduate Diploma"
        GRADUATE_CERTIFICATE = "graduate_certificate", "Graduate Certificate"
        HONOURS = "honours", "Honours"
        BACHELORS = "bachelors", "Bachelors"
        ASSOCIATE_DEGREE = "associate_degree", "Associate Degree"
        ADVANCED_DIPLOMA = "advanced_diploma", "Advanced Diploma"
        DIPLOMA = "diploma", "Diploma"
        CERTIFICATE = "certificate", "Certificate"
        TRADE_CERTIFICATE = "trade_certificate", "Trade Certificate"
        VOCATIONAL_QUALIFICATION = (
            "vocational_qualification",
            "Vocational Qualification",
        )
        TECHNICAL_DIPLOMA = "technical_diploma", "Technical Diploma"
        ARTISAN = "artisan", "Artisan"
        APPRENTICESHIP = "apprenticeship", "Apprenticeship"
        CONTINUING_EDUCATION = "continuing_education", "Continuing Education"
        EXECUTIVE_EDUCATION = "executive_education", "Executive Education"
        HIGH_SCHOOL_DIPLOMA = "high_school_diploma", "High School Diploma"
        GED = "ged", "General Educational Development (GED)"
        PROFESSIONAL_CERTIFICATION = (
            "professional_certification",
            "Professional Certification",
        )
        LICENSURE = "licensure", "Licensure"
        GRADE_12 = "grade12", "Grade 12"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="qualifications"
    )
    qualification_type = models.CharField(
        max_length=50, choices=QualificationType.choices
    )
    title = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    year_started = models.PositiveSmallIntegerField()
    year_ended = models.PositiveSmallIntegerField()
    file = models.FileField(upload_to="accounts/qualifications")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.qualification_type} {self.title}"

    # def save(self, *args, **kwargs):
    #     self.title = self.title.lower()
    #     self.institution = self.institution.lower()
    #     super().save(*args, **kwargs)


class Certification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="certifications"
    )
    title = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    institution_website = models.URLField()
    obtained_date = models.DateField()
    expiry_date = models.DateField(blank=True, null=True)
    file = models.FileField(upload_to="accounts/certifications")
    certification_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.title = self.title.lower()
        self.institution = self.institution.lower()
        super().save(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        self.job_title = self.job_title.lower()
        self.company_name = self.company_name.lower()
        self.company_reference = self.company_reference.lower()
        super().save(*args, **kwargs)
