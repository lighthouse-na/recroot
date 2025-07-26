from django.urls import path

from . import validation, views

app_name = "recruitment"

validation_urls = [
    path(
        "first_name_validation",
        validation.first_name_validation,
        name="first_name_validation",
    ),
    path(
        "middle_name_validation",
        validation.middle_name_validation,
        name="middle_name_validation",
    ),
    path(
        "last_name_validation",
        validation.last_name_validation,
        name="last_name_validation",
    ),
    path(
        "primary_contact_validation",
        validation.primary_contact_validation,
        name="primary_contact_validation",
    ),
    path(
        "secondary_contact_validation",
        validation.secondary_contact_validation,
        name="secondary_contact_validation",
    ),
]

urlpatterns = [
    path("", views.VacancyListView.as_view(), name="vacancy_list"),
    # path(
    #     "vacancy/<slug>/detail/",
    #     views.VacancyDetailView.as_view(),
    #     name="vacancy_detail",
    # ),
    # path("<slug>/apply", views.ApplicationCreateView.as_view(), name="apply"),
    path("<slug>/apply", views.ApplicationCreateView.as_view(), name="vacancy_detail"),
    path(
        "<str:pk>/invitation",
        views.InterviewResponseView.as_view(),
        name="interview_invitation",
    ),
    path("success/", views.application_success, name="application_success"),
    path(
        "interview_response_success/",
        views.interview_response_success,
        name="interview_response_success",
    ),
    path(
        "applications/<uuid:pk>/contact/edit/",
        views.ApplicationContactUpdateView.as_view(),
        name="application_contact_update",
    ),
    path(
        "applications/",
        views.ApplicationsListView.as_view(),
        name="applications_list",
    ),
]

urlpatterns += validation_urls
