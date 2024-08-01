from datetime import datetime
from typing import Any

from django.http import HttpRequest, HttpResponseRedirect
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DetailView, ListView, View
from django.views.generic.base import TemplateResponseMixin

from apps.recruitment import models
from apps.recruitment.forms import (
    ApplicantResponseForm,
    ApplicationForm,
    MinimumRequirementsAnswerForm,
)


class VacancyListView(ListView):
    """
    A ListView for displaying a list of Vacancy instances.

    Attributes:
        model (models.Vacancy): The model associated with this view.
        template_name (str): The path to the template used to render the view.
        context_object_name (str): The name of the object list in the context.

    Methods:
        get_queryset (self): Returns a filtered queryset of Vacancy instances.

    Returns:
        A list of Vacancy instances that are public and have not passed their deadline, ordered by creation date in descending order.
    """

    model = models.Vacancy
    template_name = "recruitment/vacancy/list.html"
    context_object_name = "vacancies"

    def get_queryset(self):
        """
        Returns a filtered queryset of Vacancy instances.

        Returns:
            A queryset of Vacancy instances that are public and have not passed their deadline, ordered by creation date in descending order.

        """
        return models.Vacancy.objects.filter(
            is_public=True, deadline__gt=datetime.now()
        ).order_by("-created_at")


class VacancyDetailView(DetailView):
    """
    A DetailView for displaying a single Vacancy instance.

    Attributes:
        model (models.Vacancy): The model associated with this view.
        template_name (str): The path to the template used to render the view.
        context_object_name (str): The name of the object in the context.


    Methods:
        get (request, *args, **kwargs): Handles GET requests and returns a response.

    """

    model = models.Vacancy
    template_name = "recruitment/vacancy/detail.html"
    context_object_name = "vacancy"


def application_create(request, slug):
    template_name = "recruitment/vacancy/create.html"
    vacancy = get_object_or_404(models.Vacancy, slug=slug)
    requirements = vacancy.requirements.all()

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)

        if form.is_valid():
            application = form.save(commit=False)
            application.vacancy = vacancy
            application.save()
            return redirect("vacancy_list")

    else:
        form = ApplicationForm()

    context = {
        "vacancy": vacancy,
        "requirements": requirements,
        "form": form,
    }
    return render(request, template_name, context)
