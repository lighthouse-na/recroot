from datetime import datetime
from typing import Any

from django.contrib import messages
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from apps.recruitment.forms import (
    ApplicantResponseForm,
    ApplicationForm,
    InterviewInvitationResponseForm,
    MinimumRequirementsAnswerForm,
    SubscriberForm,
)
from apps.recruitment.models import Application, Interview, Subscriber, Vacancy


class VacancyListView(ListView):
    """
    A ListView for displaying a list of Vacancy instances.

    Attributes:
        model (Vacancy): The model associated with this view.
        template_name (str): The path to the template used to render the view.
        context_object_name (str): The name of the object list in the context.

    Methods:
        get_queryset (self): Returns a filtered queryset of Vacancy instances.

    Returns:
        A list of Vacancy instances that are public and have not passed their deadline, ordered by creation date in descending order.
    """

    model = Vacancy
    template_name = "pages/index.html"
    context_object_name = "vacancies"

    def get_queryset(self):
        """
        Returns a filtered queryset of Vacancy instances.

        Returns:
            A queryset of Vacancy instances that are public and have not passed their deadline, ordered by creation date in descending order.

        """
        return Vacancy.objects.filter(
            is_public=True, deadline__gt=datetime.now()
        ).order_by("-created_at")


class VacancyDetailView(DetailView):
    """
    A DetailView for displaying a single Vacancy instance.

    Attributes:
        model (Vacancy): The model associated with this view.
        template_name (str): The path to the template used to render the view.
        context_object_name (str): The name of the object in the context.


    Methods:
        get (request, *args, **kwargs): Handles GET requests and returns a response.

    """

    model = Vacancy
    template_name = "recruitment/vacancy/detail.html"
    context_object_name = "vacancy"


class ApplicationCreateView(CreateView):
    model = Application
    form_class = ApplicationForm
    success_url = reverse_lazy("vacancy_list")
    template_name = "recruitment/application/create.html"

    def form_valid(self, form):
        slug = self.kwargs.get("slug")
        vacancy = get_object_or_404(Vacancy, slug=slug)
        application = form.save(commit=False)
        application.vacancy = vacancy
        application.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get("slug")
        context["vacancy"] = get_object_or_404(Vacancy, slug=slug)
        return context


class SubscribeCreateView(CreateView):
    model = Subscriber
    form_class = SubscriberForm
    success_url = reverse_lazy("home")
    template_name = "recruitment/subscribe/create.html"


class InterviewResponseView(UpdateView):
    model = Interview
    form_class = InterviewInvitationResponseForm
    template_name = "recruitment/interview/invitation.html"
    success_url = reverse_lazy("vacancy_list")

    def form_valid(self, form):
        response = form.save(commit=False)
        response.response_date = timezone.now()
        response.save()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.response_date:
            return redirect("vacancy_list")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        context["interview"] = get_object_or_404(Interview, pk=pk)
        return context
