from django.urls import path

from . import views

urlpatterns = [
    path("validation/email/", views.email_validation, name="email_validation"),
]
