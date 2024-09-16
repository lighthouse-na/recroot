from django.urls import include, path
from .routers import *

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("accounts/", include(accounts.urls)),
    path("organisation/", include(organisation.urls)),
    path("recruitment/", include(recruitment.urls)),
]
