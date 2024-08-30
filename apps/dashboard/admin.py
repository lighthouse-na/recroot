from allauth.account.models import EmailAddress
from django.contrib import admin
from django.contrib.auth.models import Group, User
from unfold.admin import ModelAdmin

from apps.accounts.admin import EmailAddressAdmin, GroupAdmin, UserAdmin, ProfileAdmin
from apps.accounts.models import Profile
from apps.finaid.admin import (
    BursaryAdvertAdmin,
    BursaryApplicationsAdmin,
    FinancialAssistanceAdmin,
)
from apps.finaid.models import (
    BursaryAdvert,
    BursaryApplication,
    FinancialAssistanceAdvert,
    FinancialAssistanceApplication,
)
from apps.organisation.admin import CostCentreAdmin, PositionAdmin, RegionAdmin
from apps.organisation.models import CostCentre, Position, Region
from apps.recruitment.admin import (
    ApplicationAdmin,
    InterviewAdmin,
    SubscriberAdmin,
    VacancyAdmin,
)
from apps.recruitment.models import (
    Application,
    Interview,
    Location,
    Subscriber,
    Vacancy,
    VacancyType,
)
from unfold.sites import UnfoldAdminSite

# admin.site.unregister(User)
# admin.site.unregister(Group)
# admin.site.unregister(EmailAddress)


class AdminDashboard(UnfoldAdminSite):
    site_header = "Admin Dashboard"
    site_title = "Admin Dashboard"
    index_title = "Admin Dashboard"
    # index_template = "admin/index.html"
    enable_nav_sidebar = True
    login_template = "admin/login.html"
    logout_template = "admin/logout.html"
    password_change_template = "admin/password_change.html"

    def has_permission(self, request):
        return (
            request.user.is_active
            and request.user.is_authenticated
            and request.user.groups.filter(name="admin").exists()
        )


admin_dashboard_site = AdminDashboard(name="Admin")
admin_dashboard_site.register(User, UserAdmin)
admin_dashboard_site.register(Profile, ProfileAdmin)
admin_dashboard_site.register(Group, GroupAdmin)
admin_dashboard_site.register(EmailAddress, EmailAddressAdmin)
admin_dashboard_site.register(Region, RegionAdmin)
admin_dashboard_site.register(Location, ModelAdmin)
admin_dashboard_site.register(Vacancy, VacancyAdmin)
admin_dashboard_site.register(Application, ApplicationAdmin)
admin_dashboard_site.register(Interview, InterviewAdmin)
admin_dashboard_site.register(VacancyType, ModelAdmin)
admin_dashboard_site.register(Subscriber, SubscriberAdmin)
admin_dashboard_site.register(Position, PositionAdmin)
admin_dashboard_site.register(CostCentre, CostCentreAdmin)
admin_dashboard_site.register(BursaryAdvert, BursaryAdvertAdmin)
admin_dashboard_site.register(BursaryApplication, BursaryApplicationsAdmin)
admin_dashboard_site.register(FinancialAssistanceApplication, FinancialAssistanceAdmin)
