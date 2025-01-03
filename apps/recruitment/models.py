import uuid
from datetime import date, datetime, timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, MaxValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import AutoSlugField
from phonenumber_field.modelfields import PhoneNumberField
from tinymce.models import HTMLField

from apps.organisation.models import Location, Town
from apps.utils.validators import FileValidator


# **********************************************************************************************
#                                       VACANCY
# **********************************************************************************************
class VacancyType(models.Model):
    class VACANCY_TYPE(models.TextChoices):
        APPRENTICESHIP = "apprenticeship"
        INTERNSHIP = "internship"
        PERMANENT = "permanent"
        PART_TIME = "part_time"
        CONTRACT = "contract"
        GRADUATE = "graduate"
        VOLUNTEER = "volunteer"

    type = models.CharField(max_length=50, choices=VACANCY_TYPE.choices, unique=True)

    def __str__(self):
        return self.type.upper()


class Vacancy(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    advert = models.FileField(
        upload_to="adverts/vacancy/",
        validators=[
            FileExtensionValidator(allowed_extensions=["pdf"]),
            FileValidator(max_size=10 * 1024 * 1024),
        ],
        blank=True,
        help_text="Please upload a PDF file, maximum size 10MB.",
    )
    title = models.CharField(
        max_length=255, help_text="Enter the title of the vacancy."
    )
    vacancy_type = models.ForeignKey(VacancyType, on_delete=models.SET_NULL, null=True)
    pay_grade = models.CharField(max_length=3, blank=True)
    content = HTMLField(
        verbose_name="Functions and Responsibilities",
        help_text="Enter the functions and responsibilities of the vacancy.",
    )
    town = models.ManyToManyField(
        Town,
        help_text="Select the town(s) where the vacancy is located.",
    )
    remarks = HTMLField(
        blank=True, help_text="Enter any additional remarks about the vacancy."
    )
    deadline = models.DateTimeField(help_text="Enter the deadline for the vacancy.")
    is_public = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    slug = AutoSlugField(unique=True, populate_from=["title", "id"])
    reviewers = models.ManyToManyField(
        get_user_model(),
        help_text="Reviewers will be able to see applications submitted for this vacancy.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Vacancies"

    def __str__(self):
        return self.title

    # def clean(self):
    #     if self.deadline and self.deadline < timezone.now():
    #         raise ValidationError({"deadline": "Deadline cannot be set before today."})

    def get_absolute_url(self):
        return reverse("recruitment:vacancy_detail", args=[self.slug])


class MinimumRequirement(models.Model):
    class QuestionType(models.TextChoices):
        TEXT = "text"
        BOOL = "bool"
        DATE = "date"
        SELECT = "select"
        MULTISELECT = "multiselect"

    vacancy = models.ForeignKey(
        Vacancy, on_delete=models.CASCADE, related_name="requirements"
    )
    title = models.CharField(max_length=255, verbose_name="Requirement")
    question_type = models.CharField(
        max_length=50, choices=QuestionType.choices, default=QuestionType.BOOL
    )
    is_internal = models.BooleanField(default=False)
    is_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class SelectQuestionTypeOptions(models.Model):
    requirement = models.ForeignKey(
        MinimumRequirement, on_delete=models.CASCADE, related_name="options"
    )
    option = models.CharField(max_length=255)

    def __str__(self):
        return self.option

    def clean(self):
        if (
            self.requirement.question_type != MinimumRequirement.QuestionType.SELECT
            and self.requirement.question_type
            != MinimumRequirement.QuestionType.MULTISELECT
        ):
            raise ValidationError(
                "This field is only available for select type questions."
            )
        return super().clean()


# **********************************************************************************************
#                                       APPLICATION
# **********************************************************************************************
class Application(models.Model):
    class STATUS(models.TextChoices):
        SUBMITTED = "submitted"
        ACCEPTED = "accepted"
        REJECTED = "rejected"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vacancy = models.ForeignKey(
        Vacancy, on_delete=models.PROTECT, related_name="applications"
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
    email = models.EmailField(help_text="Enter your email address")
    primary_contact = PhoneNumberField(
        region="NA",
        help_text="Enter a valid Namibian phone number",
    )
    secondary_contact = PhoneNumberField(
        region="NA",
        blank=True,
        null=True,
        help_text="Enter a valid Namibian phone number",
    )
    date_of_birth = models.DateField(help_text="Enter your data if birth")
    gender = models.CharField(
        help_text="Select your gender",
        default="",
        max_length=10,
        choices=(("male", "Male"), ("female", "Female")),
    )
    cv = models.FileField(
        upload_to="cv/",
        validators=[
            FileExtensionValidator(allowed_extensions=["pdf", "docx"]),
            FileValidator(max_size=10 * 1024 * 1024),
        ],
        help_text="Please upload a PDF/DOCX file, maximum size 10MB.",
    )
    is_internal = models.BooleanField(default=False)
    user = models.ForeignKey(
        get_user_model(),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="applications",
    )
    reviewers = models.ManyToManyField(get_user_model())
    reviewed_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="reviewed_applications",
    )
    reviewed_at = models.DateTimeField(blank=True, null=True)
    review_comments = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.vacancy.title} - {self.first_name} {self.last_name}"

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

        # if timezone.now() > self.vacancy.deadline:
        #     raise ValidationError(
        #         {"submitted_at": "Applications cannot be accepted past the deadline."}
        #     )

    # def save(self, *args, **kwargs):
    #     if timezone.now() > self.vacancy.deadline:
    #         raise ValidationError(
    #             {"submitted_at": "Applications cannot be accepted past the deadline."}
    #         )
    #     super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("application_detail", kwargs={"pk": self.pk})

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["vacancy", "primary_contact"],
                name="unique_vacancy_primary_contact",
            ),
        ]


