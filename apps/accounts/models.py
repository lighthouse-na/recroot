from django.contrib.auth.models import User
from django.db import models

from apps.organisation.models import CostCentre, Position


class Profile(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE, related_name="profile"
    )
    picture = models.ImageField(upload_to="profile/picture", blank=True, null=True)
    salary_reference_number = models.PositiveIntegerField(blank=True, null=True)
    position = models.ForeignKey(
        Position,
        on_delete=models.PROTECT,
        related_name="profiles",
        blank=True,
        null=True,
    )
    cost_centre = models.ForeignKey(
        CostCentre,
        on_delete=models.PROTECT,
        related_name="profiles",
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
    cv = models.FileField(upload_to="profile/cv", blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


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
        Profile, on_delete=models.CASCADE, related_name="qualifications"
    )
    qualification_type = models.CharField(max_length=50, choices=QUALIFICATION_TYPE)
    title = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    date_completed = models.DateField()
    file = models.FileField(upload_to="accounts/qualifications")

    def __str__(self) -> str:
        return f"{self.qualification_type} {self.title}"


class Certification(models.Model):
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="certifications"
    )
    title = models.CharField(max_length=255)
    institute = models.CharField(max_length=255)
    obtained_date = models.DateField()
    expiry_date = models.DateField(blank=True, null=True)
    file = models.FileField(upload_to="accounts/certifications")
    certification_id = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title
