from django.contrib import admin
from import_export.admin import ExportActionModelAdmin
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.import_export.forms import (ExportForm,
                                                SelectableFieldsExportForm)

from .forms import ApplicationForm, InterviewForm, VacancyForm
from .models import (Application, ApplicationRequirementAnswer, Interview,
                     MinimumRequirement, Vacancy, VacancyType)

admin.site.register(VacancyType)


class MinimumRequirementsInline(TabularInline):
    model = MinimumRequirement
    # form = MinimumRequirementsForm
    extra = 1
    tab = True


class ApplicationRequirementAnswerInline(TabularInline):
    model = ApplicationRequirementAnswer
    extra = 1
    tab = True


@admin.register(Vacancy)
class VacancyAdmin(ModelAdmin):
    form = VacancyForm
    list_display = [
        "title",
        "deadline",
        "is_public",
    ]
    list_filter = [
        "title",
        "town",
        "deadline",
        "is_public",
    ]
    inlines = [MinimumRequirementsInline]


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


@admin.register(Interview)
class InterviewAdmin(ModelAdmin):
    form = InterviewForm
    list_display = ["application", "status", "schedule_datetime"]
    list_filter = ["application", "status", "schedule_datetime"]
