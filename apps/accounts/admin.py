from allauth.account.admin import EmailAddressAdmin as BaseEmailAddressAdmin
from allauth.account.models import EmailAddress
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from unfold.admin import ModelAdmin, TabularInline

from apps.organisation.admin import RegionAdmin
from apps.organisation.models import Region
from apps.recruitment.admin import ApplicationAdmin, InterviewAdmin, VacancyAdmin
from apps.recruitment.models import (
    Application,
    Interview,
    Location,
    Vacancy,
    VacancyType,
)
from .models import Profile

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


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin): ...


@admin.register(EmailAddress)
class EmailAddressAdmin(BaseEmailAddressAdmin, ModelAdmin): ...


class AdminDashboard(admin.AdminSite):
    site_header = "Admin Dashboard"
    site_title = "Admin Dashboard"
    index_title = "Admin Dashboard"
    index_template = "account/admin/index.html"
    enable_nav_sidebar = False
    login_template = "account/admin/login.html"
    logout_template = "account/admin/logout.html"
    password_change_template = "account/admin/password_change.html"

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
