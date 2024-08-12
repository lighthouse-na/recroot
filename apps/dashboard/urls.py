from django.urls import include, path
from .recruitment import recruitment_admin_site
from .admin import admin_dashboard_site
from .finaid import finaid_admin_site

urlpatterns = [
    path("admin/", admin_dashboard_site.urls),
    path("recruitment/", recruitment_admin_site.urls),
    path("finaid/", finaid_admin_site.urls),
]
