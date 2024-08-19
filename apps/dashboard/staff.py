from datetime import datetime

from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.recruitment.models import Vacancy


class StaffDashboard(admin.AdminSite):
    site_header = "Staff Dashboard"
    site_title = "Staff Dashboard"
    # index_title = "Staff Dashboard"
    index_template = "dashboard/staff/index.html"
    enable_nav_sidebar = False
    login_template = "admin/login.html"
    logout_template = "admin/logout.html"
    password_change_template = "admin/password_change.html"

    def index(self, request, extra_context=None):
        vacancies = Vacancy.objects.filter(
            is_published=True, deadline__gt=datetime.now()
        ).order_by("-created_at")
        extra_context = {"vacancies": vacancies, "title": request.user.profile}
        return super().index(request, extra_context)

    def has_permission(self, request):
        return request.user.is_active and request.user.is_authenticated


staff_dashboard_site = StaffDashboard(name="Staff")
