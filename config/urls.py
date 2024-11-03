from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.accounts.admin import superuser_dashboard_site

urlpatterns = (
    [
        path("accounts/", include("allauth.urls")),
        path("accounts/", include("apps.accounts.urls")),
        # path("admin/", admin.site.urls),
        # path("admin/", superuser_dashboard_site.urls),
        path("tinymce/", include("tinymce.urls")),
        path("", include("apps.pages.urls")),
        path("recruitment/", include("apps.recruitment.urls")),
        path("dashboard/", include("apps.dashboard.urls")),
        path("finaid/", include("apps.finaid.urls")),
        path("api-auth/", include("rest_framework.urls")),
        path("api/v1/", include("apps.api_v1.urls")),
        path("staff/", include("apps.staff.urls")),
        path("utils/", include("apps.utils.urls")),
    ]
    # + debug_toolbar_urls()
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
    urlpatterns += [path("admin/", superuser_dashboard_site.urls)]
else:
    urlpatterns += [path("oshimashakula/", superuser_dashboard_site.urls)]
