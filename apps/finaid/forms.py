from django import forms
from tinymce.widgets import TinyMCE

from .models import BursaryAdvert, BursaryApplication, FinancialAssistanceApplication


class FinancialAssistanceApplicationForm(forms.ModelForm):
    class Meta:
        model = FinancialAssistanceApplication
        exclude = [
            "advert",
            "applicant",
            "reviewed_by",
            "reviewed_at",
            "review_comments",
            "status",
            "created_at",
            "updated_at",
        ]


class BursaryApplicationForm(forms.ModelForm):
    class Meta:
        model = BursaryApplication
        exclude = [
            "bursary",
            "status",
            "is_visible",
            "created_at",
            "updated_at",
        ]


class BursaryAdvertForm(forms.ModelForm):
    description = forms.CharField(
        label="Bursary description", required=True, widget=TinyMCE
    )

    class Meta:
        model = BursaryAdvert
        exclude = [
            "created_at",
            "updated_at",
        ]
