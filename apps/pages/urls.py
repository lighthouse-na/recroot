from django.urls import path

from . import views

# app_name = "pages"

urlpatterns = [
    path("", views.VacancyListView.as_view(), name="vacancy_list"),
    path(
        "vacancy/<slug>/detail/",
        views.VacancyDetailView.as_view(),
        name="vacancy_detail",
    ),
    path("<slug>/apply", views.application_create, name="apply"),
]
