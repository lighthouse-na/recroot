from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import Case, IntegerField, Value, When
from django.utils import timezone
from django.utils.html import format_html
from import_export.admin import ExportActionModelAdmin
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from unfold.contrib.filters.admin import RangeDateFilter
from unfold.contrib.import_export.forms import SelectableFieldsExportForm

from .forms import (
    ApplicationReviewForm,
    InterviewForm,
    MinimumRequirementsAddForm,
    SelectQuestionTypeOptionsForm,
    VacancyForm,
)
from .models import (
    Application,
    Interview,
    Location,
    MinimumRequirement,
    MinimumRequirementAnswer,
    SelectQuestionTypeOptions,
    Vacancy,
    VacancyType,
)

# **********************************************************************************************
#                                       VACANCY
# **********************************************************************************************
# Registering VacancyType model to the admin site
admin.site.register(VacancyType, ModelAdmin)


class SelectQuestionTypeOptionsInline(StackedInline):
    model = SelectQuestionTypeOptions
    form = SelectQuestionTypeOptionsForm
    extra = 1


class RequirementsAdmin(ModelAdmin):
    model = MinimumRequirement
    list_display = ("__str__", "vacancy", "is_required", "is_internal")
    readonly_fields = [
        "vacancy",
        "title",
        "question_type",
        "is_required",
        "is_internal",
    ]
    inlines = [SelectQuestionTypeOptionsInline]

    def has_add_permission(self, request):
        return False


class MinimumRequirementsAddInline(TabularInline):
    model = MinimumRequirement
    form = MinimumRequirementsAddForm
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
        "is_published",
    ]
    list_filter = [
        "title",
        "deadline",
        "is_public",
    ]
    filter_horizontal = ["town", "reviewers"]
    inlines = [MinimumRequirementsAddInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Allow superusers and admins to see all vacancies
        if request.user.is_superuser or request.user.groups.filter(name="admin").exists():
            return qs

        # Filter vacancies where the user is a reviewer
        return qs.filter(reviewers=request.user)

    def has_view_permission(self, request, obj=None):
        if obj is None:
            return True
        return request.user.is_superuser or request.user in obj.reviewers.all()

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        return request.user.is_superuser or request.user.groups.filter(name="admin").exists()

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.groups.filter(name="admin"):
            return True
        return False


# **********************************************************************************************
#                                       APPLICATION
# **********************************************************************************************
class ApplicantResponseInline(TabularInline):
    model = MinimumRequirementAnswer
    fields = ["answer"]
    tab = True
    extra = 0

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if self.parent_model == Application and hasattr(self, "parent_obj"):
            # Filters answers to only those associated with the current application
            qs = qs.filter(application=self.parent_obj)
        return qs

    def get_formset(self, request, obj=None, **kwargs):
        self.parent_obj = obj
        return super().get_formset(request, obj, **kwargs)

    def has_module_permission(self, request):
        if super().has_module_permission(request):
            return False


@admin.register(Application)
class ApplicationAdmin(ModelAdmin, ExportActionModelAdmin):
    model = Application
    export_form_class = SelectableFieldsExportForm

    readonly_fields = [
        "first_name",
        "middle_name",
        "last_name",
        "email",
        "primary_contact",
        "secondary_contact",
        "date_of_birth",
        "gender",
        "cv",
        "reviewed_by",
        "reviewers",
        "reviewed_at",
        "submitted_at",
    ]

    form = ApplicationReviewForm
    list_display = [
        "first_name",
        "last_name",
        "email",
        "vacancy",
        "status",
        "is_internal",
        "submitted_at",
    ]
    list_filter = ("vacancy", "status", "submitted_at")
    search_fields = ("first_name", "last_name", "email")
    inlines = [ApplicantResponseInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.groups.filter(name="admin"):
            return qs
        vacancies_user_can_review = Vacancy.objects.filter(reviewers=request.user)
        qs = qs.filter(vacancy__in=vacancies_user_can_review)
        qs = qs.annotate(
            status_order=Case(
                When(status="submitted", then=Value(0)),
                When(status="rejected", then=Value(1)),
                When(status="accepted", then=Value(2)),
                default=Value(3),
                output_field=IntegerField(),
            )
        ).order_by("status_order", "-submitted_at")
        return qs

    def has_view_permission(self, request, obj=None):
        if obj is None:
            return True
        return request.user.is_superuser or request.user in obj.vacancy.reviewers.all()

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        return request.user.is_superuser or request.user in obj.vacancy.reviewers.all()

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.groups.filter(name="admin"):
            return True
        return False

    def get_formset(self, request, obj=None, **kwargs):
        """
        Retrieves the formset for MinimumRequirementAnswer objects in the admin inline.

        This method ensures that the parent object (the Application) is set for the
        formset, allowing the correct filtering of answers in the formset.

        Args:
            request (HttpRequest): The HTTP request object.
            obj (Model, optional): The object being edited, if any.
            kwargs (dict): Additional arguments passed to the formset.

        Returns:
            FormSet: The formset for MinimumRequirementAnswer objects.
        """
        self.parent_obj = obj
        return super().get_formset(request, obj, **kwargs)

    def view_cv(self, obj):
        """
        Returns a link to view the uploaded CV of the applicant.

        Args:
            obj (Application): The application object.

        Returns:
            str: A link to view the CV or a message if no CV is uploaded.
        """
        if obj.cv:
            return format_html('<a href="{}" target="_blank">View CV</a>', obj.cv.url)
        return "No CV uploaded"

    def save_model(self, request, obj, form, change):
        if obj.status in [Application.STATUS.ACCEPTED, Application.STATUS.REJECTED]:
            user = get_user_model().objects.get(id=request.user.id)

            obj.reviewed_at = timezone.now()
            obj.reviewed_by = user

        super().save_model(request, obj, form, change)

    # Adding description for the CV field link in the list display
    view_cv.short_description = "CV"


# **********************************************************************************************
#                                       INTERVIEW
# **********************************************************************************************
admin.site.register(Location, ModelAdmin)


@admin.register(Interview)
class InterviewAdmin(ModelAdmin, ExportActionModelAdmin):
    form = InterviewForm
    export_form_class = SelectableFieldsExportForm
    readonly_fields = ["application"]
    list_display = ["application", "status", "schedule_datetime"]
    list_filter = ["status", ("schedule_datetime", RangeDateFilter)]
    list_filter_submit = True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.groups.filter(name="admin"):
            return qs
        return qs.filter(application__vacancy__reviewers=request.user)

    def has_view_permission(self, request, obj=None):
        if obj is None:
            return True
        return request.user.is_superuser or obj.application.vacancy.reviewers.filter(id=request.user.id).exists()

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        return request.user.is_superuser or request.user in obj.vacancy.reviewers.all()

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.groups.filter(name="admin"):
            return True
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj is not None and obj.status in [
            Interview.STATUS.ACCEPTED,
            Interview.STATUS.REJECTED,
        ]:
            return [field.name for field in self.model._meta.fields]
        return super().get_readonly_fields(request, obj)

    def save_model(self, request, obj, form, change):
        if not obj.status:
            obj.clean()  # Run model validation
            obj.status = Interview.STATUS.SCHEDULED
        super().save_model(request, obj, form, change)
