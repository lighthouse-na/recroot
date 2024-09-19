from typing import Dict, List

from allauth.account.admin import EmailAddressAdmin as BaseEmailAddressAdmin
from allauth.account.models import EmailAddress
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from django.http import HttpRequest
from django.urls import URLPattern, path
from unfold.admin import ModelAdmin, StackedInline
from unfold.sites import UnfoldAdminSite

from apps.finaid.admin import (
    BursaryAdvertAdmin,
    BursaryApplicationsAdmin,
    FinancialAssistanceAdmin,
    FinancialAssistanceAdvertAdmin,
)
from apps.finaid.models import (
    BursaryAdvert,
    BursaryApplication,
    FinancialAssistanceAdvert,
    FinancialAssistanceApplication,
)
from apps.organisation.admin import CostCentreAdmin, PositionAdmin, RegionAdmin
from apps.organisation.models import CostCentre, Location, Position, Region
from apps.pages.models import Announcement
from apps.recruitment.admin import (
    ApplicationAdmin,
    InterviewAdmin,
    SubscriberAdmin,
    VacancyAdmin,
)
from apps.recruitment.models import (
    Application,
    Interview,
    Subscriber,
    Vacancy,
    VacancyType,
)

from .forms import ProfileUpdateForm
from .models import Certification, Profile, Qualification

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(EmailAddress)


class ProfileInline(StackedInline):
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


@admin.register(Qualification)
class QualificationAdmin(ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        profile = Profile.objects.get(user=request.user)
        return qs.filter(user=profile)


@admin.register(Certification)
class CertificationAdmin(ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        profile = Profile.objects.get(user=request.user)
        return qs.filter(user=profile)


class QualificationInline(StackedInline):
    model = Qualification
    extra = 1
    tab = True


class CertificationInline(StackedInline):
    model = Certification
    extra = 1
    tab = True


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    form = ProfileUpdateForm
    # inlines = [QualificationInline, CertificationInline]
    readonly_fields = [
        "salary_reference_number",
        "position",
        "cost_centre",
        "gender",
        "date_of_birth",
        "date_appointed",
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    # def get_inline_instances(self, request, obj=None):
    #     if (
    #         request.user.is_staff
    #         and request.user.is_active
    #         and request.user.is_authenticated
    #     ):
    #         return [
    #             QualificationInline(self.model, self.admin_site),
    #             CertificationInline(self.model, self.admin_site),
    #         ]
    #     return super().get_inline_instances(request, obj)

    # def get_formsets(self, request, obj=None):

    #     if (
    #         request.user.is_staff
    #         and request.user.is_active
    #         and request.user.is_authenticated
    #     ):

    #         for inline in self.get_inline_instances(request, obj):

    #             if isinstance(inline, (QualificationInline, CertificationInline)):

    #                 yield inline.get_formset(request, obj)

    #     else:

    #         return super().get_formsets(request, obj)


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
superuser_dashboard_site.register(Profile, ProfileAdmin)
superuser_dashboard_site.register(
    FinancialAssistanceAdvert, FinancialAssistanceAdvertAdmin
)
superuser_dashboard_site.register(Announcement, ModelAdmin)
