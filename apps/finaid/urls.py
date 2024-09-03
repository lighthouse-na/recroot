from django.urls import path
from .views import FinancialAssistanceApplicationCreateView

urlpatterns = [
    path(
        "create/<uuid:advert_id>/",
        FinancialAssistanceApplicationCreateView.as_view(),
        name="financial_assistance_application_create",
    )
]
