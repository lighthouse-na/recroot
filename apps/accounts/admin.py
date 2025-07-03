from typing import List

from allauth.account.admin import EmailAddressAdmin as BaseEmailAddressAdmin
from allauth.account.models import EmailAddress
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.urls import URLPattern, path
from import_export.admin import ExportActionModelAdmin
from unfold.admin import ModelAdmin, TabularInline
from unfold.sites import UnfoldAdminSite

# from apps.accounts.models import User
from apps.organisation.admin import CostCentreAdmin, PositionAdmin, RegionAdmin
from apps.organisation.models import (
    CostCentre,
    Department,
    Division,
    Location,
    Position,
    Region,
)
from apps.pages.models import FAQ, Announcement
from apps.recruitment.admin import (
    ApplicationAdmin,
    InterviewAdmin,
    RequirementsAdmin,
    VacancyAdmin,
)
from apps.recruitment.models import (
    Application,
    Interview,
    MinimumRequirement,
    Vacancy,
    VacancyType,
)

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User

# Unregister default admin configurations for Group and EmailAddress
admin.site.unregister(Group)
admin.site.unregister(EmailAddress)


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin): ...


@admin.register(EmailAddress)
class EmailAddressAdmin(BaseEmailAddressAdmin, ModelAdmin): ...


class DepartmentInline(TabularInline):
    model = Department
    extra = 1


class DivisionAdmin(ModelAdmin):
    inlines = [DepartmentInline]


@admin.register(get_user_model())
class UserAdmin(ModelAdmin, ExportActionModelAdmin):
    form = CustomUserCreationForm
    form_add = CustomUserChangeForm

    filter_horizontal = ["groups", "user_permissions"]
    list_display = [
        "first_name",
        "last_name",
        "email",
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request).exclude(is_superuser=True)

        if request.user.is_superuser or request.user.groups.filter(name="admin").exists():
            return qs.exclude(email="AnonymousUser")
        return qs.filter(user=request.user)

    def has_add_permission(self, request):
        if request.user.is_superuser or request.user.groups.filter(name="admin").exists():
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.groups.filter(name="admin").exists():
            return True
        return False


class SuperuserDashboard(UnfoldAdminSite):
    """
    Custom admin site for superusers.

    This admin site is specifically designed for superuser access,
    providing a customised interface for superusers to manage the site.
    It includes custom templates for login, logout, and password change,
    and has permissions restricted to superusers only.
    """

    site_header = "SuperUser Dashboard"
    site_title = "SuperUser Dashboard"
    index_title = "SuperUser Dashboard"
    # index_template = "admin/index.html"  # Custom index template can be enabled if needed
    enable_nav_sidebar = True
    login_template = "admin/login.html"
    logout_template = "admin/logout.html"
    password_change_template = "admin/password_change.html"

    def has_permission(self, request):
        """
        Checks if the current user has permission to access the admin site.

        Only active, authenticated superusers are granted access.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            bool: True if the user is active, authenticated, and a superuser, otherwise False.
        """
        return request.user.is_active and request.user.is_authenticated and request.user.is_superuser

    def get_urls(self) -> List[URLPattern]:
        """
        Returns the URL patterns for the superuser dashboard.

        The custom URLs include the original admin site URLs, but with a
        custom index page for superusers.

        Returns:
            List[URLPattern]: A list of URL patterns, including the default admin URLs.
        """
        urlpatterns = super().get_urls()  # Include the original URLs
        urlpatterns += [
            path("", admin.site.urls),  # Ensure the original admin site URLs are included
        ]
        return urlpatterns 


# Create an instance of the custom SuperuserDashboard
superuser_dashboard_site = SuperuserDashboard(name="SuperUser")

# Register models with the SuperuserDashboard instance.
superuser_dashboard_site.register(Site, ModelAdmin)
superuser_dashboard_site.register(User, UserAdmin)
superuser_dashboard_site.register(Group, GroupAdmin)
superuser_dashboard_site.register(EmailAddress, EmailAddressAdmin)
superuser_dashboard_site.register(Region, RegionAdmin)
superuser_dashboard_site.register(Location, ModelAdmin)
superuser_dashboard_site.register(Vacancy, VacancyAdmin)
superuser_dashboard_site.register(Application, ApplicationAdmin)
superuser_dashboard_site.register(Interview, InterviewAdmin)
superuser_dashboard_site.register(VacancyType, ModelAdmin)
superuser_dashboard_site.register(Position, PositionAdmin)
superuser_dashboard_site.register(CostCentre, CostCentreAdmin)
superuser_dashboard_site.register(Announcement, ModelAdmin)
superuser_dashboard_site.register(FAQ, ModelAdmin)
superuser_dashboard_site.register(Division, DivisionAdmin)
superuser_dashboard_site.register(MinimumRequirement, RequirementsAdmin)
