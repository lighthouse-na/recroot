from allauth.account.views import LoginView


# Create your views here.
class CustomLoginView(LoginView):
    template_name = "account/login.html"


class AdminLoginView(CustomLoginView):
    success_url = "/dashboard/admin/"


class StaffLoginView(CustomLoginView):
    success_url = "/dashboard/staff/"


class RecruiterLoginView(CustomLoginView):
    success_url = "/dashboard/recruiter/"
