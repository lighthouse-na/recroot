from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from apps.accounts.admin import superuser_dashboard_site

urlpatterns = (
    [
        path("accounts/", include("allauth.urls")),
        path("accounts/", include("apps.accounts.urls")),
        path("tinymce/", include("tinymce.urls")),
        path("", include("apps.pages.urls")),
        path("recruitment/", include("apps.recruitment.urls")),
        path("dashboard/", include("apps.dashboard.urls")),
        path("utils/", include("apps.utils.urls")),
    ]
    # + debug_toolbar_urls()
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
    urlpatterns.append(path("admin/", superuser_dashboard_site.urls, name="superuser"))
    urlpatterns.append(path("__reload__/", include("django_browser_reload.urls")))
else:
    urlpatterns.append(path("oshimashakula/", superuser_dashboard_site.urls, name="superuser"))
