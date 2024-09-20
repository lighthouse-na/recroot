from allauth.account.forms import SignupForm
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        exclude = (
            "username",
            "date_joined",
            "last_login",
            "password",
            "is_superuser",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        exclude = (
            "username",
            "date_joined",
            "last_login",
            "password",
            "is_superuser",
        )


class CustomSignupForm(SignupForm): ...


#     def save(self, request):
#         user = super().save(request)
#         user.is_staff = True
#         user.save()
#         return user


# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         exclude = ["user"]
