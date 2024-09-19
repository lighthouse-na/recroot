from rest_framework import routers

from ..views.recruitment import (
    ApplicationViewSet,
    InterviewViewSet,
    MinimumRequirementAnswerViewSet,
    MinimumRequirementViewSet,
    SubscriberViewSet,
    VacancyTypeViewSet,
    VacancyViewSet,
)

recruitment_router = routers.DefaultRouter()
recruitment_router.register(r"vacancy_types", VacancyTypeViewSet)
recruitment_router.register(r"vacancies", VacancyViewSet)
recruitment_router.register(r"applications", ApplicationViewSet)
recruitment_router.register(r"minimum_requirements", MinimumRequirementViewSet)
recruitment_router.register(
    r"minimum_requirement_answers", MinimumRequirementAnswerViewSet
)
recruitment_router.register(r"interviews", InterviewViewSet)
recruitment_router.register(r"subscribers", SubscriberViewSet)
