from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets

from apps.accounts.models import Certification, Qualification

from ..serializers.accounts import (
    CertificationSerializer,
    GroupSerializer,
    QualificationSerializer,
    UserSerializer,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class QualificationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Qualifications to be viewed or edited.
    """

    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer
    permission_classes = [permissions.IsAuthenticated]


class CertificationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Certifications to be viewed or edited.
    """

    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    permission_classes = [permissions.IsAuthenticated]
