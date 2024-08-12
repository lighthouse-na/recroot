from datetime import datetime

from django.shortcuts import get_object_or_404, redirect, render

from apps.recruitment.models import Application, Interview, Subscriber, Vacancy


def index(request):
    template_name = "pages/index.html"
    vacancies = Vacancy.objects.filter(
        is_public=True, deadline__gt=datetime.now()
    ).order_by("-created_at")
    context = {"vacancies": vacancies}
    return render(request, template_name, context)
