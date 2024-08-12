from django.contrib import admin
from unfold.admin import ModelAdmin


class StaffDashboard(admin.AdminSite):
    site_header = "Staff Dashboard"
    site_title = "Staff Dashboard"
    index_title = "Staff Dashboard"
    index_template = "dashboard/staff/index.html"
    enable_nav_sidebar = False
    login_template = "admin/login.html"
    logout_template = "admin/logout.html"
    password_change_template = "admin/password_change.html"

    def has_permission(self, request):
        return request.user.is_active and request.user.is_authenticated


staff_dashboard_site = StaffDashboard(name="Staff")
