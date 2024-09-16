from rest_framework import routers

from ..views.organisation import (
    RegionViewSet,
    TownViewSet,
    DepartmentViewSet,
    DivisionViewSet,
    LocationViewSet,
    CostCentreViewSet,
)

organisation_router = routers.DefaultRouter()
organisation_router.register(r"regions", RegionViewSet)
organisation_router.register(r"towns", TownViewSet)
organisation_router.register(r"departments", DepartmentViewSet)
organisation_router.register(r"divisions", DivisionViewSet)
organisation_router.register(r"locations", LocationViewSet)
organisation_router.register(r"cost_centres", CostCentreViewSet)
