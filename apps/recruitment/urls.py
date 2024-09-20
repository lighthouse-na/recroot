from django.urls import path

from . import views

app_name = "recruitment"

urlpatterns = [
    path("", views.VacancyListView.as_view(), name="vacancy_list"),
    path(
        "vacancy/<slug>/detail/",
        views.VacancyDetailView.as_view(),
        name="vacancy_detail",
    ),
    path("<slug>/apply", views.ApplicationCreateView.as_view(), name="apply"),
    path(
        "<str:pk>/invitation",
        views.InterviewResponseView.as_view(),
        name="interview_invitation",
    ),
    path("subscribe/", views.SubscribeCreateView.as_view(), name="subscriber_create"),
    path("success/", views.application_success, name="application_success"),
]
