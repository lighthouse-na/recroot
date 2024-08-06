from datetime import timedelta

from django import forms
from django.utils import timezone
from phonenumber_field.formfields import PhoneNumberField
from tinymce.widgets import TinyMCE

from .models import (
    ApplicantResponse,
    Application,
    Interview,
    MinimumRequirement,
    Subscriber,
    Vacancy,
    VacancyType,
)

# **********************************************************************************************
#                                       VACANCY
# **********************************************************************************************


class MinimumRequirementsAddForm(forms.ModelForm):
    class Meta:
        model = MinimumRequirement
        fields = ["title", "question_type"]


class MinimumRequirementsAnswerForm(forms.ModelForm):
    class Meta:
        model = MinimumRequirement
        fields = ["answer"]


class VacancyForm(forms.ModelForm):
    functions_responsibilities = forms.CharField(
        label="Functions and Responsibilities", widget=TinyMCE
    )
    remarks = forms.CharField(label="Remarks", widget=TinyMCE)

    class Meta:
        model = Vacancy
        exclude = ["slug", "created_at", "updated_at"]


# **********************************************************************************************
#                                       APPLICATION
# **********************************************************************************************
class ApplicationReviewForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["status", "review_comments"]


class ApplicationForm(forms.ModelForm):
    primary_contact = PhoneNumberField(region="NA")
    secondary_contact = PhoneNumberField(region="NA", required=False)
    date_of_birth = forms.DateField(widget=forms.DateInput)

    class Meta:
        model = Application
        fields = (
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "primary_contact",
            "secondary_contact",
            "date_of_birth",
            "cv",
        )


class ApplicantResponseForm(forms.ModelForm):
    class Meta:
        model = ApplicantResponse
        fields = ["requirement", "answer"]


# **********************************************************************************************
#                                       INTERVIEW
# **********************************************************************************************
class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ("application", "schedule_datetime", "description")

    def clean_schedule_datetime(self):
        schedule_datetime = self.cleaned_data["schedule_datetime"]

        if schedule_datetime <= timezone.now():
            raise forms.ValidationError("Scheduled datetime cannot be in the past.")

        if schedule_datetime.date() == timezone.now().date():
            raise forms.ValidationError("Scheduled datetime cannot be on the same day.")

        if schedule_datetime.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
            raise forms.ValidationError("Scheduled datetime cannot be on weekends.")

        if schedule_datetime.date() - timezone.now().date() < timedelta(days=1):
            raise forms.ValidationError(
                "Scheduled datetime must be at least one day in the future."
            )

        if schedule_datetime.hour < 8 or schedule_datetime.hour > 16:
            raise forms.ValidationError("Scheduled time must be between 8am and 5pm.")

        if schedule_datetime.hour == 17:
            raise forms.ValidationError("Scheduled time cannot be later than 5pm.")

        if schedule_datetime.hour == 7:
            raise forms.ValidationError("Scheduled time cannot be earlier than 8am.")

        return schedule_datetime


class InterviewInvitationResponseForm(forms.ModelForm):
    STATUS_CHOICES = (("accepted", "Accept"), ("rejected", "Reject"))
    status = forms.ChoiceField(choices=STATUS_CHOICES)

    class Meta:
        model = Interview
        fields = ("status", "response")


# **********************************************************************************************
#                                       SUBSCRIBER
# **********************************************************************************************
class SubscriberForm(forms.ModelForm):
    vacancy_types = forms.ModelMultipleChoiceField(
        queryset=VacancyType.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Subscriber
        fields = ("email", "vacancy_types")
