from django.contrib import admin
from import_export.admin import ExportActionModelAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.import_export.forms import SelectableFieldsExportForm

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


class FinaidAminArea(admin.AdminSite):
    site_header = "Financial Aid Admin"
    site_title = "Financial Aid"
    index_title = "Financial Aid Dashboard"
    index_template = ""
    enable_nav_sidebar = False
    login_template = "admin/login.html"
    logout_template = "admin/logout.html"
    password_change_template = "admin/password_change.html"

    def has_permission(self, request):
        return (
            request.user.is_active
            and request.user.is_authenticated
            and request.user.groups.filter(name="finaid").exists()
        )


finaid_admin_site = FinaidAminArea(name="Financial Aid")
finaid_admin_site.register(BursaryAdvert, BursaryAdvertAdmin)
finaid_admin_site.register(BursaryApplication, BursaryApplicationsAdmin)
finaid_admin_site.register(FinancialAssistanceApplication, FinancialAssistanceAdmin)
