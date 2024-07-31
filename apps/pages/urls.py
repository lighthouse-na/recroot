from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.VacancyListView.as_view(), name="vacancy_list"),
    path(
        "vacancy/<slug>/detail/",
        views.vacancy_detail_create,
        name="vacancy_detail",
    ),
    # path(
    #     "vacancy/<slug>/detail/",
    #     views.VacancyDetailView.as_view(),
    #     name="vacancy_detail",
    # ),
]
