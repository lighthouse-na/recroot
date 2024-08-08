from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import include, path
from apps.recruitment.admin import recruitment_admin_site
urlpatterns = [
    path("admin/", admin.site.urls),
    path("recruitment/", recruitment_admin_site.urls),
    path("tinymce/", include("tinymce.urls")),
    path("", include("apps.pages.urls")),
] + debug_toolbar_urls()
