from datetime import date, timedelta

from django import forms
from django.apps import apps  
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

        def _init_(self, *args, **kwargs):
         super()._init_(*args, **kwargs)
        
        Town = apps.get_model('recruitment', 'Town')
        self.fields['town'].queryset = Town.objects.all() 


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
        ("on_hold", "On Hold"),
        ("ACK_WITH_TIMELINE", "Acknowledgment With Timeline")
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
    trade_specialty = forms.CharField(required=False)
    tertiary_institution = forms.CharField(max_length=255)
    field_of_study = forms.CharField(max_length=255)
    trade_speciality = forms.CharField(max_length=255)
    NQF_level_or_level = forms.IntegerField()

    

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
            "tertiary_institution",
            "field_of_study",
            "trade_speciality",
            "NQF_level_or_level"
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
        """
        schedule_datetime = self.cleaned_data.get("schedule_datetime")

        if not schedule_datetime:
            raise forms.ValidationError("Scheduled datetime cannot be empty.")

        now = timezone.localtime()

        # In the past
        if schedule_datetime <= now:
            raise forms.ValidationError("Scheduled datetime cannot be in the past.")

        # Same day
        if schedule_datetime.date() == now.date():
            raise forms.ValidationError("Scheduled datetime cannot be on the same day.")

        # Weekend
        if schedule_datetime.weekday() >= 5:
            raise forms.ValidationError("Scheduled datetime cannot fall on a weekend (Saturday or Sunday).")

        # Less than 1 day ahead
        if (schedule_datetime.date() - now.date()).days < 1:
            raise forms.ValidationError("Scheduled datetime must be at least one day in the future.")

        # Time check (between 8:00 and 17:00)
        if not (8 <= schedule_datetime.hour < 17):
            raise forms.ValidationError("Scheduled time must be between 8:00 AM and 5:00 PM.")

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
