from allauth.account.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy


# Create your views here.
class CustomLoginView(LoginView):
    template_name = "account/login.html"


class AdminLoginView(CustomLoginView):
    success_url = "/dashboard/admin/"


class StaffLoginView(CustomLoginView):
    success_url = "/dashboard/staff/"


class RecruiterLoginView(CustomLoginView):
    success_url = "/dashboard/recruiter/"


class FinaidLoginView(CustomLoginView):
    success_url = "/dashboard/finaid/"
