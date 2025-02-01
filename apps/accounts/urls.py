from django.urls import path

from . import views

app_name = "accounts"
urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path("experience/create/", views.create_experience, name="create_experience"),
    path(
        "experience/<int:experience_id>/delete/",
        views.delete_experience,
        name="delete_experience",
    ),
    path("qualification/create/", views.create_qualification, name="create_qualification"),
    path(
        "qualification/<int:qualification_id>/delete/",
        views.delete_qualification,
        name="delete_qualification",
    ),
    path("certification/create/", views.create_certification, name="create_certification"),
    path(
        "certification/<int:certification_id>/delete/",
        views.delete_certification,
        name="delete_certification",
    ),
]
