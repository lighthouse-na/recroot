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
    SubscriberForm,
)
from apps.recruitment.models import (
    Application,
    Interview,
    MinimumRequirement,
    MinimumRequirementAnswer,
    Subscriber,
    Vacancy,
)


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
        return Vacancy.objects.filter(is_public=True, deadline__gt=datetime.now()).order_by("-created_at")


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
    """
    View for creating a new application for a specific vacancy.

    This view renders a form for users to apply for a job vacancy. It handles
    saving the application along with associated minimum requirements answers
    and user data. It also ensures that applications cannot be submitted after
    the vacancy's deadline.
    """

    model = Application
    form_class = ApplicationForm
    success_url = reverse_lazy("recruitment:application_success")
    template_name = "recruitment/vacancy/detail.html"  # Used the vacancy detail template

    def form_valid(self, form):
        """
        Handles the valid submission of the application form.

        This method overrides the default `form_valid` to associate the application
        with the selected vacancy and authenticated user, as well as save answers
        to minimum requirements related to the vacancy.

        Args:
            form: The submitted form with valid data.

        Returns:
            HTTP response: A redirect to the `success_url` if the form is valid.
        """
        slug = self.kwargs.get("slug")
        vacancy = get_object_or_404(Vacancy, slug=slug)  # Fetch the vacancy based on the slug
        try:
            # Wrap the entire save process in a transaction to ensure atomicity
            with transaction.atomic():
                # Create the application without saving to the database yet
                application = form.save(commit=False)
                application.vacancy = vacancy  # Associate with the correct vacancy
                user = self.request.user

                if user.is_authenticated:
                    # Fill in user-related fields if the user is authenticated
                    application.first_name = user.first_name
                    application.middle_name = user.middle_name
                    application.last_name = user.last_name
                    application.email = user.email
                    application.primary_contact = user.primary_contact
                    application.secondary_contact = user.secondary_contact
                    application.date_of_birth = user.date_of_birth
                    application.gender = user.gender

                application.save()  # Save the application to the database

                # Save answers to minimum requirements if any
                requirements = MinimumRequirement.objects.filter(vacancy=vacancy)
                for requirement in requirements:
                    answer = form.cleaned_data[f"requirement_{requirement.id}"]
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
        """
        Adds additional context to the template rendering.

        This method ensures that the vacancy details are included in the context
        and disables the application link if the current date is past the vacancy deadline.

        Args:
            kwargs: Any additional keyword arguments for context.

        Returns:
            dict: The context data to be passed to the template.
        """
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get("slug")
        vacancy = get_object_or_404(Vacancy, slug=slug)
        context["disable_link"] = timezone.now() > vacancy.deadline  # Disable link if the deadline has passed
        context["vacancy"] = vacancy  # Include the vacancy details in the context
        return context

    def get_form_kwargs(self):
        """
        Passes the vacancy to the form for further customization.

        This method adds the vacancy to the form’s arguments so that it can be used
        when creating the application instance and when saving minimum requirement answers.

        Returns:
            dict: The form keyword arguments, including the vacancy instance.
        """
        kwargs = super().get_form_kwargs()
        slug = self.kwargs.get("slug")
        vacancy = get_object_or_404(Vacancy, slug=slug)
        kwargs["vacancy"] = vacancy  # Add the vacancy to the form arguments
        return kwargs


class SubscribeCreateView(CreateView):
    model = Subscriber
    form_class = SubscriberForm
    success_url = reverse_lazy("home")
    template_name = "recruitment/subscribe/create.html"


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
