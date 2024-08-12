from django.urls import include, path

from .admin import admin_dashboard_site
from .finaid import finaid_admin_site
from .recruitment import recruitment_admin_site
from .staff import staff_dashboard_site

urlpatterns = [
    path("admin/", admin_dashboard_site.urls),
    path("recruitment/", recruitment_admin_site.urls),
    path("finaid/", finaid_admin_site.urls),
    path("staff/", staff_dashboard_site.urls),
]
