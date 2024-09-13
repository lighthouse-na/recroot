from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("privacy-policy/", views.policy, name="privacy"),
]
