from rest_framework import serializers
from apps.recruitment.models import (
    Vacancy,
    VacancyType,
    MinimumRequirement,
    MinimumRequirementAnswer,
    Application,
    Interview,
    Subscriber,
)


class VacancyTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VacancyType
        fields = ["type"]


class VacancySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vacancy
        fields = [
            "advert",
            "title",
            "vacancy_type",
            "pay_grade",
            "functions_responsibilities",
            "town",
            "remarks",
            "is_public",
            "is_public",
            "is_published",
            "slug",
            "created_at",
            "updated_at",
        ]


class MinimumRequirementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MinimumRequirement
        fields = ["vacancy", "title", "question_type", "created_at", "updated_at"]


class MinimumRequirementAnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MinimumRequirementAnswer
        fields = ["application", "requirement", "answer"]


class ApplicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Application
        fields = [
            "vacancy",
            "status",
            "submitted_at",
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "primary_contact",
            "secondary_contact",
            "date_of_birth",
            "cv",
            "reviewed_by",
            "reviewed_at",
            "review_comments",
        ]


class InterviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Interview
        fields = [
            "application",
            "schedule_datetime",
            "status",
            "description",
            "created_at",
            "updated_at",
            "response",
            "response_deadline",
            "response_date",
            "location",
        ]


class SubscriberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subscriber
        fields = [
            "email",
            "vacancy_types",
            "subscribed",
            "created_at",
            "unsubscribed_at",
        ]
