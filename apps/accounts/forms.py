from allauth.account.forms import LoginForm
from django import forms
from django.contrib.auth import get_user_model
from django_recaptcha.fields import ReCaptchaField, ReCaptchaV3

from unfold.widgets import UnfoldAdminPasswordInput
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
            "password",
        )


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        exclude = (
            "date_joined",
            "last_login",
            "is_superuser",
            "is_staff",
            "password",
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
