from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from . import forms, models


def profile(request):
    template_name = "account/profile.html"
    user = request.user
    experiences = models.Experience.objects.filter(user=user)
    if request.user != user:
        raise PermissionDenied("You do not have permission to view this profile.")

    context = {
        "user": user,
        "experiences": experiences,
    }

    return render(request, template_name, context)


class CreateExperience(CreateView):
    model = models.Experience
    template_name = "account/experience/create.html"
    form_class = forms.ExperienceForm
    success_url = reverse_lazy("accounts:profile")

    def form_valid(self, form):
        experience = form.save(commit=False)
        experience.user = self.request.user
        experience.save()
        return super().form_valid(form)


def create_experience(request):
    if request.method == "POST":
        form = forms.ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = request.user  # assuming user is from the current session
            experience.save()
            return redirect(reverse_lazy("accounts:create_experience"))
    else:
        form = forms.ExperienceForm()

    return render(request, "account/experience/create.html", {"form": form})
