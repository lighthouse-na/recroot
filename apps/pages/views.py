from datetime import datetime

from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView, TemplateView

from apps.recruitment import models
from apps.recruitment.forms import (ApplicationForm,
                                    MinimumRequirementsAnswerForm)


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


def vacancy_detail_create(request, slug):
    template_name = "recruitment/vacancy/detail.html"
    vacancy = get_object_or_404(models.Vacancy, slug=slug)
    requirements = vacancy.requirements.all()

    if request.method == "POST":
        application_form = ApplicationForm(request.POST, request.FILES)

        if application_form.is_valid():
            application = application_form.save(commit=False)
            application.vacancy = vacancy
            application.save()

            for requirement in requirements:
                requirement_form = MinimumRequirementsAnswerForm(
                    request.POST, instance=requirement
                )
                if requirement_form.is_valid():
                    req = requirement_form.save(commit=False)
                    req.application = application
                    req.save()

            return redirect("pages:vacancy_list")
    else:
        application_form = ApplicationForm()
        requirements_forms = [
            MinimumRequirementsAnswerForm(instance=requirement)
            for requirement in requirements
        ]

    context = {
        "vacancy": vacancy,
        "application_form": application_form,
        "requirements_forms": zip(requirements, requirements_forms),
    }
    return render(request, template_name, context)


class VacancyDetailCreateView(TemplateView):

    template_name = "recruitment/vacancy/detail.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        self.vacancy = get_object_or_404(models.Vacancy, slug=self.kwargs["slug"])

        self.requirements = self.vacancy.requirements.all()

        context["vacancy"] = self.vacancy

        context["application_form"] = ApplicationForm()

        context["requirements_forms"] = [
            MinimumRequirementsAnswerForm(instance=requirement)
            for requirement in self.requirements
        ]

        return context

    def post(self, request, *args, **kwargs):

        application_form = ApplicationForm(request.POST, request.FILES)

        if application_form.is_valid():

            application = application_form.save(commit=False)

            application.vacancy = self.vacancy

            application.save()

            for requirement in self.requirements:

                requirement_form = MinimumRequirementsAnswerForm(
                    request.POST, instance=requirement
                )

                if requirement_form.is_valid():

                    req = requirement_form.save(commit=False)

                    req.application = application

                    req.save()

            return redirect("pages:vacancy_list")

        return self.render_to_response(self.get_context_data())
