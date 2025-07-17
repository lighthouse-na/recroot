from django import forms
from tinymce.widgets import TinyMCE

from .models import FAQ


class FAQForm(forms.ModelForm):
    answer = forms.CharField(widget=TinyMCE())

    class Meta:
        model = FAQ
        fields = "__all__"
