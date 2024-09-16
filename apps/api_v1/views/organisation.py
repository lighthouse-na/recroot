from rest_framework import permissions, viewsets
from apps.organisation.models import (
    Region,
    Town,
    Department,
    Position,
    Location,
    Division,
    CostCentre,
)
from ..serializers.organisation import (
    RegionSerializer,
    TownSerializer,
    DepartmentSerializer,
    DivisionSerializer,
    LocationSerializer,
    CostCentreSerializer,
)


class RegionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Regions to be viewed or edited.
    """

    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [permissions.IsAuthenticated]


class TownViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Towns to be viewed or edited.
    """

    queryset = Town.objects.all().order_by("name")
    serializer_class = TownSerializer
    permission_classes = [permissions.IsAuthenticated]


class DivisionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Divisions to be viewed or edited.
    """

    queryset = Division.objects.all()
    serializer_class = DivisionSerializer
    permission_classes = [permissions.IsAuthenticated]


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Departments to be viewed or edited.
    """

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class LocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Locations to be viewed or edited.
    """

    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]


class CostCentreViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows CostCentres to be viewed or edited.
    """

    queryset = CostCentre.objects.all()
    serializer_class = CostCentreSerializer
    permission_classes = [permissions.IsAuthenticated]
