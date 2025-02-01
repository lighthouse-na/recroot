from django.contrib import admin
from django.contrib.auth import get_user_model
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
    Subscriber,
    Vacancy,
    VacancyType,
)

# **********************************************************************************************
#                                       VACANCY
# **********************************************************************************************
# Registering VacancyType model to the admin site
admin.site.register(VacancyType, ModelAdmin)


class SelectQuestionTypeOptionsInline(StackedInline):
    """
    Inline form for adding or editing SelectQuestionTypeOptions within a VacancyType.

    This inline form is used to edit the SelectQuestionTypeOptions related to a
    VacancyType in the admin interface. It allows administrators to manage options
    associated with the question types.

    Attributes:
        model: The model associated with this inline form (SelectQuestionTypeOptions).
        form: The form used for this inline model (SelectQuestionTypeOptionsForm).
        extra: The number of empty forms to display initially (1).
    """

    model = SelectQuestionTypeOptions
    form = SelectQuestionTypeOptionsForm
    extra = 1


class RequirementsAdmin(ModelAdmin):
    """
    Admin configuration for managing MinimumRequirement models.

    This custom admin configuration is used to display and manage MinimumRequirement
    entries associated with a Vacancy. The configuration includes specific fields
    to be displayed in the list view and makes certain fields read-only. It also
    disables adding new MinimumRequirement entries.

    Attributes:
        model: The model associated with this admin (MinimumRequirement).
        list_display: The fields to display in the admin list view.
        readonly_fields: The fields that are read-only in the admin form.
        inlines: The inline models (SelectQuestionTypeOptionsInline) to be displayed.
    """

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
        """
        Disable the ability to add new MinimumRequirement entries.

        This method returns False, meaning that no new MinimumRequirement entries
        can be added from the admin interface.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            bool: Always returns False to disable the add permission.
        """
        return False


class MinimumRequirementsAddInline(TabularInline):
    """
    Inline form for adding MinimumRequirement entries in a Tabular format.

    This inline form is used to add MinimumRequirement entries associated with
    a parent model. It allows administrators to add these entries directly within
    the parent form interface.

    Attributes:
        model: The model associated with this inline form (MinimumRequirement).
        form: The form used for this inline model (MinimumRequirementsAddForm).
        extra: The number of empty forms to display initially (1).
        tab: A custom flag to indicate tabular inline style.
    """

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
        """Users can only view applications for vacancies they are reviewers of."""
        if obj is None:
            return True
        return request.user.is_superuser or request.user in obj.reviewers.all()

    def has_change_permission(self, request, obj=None):
        """Users can only change applications for vacancies they are reviewers of."""
        if obj is None:
            return True
        return request.user.is_superuser or request.user.groups.filter(name="admin").exists()

    def has_delete_permission(self, request, obj=None):
        """Users can only delete applications for vacancies they are reviewers of."""
        if request.user.is_superuser or request.user.groups.filter(name="admin"):
            return True
        return False


# **********************************************************************************************
#                                       APPLICATION
# **********************************************************************************************
class ApplicantResponseInline(TabularInline):
    """
    Inline admin interface for managing MinimumRequirementAnswer objects related to Applications.

    This class is used to display and manage the answers provided by applicants to
    minimum requirements for a vacancy within the admin interface. It is intended to
    be used as an inline model within the Application model.

    Attributes:
        model: The model associated with this inline (MinimumRequirementAnswer).
        fields: The fields to display in the inline (answer).
        tab: A flag indicating whether this is a tabbed inline (True).
    """

    model = MinimumRequirementAnswer
    fields = ["answer"]
    tab = True

    def get_queryset(self, request):
        """
        Retrieves the queryset of MinimumRequirementAnswer objects to display in the admin inline.

        This method customises the queryset to filter answers based on the related application.
        It ensures that only answers associated with the current application are displayed.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            queryset: A filtered queryset of MinimumRequirementAnswer objects.
        """
        qs = super().get_queryset(request)
        if self.parent_model == Application and hasattr(self, "parent_obj"):
            # Filters answers to only those associated with the current application
            qs = qs.filter(application=self.parent_obj)
        return qs

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

    def has_module_permission(self, request):
        """
        Checks if the user has permission to access the inline module.

        This method overrides the default behaviour to prevent access to this inline
        model in the admin interface, returning False to disable access.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            bool: False (module is not accessible).
        """
        if super().has_module_permission(request):
            return False


