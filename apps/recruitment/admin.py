from django.contrib import admin
from import_export.admin import ExportActionModelAdmin
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.import_export.forms import ExportForm, SelectableFieldsExportForm
from django.utils.html import format_html
from .forms import (
    ApplicationForm,
    InterviewForm,
    MinimumRequirementsAddForm,
    MinimumRequirementsAnswerForm,
    VacancyForm,
    ApplicationReviewForm,
)
from .models import Application, Interview, MinimumRequirement, Vacancy, VacancyType

admin.site.register(VacancyType)


class MinimumRequirementsAddInline(TabularInline):
    model = MinimumRequirement
    form = MinimumRequirementsAddForm
    extra = 1
    tab = True


class MinimumRequirementsAnswerInline(TabularInline):
    model = MinimumRequirement
    form = MinimumRequirementsAnswerForm
    extra = 1
    tab = True


@admin.register(Vacancy)
class VacancyAdmin(ModelAdmin):
    form = VacancyForm
    list_display = [
        "title",
        "deadline",
        "vacancy_type",
        "is_public",
    ]
    list_filter = [
        "title",
        "deadline",
        "is_public",
    ]
    inlines = [MinimumRequirementsAddInline]


@admin.register(Application)
class ApplicationAdmin(ModelAdmin):
    model = Application
    readonly_fields = [
        "first_name",
        "middle_name",
        "last_name",
        "email",
        "primary_contact",
        "secondary_contact",
        "date_of_birth",
        "cv",
    ]
    form = ApplicationReviewForm
    list_display = [
        "first_name",
        "last_name",
        "email",
        "status",
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

    # inlines = [MinimumRequirementsAnswerInline]
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.status != "submitted":
            return False
        return super().has_change_permission(request, obj)

    def view_cv(self, obj):
        if obj.cv:
            return format_html('<a href="{}" target="_blank">View CV</a>', obj.cv.url)
        return "No CV uploaded"

    view_cv.short_description = "CV"


@admin.register(Interview)
class InterviewAdmin(ModelAdmin):
    form = InterviewForm
    list_display = ["application", "status", "schedule_datetime"]
    list_filter = ["application", "status", "schedule_datetime"]
