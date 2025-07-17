from unfold.sites import UnfoldAdminSite

from apps.recruitment.admin import (
    ApplicationAdmin,
    InterviewAdmin,
    VacancyAdmin,
)
from apps.recruitment.models import Application, Interview, Vacancy

from .views import RecruiterLoginView


class RecruitmentAdminArea(UnfoldAdminSite):
    site_header = "Recruitment Admin"
    site_title = "Recruitment"
    index_title = "Recruitment Dashboard"
    index_template = "admin/index.html"
    enable_nav_sidebar = False

    def login(self, request, extra_context=None):
        return RecruiterLoginView.as_view()(request)

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
