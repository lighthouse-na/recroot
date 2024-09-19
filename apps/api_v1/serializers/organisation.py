from rest_framework import serializers

from apps.organisation.models import (
    CostCentre,
    Department,
    Division,
    Location,
    Position,
    Region,
    Town,
)


class RegionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Region
        fields = ["name"]


class TownSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Town
        fields = ["region", "name"]


class DivisionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Division
        fields = ["name"]


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Department
        fields = ["division", "name"]


class CostCentreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CostCentre
        fields = ["number"]


class PositionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Position
        fields = [
            "department",
            "line_manager",
            "name",
            "is_manager",
        ]


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = [
            "title",
            "address",
            "town",
        ]
