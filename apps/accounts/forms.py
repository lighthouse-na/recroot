from allauth.account.forms import SignupForm
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Profile


class CustomSignupForm(SignupForm): ...


#     def save(self, request):
#         user = super().save(request)
#         user.is_staff = True
#         user.save()
#         return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ["user"]
