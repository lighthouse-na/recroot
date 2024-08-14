from typing import List
from allauth.account.admin import EmailAddressAdmin as BaseEmailAddressAdmin
from allauth.account.models import EmailAddress
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from django.urls import URLPattern
from unfold.admin import ModelAdmin, TabularInline
from unfold.sites import UnfoldAdminSite
from django.urls import path
from .models import Profile


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


admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(EmailAddress)


class ProfileInline(TabularInline):
    model = Profile
    can_delete = False
    max_num = 1
    extra = 0
    tab = True


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    readonly_fields = ["is_superuser", "date_joined", "last_login"]
    inlines = [ProfileInline]

    def has_add_permission(self, request):
        return False


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin): ...


@admin.register(EmailAddress)
class EmailAddressAdmin(BaseEmailAddressAdmin, ModelAdmin): ...


class SuperuserDashboard(UnfoldAdminSite):
    site_header = "SuperUser Dashboard"
    site_title = "SuperUser Dashboard"
    index_title = "SuperUser Dashboard"
    # index_template = "admin/index.html"
    enable_nav_sidebar = True
    login_template = "admin/login.html"
    logout_template = "admin/logout.html"
    password_change_template = "admin/password_change.html"

    def has_permission(self, request):
        return (
            request.user.is_active
            and request.user.is_authenticated
            and request.user.is_superuser
        )

    def get_urls(self) -> List[URLPattern]:
        urlpatterns = super().get_urls()  # include the original URLs
        urlpatterns += [
            path("", admin.site.urls),
        ]
        return urlpatterns


superuser_dashboard_site = SuperuserDashboard(name="SupeUser")
superuser_dashboard_site.register(User, UserAdmin)
superuser_dashboard_site.register(Group, GroupAdmin)
superuser_dashboard_site.register(EmailAddress, EmailAddressAdmin)
superuser_dashboard_site.register(Region, RegionAdmin)
superuser_dashboard_site.register(Location, ModelAdmin)
superuser_dashboard_site.register(Vacancy, VacancyAdmin)
superuser_dashboard_site.register(Application, ApplicationAdmin)
superuser_dashboard_site.register(Interview, InterviewAdmin)
superuser_dashboard_site.register(VacancyType, ModelAdmin)
superuser_dashboard_site.register(Subscriber, SubscriberAdmin)
superuser_dashboard_site.register(Position, PositionAdmin)
superuser_dashboard_site.register(CostCentre, CostCentreAdmin)
superuser_dashboard_site.register(BursaryAdvert, BursaryAdvertAdmin)
superuser_dashboard_site.register(BursaryApplication, BursaryApplicationsAdmin)
superuser_dashboard_site.register(
    FinancialAssistanceApplication, FinancialAssistanceAdmin
)
