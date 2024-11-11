from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
import json
from . import forms, models
from apps.utils.models import ChoicesQuerySet


def profile(request):
    template_name = "account/profile.html"
    user = request.user
    types = models.Qualification.QualificationType.choices
    if request.user != user:
        raise PermissionDenied("You do not have permission to view this profile.")

    context = {
        "user": user,
        "types": types,
    }

    return render(request, template_name, context)


# Experience


def create_experience(request):

    if request.method == "POST":
        form = forms.ExperienceForm(request.POST, request.FILES)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = request.user
            experience.save()
            return render(request, "account/experience/list.html")
    else:
        form = forms.ExperienceForm()

    return render(request, "account/experience/create.html", {"form": form})


def delete_experience(request, experience_id):
    experience = get_object_or_404(models.Experience, id=experience_id)
    experience.delete()
    return render(request, "account/experience/list.html")


# Qualification


def create_qualification(request):
    if request.method == "POST":
        form = forms.QualificationForm(request.POST, request.FILES)
        if form.is_valid():
            qualification = form.save(commit=False)
            qualification.user = request.user
            qualification.save()
            return render(request, "account/qualification/list.html")
    else:
        form = forms.QualificationForm()

    return render(
        request,
        "account/qualification/create.html",
        {"form": form},
    )


def delete_qualification(request, qualification_id):
    qualification = get_object_or_404(models.Qualification, id=qualification_id)
    qualification.delete()
    return render(request, "account/qualification/list.html")


# Certification


def create_certification(request):

    if request.method == "POST":
        form = forms.CertificationForm(request.POST, request.FILES)
        if form.is_valid():
            certification = form.save(commit=False)
            certification.user = request.user
            certification.save()
            return render(request, "account/certification/list.html")
    else:
        form = forms.CertificationForm()

    return render(request, "account/certification/create.html", {"form": form})


def delete_certification(request, certification_id):
    certification = get_object_or_404(models.Certification, id=certification_id)
    certification.delete()
    return render(request, "account/certification/list.html")
