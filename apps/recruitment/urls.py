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
     path(
        "tertiary_institution_validation",
        validation.tertiary_institution_validation,
        name="tertiary_institution_validation",
    ),
    path(
        "field_of_study_validation",
        validation.field_of_study_validation,
        name="field_of_study_validation",
    ),
    path(
        "trade_speciality_validation",
        validation.trade_speciality_validation,
        name="trade_speciality_validation",
    ),
    path(
        "NQF_level_or_level_validation",
        validation.NQF_level_or_level_validation,
        name="NQF_level_or_level_validation",
    ),
    path(
        "applicable_role_validation",
        validation.applicable_role_validation,
        name="applicable_role_validation",
    ),
    path(
        "applicable_experience_validation",
        validation.applicable_experience_validation,
        name="applicable_experience_validation",
    ),
    
    path(
        "non_applicable_role_validation",
        validation.non_applicable_role_validation,
        name="non_applicable_role_validation",
    ),
    path(
        "non_applicable_experience_validation",
        validation.non_applicable_experience_validation,
        name="non_applicable_experience_validation",
    ),
    
     path(
        "references_name_validation",
        validation.references_name_validation,
        name="references_name_validation",
    ),
     path(
        "references_position_validation",
        validation.references_position_validation,
        name="references_position_validation",
    ),
    path(
        "references_company_validation",
        validation.references_company_validation,
        name="references_company_validation",
    ),
    path(
        "references_email_validation",
        validation.references_email_validation,
        name="references_email_validation",
    )


    
    
    
    
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
        "applications/",
        views.ApplicationsListView.as_view(),
        name="applications_list",
    ),
   path("<slug>/interview", views.InterviewFormView.as_view(), name="interview_form")
    
]

urlpatterns += validation_urls
