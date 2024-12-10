from allauth.account.forms import LoginForm
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_recaptcha.fields import ReCaptchaField, ReCaptchaV3
from . import models


class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        exclude = (
            "date_joined",
            "last_login",
            "is_superuser",
            "is_active",
            "is_staff",
        )


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        exclude = (
            "date_joined",
            "last_login",
            "is_superuser",
            "is_staff",
        )


class CustomLoginForm(LoginForm):
    captcha = ReCaptchaField(
        widget=ReCaptchaV3,
    )

    def login(self, *args, **kwargs):
        return super(CustomLoginForm, self).login(*args, **kwargs)


#     def save(self, request):
#         user = super().save(request)
#         user.is_staff = True
#         user.save()
#         return user


class QualificationForm(forms.ModelForm):
    class Meta:
        model = models.Qualification
        fields = (
            "qualification_type",
            "title",
            "institution",
            "year_started",
            "year_ended",
            "file",
        )


class CertificationForm(forms.ModelForm):
    class Meta:
        model = models.Certification
        fields = (
            "title",
            "institution",
            "institution_website",
            "obtained_date",
            "expiry_date",
            "file",
            "certification_id",
        )


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = models.Experience
        fields = (
            "job_title",
            "company_name",
            "url",
            "company_reference",
            "start_date",
            "end_date",
            "description",
            "file",
        )
