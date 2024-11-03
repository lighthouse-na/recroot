from datetime import datetime

from django.shortcuts import render

from apps.recruitment import models


def dashboard(request):
    template_name = "staff/dashboard.html"
    vacancies = models.Vacancy.objects.filter(
        is_published=True, is_public=True, deadline__gt=datetime.now()
    ).order_by("-created_at")
    context = {"vacancies": vacancies}
    return render(request, template_name, context)
