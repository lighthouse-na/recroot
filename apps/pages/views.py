from django.shortcuts import render
from django.utils import timezone

from apps.pages.models import FAQ, Announcement
from apps.recruitment.models import Vacancy


def index(request):
    template_name = "pages/index.html"

    if request.is_intranet:
        vacancies = Vacancy.objects.filter(is_published=True, deadline__gt=timezone.now()).order_by("-created_at")
    else:
        vacancies = Vacancy.objects.filter(is_public=True, is_published=True, deadline__gt=timezone.now()).order_by(
            "-created_at"
        )
    announcements = Announcement.objects.filter(deadline__gt=timezone.now(), is_visible=True, is_external=True)
    faqs = FAQ.objects.filter(is_visible=True)

    user_groups = []
    if request.user.is_authenticated:
        user_groups = [group.name for group in request.user.groups.all()]

    context = {
        "vacancies": vacancies,
        "announcements": announcements,
        "faqs": faqs,
        "user_groups": user_groups,
    }
    return render(request, template_name, context)


def policy(request):
    template_name = "pages/privacy.html"
    return render(request, template_name)
