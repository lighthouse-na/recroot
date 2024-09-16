from rest_framework import permissions, viewsets
from apps.recruitment.models import (
    Vacancy,
    VacancyType,
    MinimumRequirementAnswer,
    MinimumRequirement,
    Application,
    Subscriber,
    Interview,
)
from ..serializers.recruitment import (
    VacancySerializer,
    VacancyTypeSerializer,
    MinimumRequirementAnswerSerializer,
    MinimumRequirementSerializer,
    ApplicationSerializer,
    SubscriberSerializer,
    InterviewSerializer,
)


class VacancyTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows VacancyTypes to be viewed or edited.
    """

    queryset = VacancyType.objects.all()
    serializer_class = VacancyTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class VacancyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Vacancies to be viewed or edited.
    """

    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = [permissions.IsAuthenticated]


class MinimumRequirementViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows MinimumRequirements to be viewed or edited.
    """

    queryset = MinimumRequirement.objects.all()
    serializer_class = MinimumRequirementSerializer
    permission_classes = [permissions.IsAuthenticated]


class MinimumRequirementAnswerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows MinimumRequirementAnswers to be viewed or edited.
    """

    queryset = MinimumRequirementAnswer.objects.all()
    serializer_class = MinimumRequirementAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Applications to be viewed or edited.
    """

    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]


class InterviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Interviews to be viewed or edited.
    """

    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer
    permission_classes = [permissions.IsAuthenticated]


class SubscriberViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Subscribers to be viewed or edited.
    """

    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    permission_classes = [permissions.IsAuthenticated]
