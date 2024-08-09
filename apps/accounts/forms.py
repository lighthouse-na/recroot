from allauth.account.forms import SignupForm
from django.utils.translation import gettext_lazy as _


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        user.is_staff = True
        user.save()
        return user