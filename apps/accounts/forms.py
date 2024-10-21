from allauth.account.forms import LoginForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from django_recaptcha.fields import ReCaptchaField, ReCaptchaV3
from django_recaptcha.widgets import ReCaptchaV2Invisible

from config.env import env


class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        # fields = "__all__"
        exclude = (
            # "username",
            "date_joined",
            "last_login",
            # "password",
            "is_superuser",
            "is_active",
            "is_staff",
        )


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        # fields = "__all__"
        exclude = (
            # "username",
            "date_joined",
            "last_login",
            # "password",
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


# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         exclude = ["user"]
