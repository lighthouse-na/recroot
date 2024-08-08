from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import include, path
from apps.recruitment.admin import recruitment_admin_site
from apps.accounts.admin import admin_dashboard_site
urlpatterns = [
    path("superuser/", admin.site.urls),
    path("admin/", admin_dashboard_site.urls),
    path("recruitment/", recruitment_admin_site.urls),
    path("tinymce/", include("tinymce.urls")),
    path("", include("apps.pages.urls")),
] + debug_toolbar_urls()
