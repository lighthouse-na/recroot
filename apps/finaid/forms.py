from django import forms

from .models import FinancialAssistanceApplication


class FinancialAssistanceApplicationForm(forms.ModelForm):
    class Meta:
        model = FinancialAssistanceApplication
        exclude = [
            "status",
            "created_at",
            "updated_at",
        ]