class MinimumRequirementAnswer(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    requirement = models.ForeignKey(MinimumRequirement, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.requirement.title


# **********************************************************************************************
#                                       INTERVIEW
# **********************************************************************************************


class Interview(models.Model):
    class STATUS(models.TextChoices):
        RESCHEDULED = "rescheduled"
        SCHEDULED = "scheduled"
        DONE = "done"
        CANCELED = "canceled"
        WAITING = "Waiting"
        REJECTED = "rejected"
        ACCEPTED = "accepted"

    class INTERVIEW_TYPE(models.TextChoices): ...

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name="interviews"
    )
    schedule_datetime = models.DateTimeField(
        help_text=_(
            "Please select a date and time at least one day in the future, excluding weekends."
        ),
        blank=True,
    )
    status = models.CharField(max_length=20, choices=STATUS.choices, blank=True)
    description = models.TextField(
        blank=True,
        help_text=_(
            "What do you want the interviewee to know before attending the interview?"
        ),
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    response = models.CharField(max_length=255, blank=True, null=True)
    response_deadline = models.DateTimeField(blank=True, null=True)
    response_date = models.DateTimeField(blank=True, null=True)
    location = models.ForeignKey(
        Location,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="interviews",
    )
    reschedule_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.application.vacancy.title} - {self.application.first_name} {self.application.last_name}"

    def clean(self):
        if self.schedule_datetime <= timezone.now():
            raise ValidationError("Scheduled datetime cannot be in the past.")

        if self.schedule_datetime.date() == timezone.now().date():
            raise ValidationError("Scheduled datetime cannot be on the same day.")

        if self.schedule_datetime.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
            raise ValidationError("Scheduled datetime cannot be on weekends.")

        # if self.schedule_datetime.date() - timezone.now().date() < timedelta(days=3):
        #     raise ValidationError(
        #         "Scheduled datetime must be at least three(3) days in the future."
        #     )

        # if self.application.vacancy.deadline < timezone.now():
        #     raise ValidationError(
        #         "Cannot schedule an interview before the vacancy deadline"
        #     )

    def update_no_response_status(self):
        if self.response_deadline and self.response_deadline < datetime.now():
            self.status = "no_response"
            self.save()

    def save(self, *args, **kwargs):
        self.clean()
        if self.schedule_datetime:
            self.response_deadline = self.schedule_datetime - timedelta(days=2)
        super().save(*args, **kwargs)


# **********************************************************************************************
#                                       SUBSCRIBER
# **********************************************************************************************
class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    vacancy_types = models.ManyToManyField(VacancyType, related_name="subscribers")
    subscribed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
