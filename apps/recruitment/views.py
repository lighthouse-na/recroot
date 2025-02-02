from datetime import datetime

from django.contrib import messages
from django.db import IntegrityError, transaction
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from apps.recruitment.forms import (
    ApplicationForm,
    InterviewInvitationResponseForm,
)
from apps.recruitment.models import (
    Application,
    Interview,
    MinimumRequirement,
    MinimumRequirementAnswer,
    Vacancy,
)


class VacancyListView(ListView):
    model = Vacancy
    template_name = "pages/index.html"
    context_object_name = "vacancies"

    def get_queryset(self):
        print(f"Request is_intranet: {self.request.is_intranet}")
        if self.request.is_intranet:
            return Vacancy.objects.filter(is_public=False, is_published=True, deadline__gt=datetime.now()).order_by(
                "-created_at"
            )
        return Vacancy.objects.filter(is_public=True, is_published=True, deadline__gt=datetime.now()).order_by(
            "-created_at"
        )


class VacancyDetailView(DetailView):
    model = Vacancy
    template_name = "recruitment/vacancy/detail.html"
    context_object_name = "vacancy"


class ApplicationCreateView(CreateView):
    model = Application
    form_class = ApplicationForm
    success_url = reverse_lazy("recruitment:application_success")
    template_name = "recruitment/vacancy/detail.html"

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get("slug")
        vacancy = get_object_or_404(Vacancy, slug=slug)

        # Check if the vacancy is internal and the user is not on the intranet
        if vacancy.is_public is False and not request.is_intranet:
            # Redirect to homepage if the user is not on the intranet
            return redirect("home")  # Adjust "homepage" to your actual homepage URL name

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        slug = self.kwargs.get("slug")
        vacancy = get_object_or_404(Vacancy, slug=slug)  # Fetch the vacancy based on the slug
        try:
            # Wrap the entire save process in a transaction to ensure atomicity
            with transaction.atomic():
                # Create the application without saving to the database yet
                application = form.save(commit=False)
                application.vacancy = vacancy  # Associate with the correct vacancy
                application.is_internal = self.request.is_intranet  # if applied via the intranet
                application.save()  # Save the application to the database

                # Save answers to minimum requirements if any
                requirements = MinimumRequirement.objects.filter(vacancy=vacancy)
                for requirement in requirements:
                    # answer = form.cleaned_data[f"requirement_{requirement.id}"]
                    # MinimumRequirementAnswer.objects.create(
                    #     application=application, requirement=requirement, answer=answer
                    # )

                    field_name = f"requirement_{requirement.id}"
                    # Check if the field is in the cleaned_data to avoid KeyError
                    if field_name in form.cleaned_data:
                        answer = form.cleaned_data[field_name]
                        MinimumRequirementAnswer.objects.create(
                            application=application, requirement=requirement, answer=answer
                        )

                # Save many-to-many relationships
                form.save_m2m()

        except IntegrityError:
            # Handle the case where the user has already applied for the vacancy
            messages.add_message(
                self.request,
                messages.ERROR,
                "You have already applied for this vacancy.",
            )
            return self.form_invalid(form)

        return super().form_valid(form)  # Proceed to the success URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get("slug")
        vacancy = get_object_or_404(Vacancy, slug=slug)
        context["disable_link"] = timezone.now() > vacancy.deadline  # Disable link if the deadline has passed
        context["vacancy"] = vacancy  # Include the vacancy details in the context
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        slug = self.kwargs.get("slug")
        vacancy = get_object_or_404(Vacancy, slug=slug)
        kwargs["vacancy"] = vacancy
        kwargs["request"] = self.request
        return kwargs


class InterviewResponseView(UpdateView):
    model = Interview
    form_class = InterviewInvitationResponseForm
    template_name = "recruitment/interview/invitation.html"
    success_url = reverse_lazy("recruitment:interview_response_success")

    def form_valid(self, form):
        response = form.save(commit=False)
        response.response_date = timezone.now()
        # response.response_deadline = timezone.now()
        response.save()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.response_date:
            return redirect("home")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        interview = get_object_or_404(Interview, pk=pk)
        context["interview"] = interview

        disabled_statuses = ["no_response", "accepted", "rescheduled", "rejected"]
        if interview.status in disabled_statuses:
            context["disable_link"] = True
        else:
            context["disable_link"] = False
        return context


def application_success(request):
    return render(request, "recruitment/application/success.html")


def interview_response_success(request):
    return render(request, "recruitment/interview/success.html")


class ApplicationsListView(ListView):
    model = Application
    template_name = "recruitment/application/list.html"
    context_object_name = "applications"
