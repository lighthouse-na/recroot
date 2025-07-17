from allauth.account.views import LoginView
from django.urls import reverse


# Create your views here.
class CustomLoginView(LoginView):
    template_name = "account/login.html"

    def get_success_url(self):
        user = self.request.user

        if user.groups.filter(name="admin").exists():
            return reverse("Admin:index")

        if user.groups.filter(name="recruiter").exists():
            return reverse("Recruitment:index")

        return None


class AdminLoginView(CustomLoginView): ...


class StaffLoginView(CustomLoginView):
    success_url = "/dashboard/staff/"


class RecruiterLoginView(CustomLoginView): ...
