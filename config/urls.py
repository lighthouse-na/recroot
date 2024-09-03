from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import include, path

from apps.accounts.admin import superuser_dashboard_site

urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("apps.accounts.urls")),
    # path("admin/", admin.site.urls),
    path("admin/", superuser_dashboard_site.urls),
    path("tinymce/", include("tinymce.urls")),
    path("", include("apps.pages.urls")),
    path("recruitment/", include("apps.recruitment.urls")),
    path("dashboard/", include("apps.dashboard.urls")),
    path("finaid/", include("apps.finaid.urls")),
] + debug_toolbar_urls()
