from django.contrib.auth.models import Group, User
from rest_framework import serializers

from apps.accounts.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            "url",
            "email",
            "groups",
            "password",
            "is_active",
            "is_staff",
            "is_superuser",
            "salary_reference_number",
            "position",
            "cost_centre",
            "gender",
            "date_appointed",
            "date_of_birth",
        ]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class QualificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Qualification
        fields = [
            "url",
            "user",
            "qualification_type",
            "title",
            "institution",
            "date_completed",
            "file",
        ]


class CertificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Certification
        fields = [
            "url",
            "user",
            "expiry_date",
            "institute",
            "obtained_date",
            "certification_id",
            "file",
        ]
