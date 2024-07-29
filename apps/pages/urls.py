from django.urls import path
from . import views

app_name = "vacancy"

urlpatterns = [
    path("", views.VacancyListView.as_view(), name="vacancy_list"),
    path(
        "vacancy/<slug>/detail/",
        views.VacancyDetailView.as_view(),
        name="vacancy_detail",
    ),
]
