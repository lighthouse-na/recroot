from datetime import date, timedelta

from django import forms
from django.contrib import messages
from django.utils import timezone
from phonenumber_field.formfields import PhoneNumberField
from tinymce.widgets import TinyMCE
from unfold.widgets import UnfoldAdminSelectWidget

from .models import (
    Application,
    Interview,
    MinimumRequirement,
    MinimumRequirementAnswer,
    SelectQuestionTypeOptions,
    Vacancy,
)

# **********************************************************************************************
#                                       VACANCY
# **********************************************************************************************


class MinimumRequirementsAddForm(forms.ModelForm):
    class Meta:
        model = MinimumRequirement
        fields = ["title", "question_type", "is_internal", "is_required"]


class VacancyForm(forms.ModelForm):
    content = forms.CharField(label="Content", widget=TinyMCE())
    remarks = forms.CharField(label="Remarks", widget=TinyMCE())

    class Meta:
        model = Vacancy
        exclude = ["slug", "created_at", "updated_at"]


class SelectQuestionTypeOptionsForm(forms.ModelForm):
    class Meta:
        model = SelectQuestionTypeOptions
        fields = ("option",)


# **********************************************************************************************
#                                       APPLICATION
# **********************************************************************************************
class ApplicationReviewForm(forms.ModelForm):
    STATUS_CHOICES = (
        ("accepted", "Accept"),
        ("rejected", "Reject"),
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=UnfoldAdminSelectWidget())

    class Meta:
        model = Application
        fields = ["status", "review_comments"]


class ApplicationForm(forms.ModelForm):
    # captcha = ReCaptchaField(
    #     public_key=env("RECAPTCHA_V2_PUBLIC_KEY"),
    #     private_key=env("RECAPTCHA_V2_PRIVATE_KEY"),
    #     widget=ReCaptchaV2Invisible,
    # )
    primary_contact = PhoneNumberField(region="NA")
    secondary_contact = PhoneNumberField(region="NA", required=False)
    date_of_birth = forms.DateField(widget=forms.DateInput())

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
            "gender",
            "cv",
        )

    def __init__(self, vacancy, *args, **kwargs):
        self.vacancy = vacancy
        self.requirements = MinimumRequirement.objects.filter(vacancy=vacancy)
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        # We will keep track of the fields that are being added
        fields_to_remove = []

        for requirement in self.requirements:
            # Only display requirements that are internal if the request is from the intranet
            if requirement.is_internal and not self.request.is_intranet:
                fields_to_remove.append(f"requirement_{requirement.id}")
                continue  # Skip this requirement if it's internal and the user is not on the intranet

            if requirement.question_type == MinimumRequirement.QuestionType.TEXT:
                self.fields[f"requirement_{requirement.id}"] = forms.CharField(
                    label=requirement.title,
                    required=requirement.is_required,
                )

            elif requirement.question_type == MinimumRequirement.QuestionType.DATE:
                self.fields[f"requirement_{requirement.id}"] = forms.DateField(
                    label=requirement.title,
                    required=requirement.is_required,
                    widget=forms.DateInput(attrs={"type": "date"}),
                )

            elif requirement.question_type == MinimumRequirement.QuestionType.SELECT:
                self.fields[f"requirement_{requirement.id}"] = forms.ChoiceField(
                    label=requirement.title,
                    required=requirement.is_required,
                    choices=[(str(option.option), str(option.option)) for option in requirement.options.all()],
                    widget=forms.Select(),
                )
                self.fields[f"requirement_{requirement.id}"].is_select = True

            # elif requirement.question_type == MinimumRequirement.QuestionType.MULTISELECT:
            #     self.fields[f"requirement_{requirement.id}"] = forms.ChoiceField(
            #         label=requirement.title,
            #         choices=[(option.id, str(option.option)) for option in requirement.options.all()],
            #         widget=forms.SelectMultiple(),
            #         required=requirement.is_required,
            #     )
            #     self.fields[f"requirement_{requirement.id}"].is_multiselect = True

    def clean_date_of_birth(self):
        dob = self.cleaned_data["date_of_birth"]
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        if age < 18:
            messages.error(self.request, "You must be at least 18 years old to apply.")

        return dob


class MinimumRequirementAnswerForm(forms.ModelForm):
    class Meta:
        model = MinimumRequirementAnswer
        fields = ["requirement", "answer"]


# **********************************************************************************************
#                                       INTERVIEW
# **********************************************************************************************
class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ("application", "schedule_datetime", "description", "location")

    def clean_schedule_datetime(self):
        """
        Validates the 'schedule_datetime' field to ensure it meets the required conditions.

        This method checks the following conditions:
        - The scheduled datetime cannot be in the past.
        - The scheduled datetime cannot be on the same day.
        - The scheduled datetime cannot fall on weekends (Saturday or Sunday).
        - The scheduled datetime must be at least one day in the future.
        - The scheduled time must be between 8:00 AM and 5:00 PM.
        - The scheduled time cannot be later than 5:00 PM or earlier than 8:00 AM.

        Raises:
            forms.ValidationError: If any of the conditions are not met.

        Returns:
            schedule_datetime (datetime): The validated scheduled datetime.
        """
        schedule_datetime = self.cleaned_data["schedule_datetime"]

        # Check if the scheduled datetime is empty
        if not schedule_datetime:
            raise forms.ValidationError("Scheduled datetime cannot be empty.")

        # Check if the scheduled datetime is in the past
        if schedule_datetime <= timezone.now():
            raise forms.ValidationError("Scheduled datetime cannot be in the past.")

        # Check if the scheduled datetime is on the same day
        if schedule_datetime.date() == timezone.now().date():
            raise forms.ValidationError("Scheduled datetime cannot be on the same day.")

        # Check if the scheduled datetime is on the weekend
        if schedule_datetime.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
            raise forms.ValidationError("Scheduled datetime cannot be on weekends.")

        # Check if the scheduled datetime is less than one day in the future
        if schedule_datetime.date() - timezone.now().date() < timedelta(days=1):
            raise forms.ValidationError("Scheduled datetime must be at least one day in the future.")

        # Check if the scheduled time is within working hours (8 AM to 5 PM)
        if schedule_datetime.hour < 8 or schedule_datetime.hour > 16:
            raise forms.ValidationError("Scheduled time must be between 8am and 5pm.")

        # Check if the scheduled time is exactly at 5 PM or earlier than 8 AM
        if schedule_datetime.hour == 17:
            raise forms.ValidationError("Scheduled time cannot be later than 5pm.")

        if schedule_datetime.hour == 7:
            raise forms.ValidationError("Scheduled time cannot be earlier than 8am.")

        return schedule_datetime


class InterviewInvitationResponseForm(forms.ModelForm):
    STATUS_CHOICES = (
        ("accepted", "Accept"),
        ("rejected", "Reject"),
        # ("reschedule", "Reschedule"),
    )
    # captcha = ReCaptchaField(
    #     public_key=env("RECAPTCHA_V2_PUBLIC_KEY"),
    #     private_key=env("RECAPTCHA_V2_PRIVATE_KEY"),
    #     widget=ReCaptchaV2Invisible,
    # )
    status = forms.ChoiceField(choices=STATUS_CHOICES)
    # reschedule_date = forms.DateField(
    #     widget=forms.DateInput(attrs={"type": "date"}), required=False
    # )

    class Meta:
        model = Interview
        fields = ("status",)
