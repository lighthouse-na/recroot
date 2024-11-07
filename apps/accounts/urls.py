from django.urls import path

from . import views

app_name = "accounts"
urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path("experience/", views.CreateExperience.as_view(), name="create_experience"),
    # path("experience/", views.create_experience, name="create_experience"),
]
