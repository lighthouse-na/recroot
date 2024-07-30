from datetime import date, timedelta

from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils import timezone
from tinymce.widgets import TinyMCE
from unfold.widgets import UnfoldAdminSelectWidget

from .models import (Application, ApplicationRequirementAnswer, Interview,
                     Subscriber, Vacancy, VacancyType)


class VacancyForm(forms.ModelForm):
    functions_responsibilities = forms.CharField(
        label="Functions and Responsibilities", widget=TinyMCE
    )
    remarks = forms.CharField(
        label="Remarks", widget=TinyMCE
    )
    town = forms.MultipleChoiceField(widget=FilteredSelectMultiple("Towns", False))

    class Meta:
        model = Vacancy
        exclude = ["slug", "created_at", "updated_at"]


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = (
            "vacancy",
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "primary_contact",
            "secondary_contact",
            "date_of_birth",
            "cv",
        )


class SubscriberForm(forms.ModelForm):
    vacancy_types = forms.ModelMultipleChoiceField(
        queryset=VacancyType.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Subscriber
        fields = ("email", "vacancy_types")


class InterviewForm(forms.ModelForm):
    application = forms.ModelChoiceField(
        queryset=Application.objects.filter(status=Application.STATUS.ACCEPTED),
        widget=UnfoldAdminSelectWidget,
    )

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

        return schedule_datetime
