import uuid
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import UniqueConstraint
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import AutoSlugField
from phonenumber_field.modelfields import PhoneNumberField
from tinymce.models import HTMLField

from datetime import timedelta, datetime

from apps.organisation.models import Location, Town
from apps.utils.validators import FileValidator



# **********************************************************************************************
#                                       VACANCY
# **********************************************************************************************
class VacancyType(models.Model):
    class VacancyTypes(models.TextChoices):
        APPRENTICESHIP = "apprenticeship", "Apprenticeship"
        INTERNSHIP = "internship", "Internship"
        PERMANENT = "permanent", "Permanent"
        PART_TIME = "part_time", "Part Time"
        CONTRACT = "contract", "Contract"
        GRADUATE = "graduate", "Graduate"
        VOLUNTEER = "volunteer", "Volunteer"

    type = models.CharField(max_length=50, choices=VacancyTypes.choices, unique=True)

    def __str__(self) -> str:
        return self.type


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
    title = models.CharField(max_length=255, help_text="Enter the title of the vacancy.")
    vacancy_type = models.ForeignKey(VacancyType, on_delete=models.SET_NULL, null=True)
    pay_grade = models.CharField(max_length=3, blank=True)
    content = HTMLField(
        verbose_name="Functions and Responsibilities",
        help_text="Enter the functions and responsibilities of the vacancy.",
    )
    town = models.ManyToManyField(
        'organisation.Town',
        help_text="Select the town(s) where the vacancy is located.",
    )
    remarks = HTMLField(blank=True, help_text="Enter any additional remarks about the vacancy.")
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
        # BOOL = "bool"
        DATE = "date"
        SELECT = "select"
        # MULTISELECT = "multiselect"

    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="requirements")
    title = models.CharField(max_length=255, verbose_name="Requirement")
    question_type = models.CharField(max_length=50, choices=QuestionType.choices, default=QuestionType.TEXT)
    is_internal = models.BooleanField(default=False)
    is_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class SelectQuestionTypeOptions(models.Model):
    requirement = models.ForeignKey(MinimumRequirement, on_delete=models.CASCADE, related_name="options")
    option = models.CharField(max_length=255)

    def __str__(self):
        return self.option

    def clean(self):
        if (
            self.requirement.question_type != MinimumRequirement.QuestionType.SELECT
            and self.requirement.question_type != MinimumRequirement.QuestionType.MULTISELECT
        ):
            raise ValidationError("This field is only available for select type questions.")
        return super().clean()


# **********************************************************************************************
#                                       APPLICATION
# **********************************************************************************************
class Application(models.Model):
    class STATUS(models.TextChoices):
        SUBMITTED = "submitted"
        ACCEPTED = "accepted"
        REJECTED = "rejected"
        ACK_WITH_TIMELINE = "ACK_WITH_TIMELINE"
        ON_HOLD= "on_hold"


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.PROTECT, related_name="applications")
    status = models.CharField(max_length=20, choices=STATUS.choices, default=STATUS.SUBMITTED)
    submitted_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=255, help_text="Enter your first name")
    middle_name = models.CharField(max_length=255, blank=True, null=True, help_text="Enter your middle name")
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
    tertiary_institution = models.CharField(max_length=255,help_text="Enter tertiary institution", default=" ")
    field_of_study = models.CharField(max_length=255,help_text="Enter field of study",  default=" ")
    trade_speciality = models.CharField(max_length=255,help_text="Enter Speciality or Trade", default=" ")
    NQF_level_or_level = models.IntegerField(
    default=4,  # or another suitable level
    help_text="Enter NQF level or Trade level"
)



    applicable_role = models.CharField(
    max_length=255,
    help_text="Enter the job title for roles in a similar environment.",
    default=" "
)

    applicable_experience = models.IntegerField(
    help_text="Enter years of experience in a similar environment (e.g. 1).",
    default=0
)

    non_applicable_role = models.CharField(
    max_length=255,
    help_text="Enter the job title for other relevant roles you've held.",
    default=" "
)

    non_applicable_experience = models.IntegerField(
    help_text="Enter years of experience in other relevant roles (e.g. 1).",
    default=0
)

    references_name = models.CharField(
        max_length=255,
        help_text="Enter References name",
        default=" "
    )
    references_position = models.CharField(
        max_length=255,
        help_text="Enter References position",
        default=" "
    )
    references_company = models.CharField(
        max_length=255,
        help_text="Enter References company",
        default=" "
    )
    references_email = models.CharField(
        max_length=255,
        help_text="Enter References email",
        default=" "
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
                - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
            )
            if age < 18:
                raise ValidationError("Applicant must be at least 18 years old")

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


# apps/recruitment/models.py



class Interview(models.Model):
    class STATUS(models.TextChoices):
        RESCHEDULED = "rescheduled", "Rescheduled"
        SCHEDULED = "scheduled", "Scheduled"
        DONE = "done", "Done"
        CANCELED = "canceled", "Canceled"
        WAITING = "waiting", "Waiting"
        REJECTED = "rejected", "Rejected"
        ACCEPTED = "accepted", "Accepted"

    class InterviewTypes(models.TextChoices): 
        INDIVIDUAL = "individual", "Individual"
        GROUP = "group", "Group"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    type = models.CharField(
        max_length=20,
        choices=InterviewTypes.choices,
        default=InterviewTypes.INDIVIDUAL,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS.choices,
        default=STATUS.SCHEDULED,
        blank=True
    )

    application = models.ForeignKey(
        'recruitment.Application',  # use 'app_label.ModelName' if in another app
        on_delete=models.CASCADE, 
        related_name="interviews"
    )

    schedule_datetime = models.DateTimeField(
        help_text=_("Please select a date and time at least one day in the future, excluding weekends."),
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True,
        null=True,
        help_text=_("What do you want the interviewee to know before attending the interview?")
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    response = models.CharField(max_length=255, blank=True, null=True)
    response_deadline = models.DateTimeField(blank=True, null=True)
    response_date = models.DateTimeField(blank=True, null=True)

    location = models.ForeignKey(
        'organisation.Town',  # use app_label.ModelName if model is in another app
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="interviews"
    )

    reschedule_date = models.DateField(blank=True, null=True)

    vacancy = models.ForeignKey(
        'recruitment.Vacancy',  # use app_label.ModelName if model is in another app
        on_delete=models.CASCADE, 
        related_name="interviews",
        null=True,
        blank=True
    )

    timestamp = models.DateTimeField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        try:
            return f"{self.application.vacancy.title} - {self.application.first_name} {self.application.last_name}"
        except Exception:
            return f"Interview {self.id}"

    def clean(self):
        if not self.schedule_datetime:
            raise ValidationError("Scheduled datetime cannot be empty.")

        now = timezone.localtime()

        if self.schedule_datetime <= now:
            raise ValidationError("Scheduled datetime cannot be in the past.")

        if self.schedule_datetime.date() == now.date():
            raise ValidationError("Scheduled datetime cannot be on the same day.")

        if self.schedule_datetime.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
            raise ValidationError("Scheduled datetime cannot be on weekends.")

    def update_no_response_status(self):
        if self.response_deadline and self.response_deadline < timezone.now():
            self.status = self.STATUS.WAITING  # or "no_response" if you add that to STATUS
            self.save()

    def save(self, *args, **kwargs):
        self.clean()
        if self.schedule_datetime:
            self.response_deadline = self.schedule_datetime - timedelta(days=2)
        super().save(*args, **kwargs)
