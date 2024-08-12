from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("superuser/", admin.site.urls),
    path("tinymce/", include("tinymce.urls")),
    path("", include("apps.pages.urls")),
    path("recruitment/", include("apps.recruitment.urls")),
    path("dashboard/", include("apps.dashboard.urls")),
] + debug_toolbar_urls()