@admin.register(Application)
class ApplicationAdmin(ModelAdmin, ExportActionModelAdmin):
    """
    Admin interface for managing Application objects.

    This class customizes the admin interface for the `Application` model, providing:
    - Permissions to control access to various actions (view, change, etc.)
    - Custom form for reviewing applications
    - Display fields, filters, and search options for easy management of applications.
    """

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
        "submitted_at",
    ]
    list_filter = ("vacancy", "status", "submitted_at")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("submitted_at",)
    inlines = [ApplicantResponseInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.groups.filter(name="admin"):
            return qs
        vacancies_user_can_review = Vacancy.objects.filter(reviewers=request.user)
        return qs.filter(vacancy__in=vacancies_user_can_review)

    def has_view_permission(self, request, obj=None):
        """Users can only view applications for vacancies they are reviewers of."""
        if obj is None:
            return True
        return request.user.is_superuser or request.user in obj.vacancy.reviewers.all()

    def has_change_permission(self, request, obj=None):
        """Users can only change applications for vacancies they are reviewers of."""
        if obj is None:
            return True
        return request.user.is_superuser or request.user in obj.vacancy.reviewers.all()

    def has_delete_permission(self, request, obj=None):
        """Users can only delete applications for vacancies they are reviewers of."""
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
        """
        Custom save logic to track when an application is reviewed.

        If the application is accepted or rejected, the reviewed details are saved.

        Args:
            request (HttpRequest): The HTTP request object.
            obj (Application): The application object being saved.
            form (Form): The form being used to save the application.
            change (bool): Whether the object is being changed or created.
        """
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
    """
    Custom admin interface for the Interview model.
    Handles permissions, read-only fields, list display, and custom save behaviour.
    """

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
        """Users can only view applications for vacancies they are reviewers of."""
        if obj is None:
            return True
        return request.user.is_superuser or obj.application.vacancy.reviewers.filter(id=request.user.id).exists()

    def has_change_permission(self, request, obj=None):
        """Users can only change applications for vacancies they are reviewers of."""
        if obj is None:
            return True
        return request.user.is_superuser or request.user in obj.vacancy.reviewers.all()

    def has_delete_permission(self, request, obj=None):
        """Users can only delete applications for vacancies they are reviewers of."""
        if request.user.is_superuser or request.user.groups.filter(name="admin"):
            return True
        return False

    def get_readonly_fields(self, request, obj=None):
        """
        Returns the list of read-only fields based on the interview's status.

        Args:
            request: The HTTP request object.
            obj: The object for which the read-only fields are being determined.

        Returns:
            List of read-only field names.
        """
        if obj is not None and obj.status in [
            Interview.STATUS.ACCEPTED,
            Interview.STATUS.REJECTED,
        ]:
            return [field.name for field in self.model._meta.fields]
        return super().get_readonly_fields(request, obj)

    def save_model(self, request, obj, form, change):
        """
        Custom save logic for the Interview model.

        If the status is not set, it is automatically set to 'SCHEDULED' before saving.

        Args:
            request: The HTTP request object.
            obj: The interview object being saved.
            form: The form used to save the object.
            change: A boolean indicating if the object is being changed or created.

        Returns:
            None
        """
        if not obj.status:
            obj.clean()  # Run model validation
            obj.status = Interview.STATUS.SCHEDULED
        super().save_model(request, obj, form, change)


# **********************************************************************************************
#                                       SUBSCRIBER
# **********************************************************************************************
@admin.register(Subscriber)
class SubscriberAdmin(ModelAdmin):
    """
    Custom admin interface for the Subscriber model.
    Manages the display of subscriber information, with restricted permissions to prevent adding new subscribers.
    """

    model = Subscriber
    readonly_fields = ["email", "vacancy_types", "subscribed"]

    def has_add_permission(self, request):
        """
        Determines if the user has permission to add a new Subscriber.

        Args:
            request: The HTTP request object.

        Returns:
            False to prevent adding new subscribers via the admin interface.
        """
        return False
