from rest_framework import routers

from ..views.accounts import (
    CertificationViewSet,
    GroupViewSet,
    ProfileViewSet,
    QualificationViewSet,
    UserViewSet,
)

accounts_router = routers.DefaultRouter()
accounts_router.register(r"users", UserViewSet)
accounts_router.register(r"groups", GroupViewSet)
accounts_router.register(r"profiles", ProfileViewSet)
accounts_router.register(r"qualifications", QualificationViewSet)
accounts_router.register(r"certifications", CertificationViewSet)
