from datetime import datetime
from django.contrib.admin import site
from django.shortcuts import get_object_or_404, redirect, render

from apps.recruitment.models import Application, Interview, Subscriber, Vacancy


def index(request):
    template_name = "pages/index.html"
    vacancies = Vacancy.objects.filter(
        is_public=True, deadline__gt=datetime.now()
    ).order_by("-created_at")
    context = {
        "title": "My Admin Page",
        "site_header": "My Site",
        "site_url": "/",
        # "has_permission": request.user.is_staff,
        # "available_apps": site.get_app_list(request),
        "is_popup": True,
        "is_nav_sidebar_enabled": True,
        # "app_label": "myapp",  # Replace with your app label
        # "app_list": site.get_model_list(
        #     request, "myapp"
        # ),  # Replace with your app label
        "request": request,
    }
    context = {"vacancies": vacancies}
    return render(request, template_name, context)
