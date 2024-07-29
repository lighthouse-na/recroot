# forms.py
from django import forms
from .models import Application, ApplicationRequirementAnswer, Vacancy


class VacancyForm(forms.ModelForm):
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
