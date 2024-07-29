from django.contrib import admin
from import_export.admin import ExportActionModelAdmin
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.import_export.forms import ExportForm, SelectableFieldsExportForm
from .models import (
    Application,
    Vacancy,
    MinimumRequirement,
    ApplicationRequirementAnswer,
)
from .forms import ApplicationForm
from django.utils.html import format_html
from django.urls import path, reverse
from django.shortcuts import redirect, render


class MinimumRequirementsInline(TabularInline):
    model = MinimumRequirement
    # form = MinimumRequirementsForm
    extra = 1
    # tab = True


class ApplicationRequirementAnswerInline(TabularInline):
    model = ApplicationRequirementAnswer
    extra = 1
    tab = True


@admin.register(Vacancy)
class VacancyAdmin(ModelAdmin):
    list_display = [
        "title",
        "town",
        "deadline",
        "is_public",
        "apply_button",
    ]
    list_filter = [
        "title",
        "town",
        "deadline",
        "is_public",
    ]
    inlines = [MinimumRequirementsInline]

    def apply_button(self, obj):
        url = reverse("admin:vacancy_apply", args=[obj.id])
        return format_html('<a class="button" href="{}">Apply</a>', url)

    apply_button.short_description = "Apply"

    apply_button.allow_tags = True

    def get_urls(self):

        urls = super().get_urls()

        custom_urls = [
            path(
                "vacancy/<int:vacancy_id>/apply/",
                self.admin_site.admin_view(self.apply_view),
                name="vacancy_apply",
            ),
        ]

        return custom_urls + urls

    def apply_view(self, request, vacancy_id):
        vacancy = Vacancy.objects.get(id=vacancy_id)

        if request.method == "POST":
            form = ApplicationForm(request.POST)

            if form.is_valid():
                application = form.save(commit=False)
                application.vacancy = vacancy
                application.save()
                return redirect(reverse("admin:recruitment_vacancy_changelist"))
        else:
            form = ApplicationForm()

        return render(request, "admin/apply.html", {"form": form, "vacancy": vacancy})


@admin.register(Application)
class ApplicationAdmin(ModelAdmin):
    model = Application
    form = ApplicationForm
    list_display = [
        "first_name",
        "last_name",
        "email",
    ]
    list_filter = (
        "first_name",
        "last_name",
        "email",
    )
    search_fields = (
        "first_name",
        "last_name",
        "email",
    )
    inlines = [ApplicationRequirementAnswerInline]
