from django.contrib import admin

from apps.recruitment.admin import (
    ApplicationAdmin,
    InterviewAdmin,
    SubscriberAdmin,
    VacancyAdmin,
)
from apps.recruitment.models import Application, Interview, Subscriber, Vacancy


class RecruitmentAdminArea(admin.AdminSite):
    site_header = "Recruitment Admin"
    site_title = "Recruitment"
    index_title = "Recruitment Dashboard"
    index_template = ""
    enable_nav_sidebar = False
    login_template = "admin/login.html"
    logout_template = "admin/logout.html"
    password_change_template = "admin/password_change.html"

    def has_permission(self, request):
        return (
            request.user.is_active
            and request.user.is_authenticated
            and request.user.groups.filter(name="recruiter").exists()
        )


recruitment_admin_site = RecruitmentAdminArea(name="Recruitment")
recruitment_admin_site.register(Application, ApplicationAdmin)
recruitment_admin_site.register(Vacancy, VacancyAdmin)
recruitment_admin_site.register(Interview, InterviewAdmin)
recruitment_admin_site.register(Subscriber, SubscriberAdmin)
