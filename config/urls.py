from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import include, path

from apps.accounts.admin import admin_dashboard_site
from apps.recruitment.admin import recruitment_admin_site

urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path("superuser/", admin.site.urls),
    path("admin/", admin_dashboard_site.urls),
    path("recruitment-admin/", recruitment_admin_site.urls),
    path("tinymce/", include("tinymce.urls")),
    path("", include("apps.pages.urls")),
    path("recruitment/", include("apps.recruitment.urls")),
] + debug_toolbar_urls()
