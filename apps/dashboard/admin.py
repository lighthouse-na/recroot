from allauth.account.models import EmailAddress
from django.contrib import admin
from django.contrib.auth.models import Group, User
from unfold.admin import ModelAdmin

from apps.organisation.admin import RegionAdmin, PositionAdmin, CostCentreAdmin
from apps.organisation.models import Region, Position, CostCentre
from apps.recruitment.admin import (
    ApplicationAdmin,
    InterviewAdmin,
    VacancyAdmin,
    SubscriberAdmin,
)
from apps.recruitment.models import (
    Application,
    Interview,
    Location,
    Vacancy,
    VacancyType,
    Subscriber,
)
from apps.finaid.admin import BursaryAdvertAdmin, BursaryApplicationsAdmin, FinancialAssistanceAdmin
from apps.finaid.models import (
    BursaryAdvert,
    BursaryApplication,
    FinancialAssistanceAdvert,
    FinancialAssistanceApplication,
)
from apps.accounts.admin import UserAdmin, GroupAdmin, EmailAddressAdmin

# admin.site.unregister(User)
# admin.site.unregister(Group)
# admin.site.unregister(EmailAddress)


class AdminDashboard(admin.AdminSite):
    site_header = "Admin Dashboard"
    site_title = "Admin Dashboard"
    index_title = "Admin Dashboard"
    # index_template = "account/admin/index.html"
    enable_nav_sidebar = False
    login_template = "admin/login.html"
    logout_template = "admin/logout.html"
    password_change_template = "admin/password_change.html"

    def has_permission(self, request):
        return (
            request.user.is_active and request.user.groups.filter(name="admin").exists()
        )


admin_dashboard_site = AdminDashboard(name="Admin")
admin_dashboard_site.register(User, UserAdmin)
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
