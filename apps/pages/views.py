from datetime import datetime
from django.shortcuts import render

from apps.pages.models import FAQ, Announcement
from apps.recruitment.models import Vacancy


def index(request):
    template_name = "pages/index.html"
    vacancies = Vacancy.objects.filter(is_published=True, is_public=True, deadline__gt=datetime.now()).order_by(
        "-created_at"
    )
    announcements = Announcement.objects.filter(deadline__gt=datetime.now(), is_visible=True, is_external=True)
    faqs = FAQ.objects.filter(is_visible=True)

    context = {
        "vacancies": vacancies,
        "announcements": announcements,
        "faqs": faqs,
    }
    return render(request, template_name, context)


def policy(request):
    template_name = "pages/privacy.html"
    return render(request, template_name)
