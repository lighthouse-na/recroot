from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.html import format_html
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_objects_for_user
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
class VacancyAdmin(ModelAdmin, GuardedModelAdmin):
    """
    Custom admin interface for managing Vacancy models.

    This class customises the admin interface for managing Vacancy objects.
    It provides functionality for filtering, permissions, and accessing the
    Vacancy data based on user permissions.

    Attributes:
        form: The form used for the Vacancy model in the admin interface.
        list_display: The fields to display in the Vacancy model list view.
        list_filter: The fields to filter Vacancy objects by in the list view.
        filter_horizontal: The fields to display with a horizontal filter widget.
        inlines: Inline models (MinimumRequirementsAddInline) to be displayed.
    """

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
    # list_editable = ["is_published"]
    filter_horizontal = ["town"]
    inlines = [MinimumRequirementsAddInline]

    def get_model_objects(self, request, action=None, klass=None):
        """
        Retrieves the objects for a user based on permissions and actions.

        This method returns objects for the model that a user has permissions to view,
        change, or delete. It checks the permissions for the specified action and model.

        Args:
            request (HttpRequest): The HTTP request object.
            action (str): The action to check permissions for (e.g., "view").
            klass (Model): The model class to check permissions for.

        Returns:
            queryset: A queryset of model objects that the user has permission to access.
        """
        opts = self.opts
        actions = [action] if action else ["view"]
        klass = klass if klass else opts.model
        model_name = klass._meta.model_name
        return get_objects_for_user(
            user=request.user,
            perms=[f"{perm}_{model_name}" for perm in actions],
            klass=klass,
            any_perm=True,
        )

    def has_permission(self, request, obj, action):
        """
        Checks if a user has permission to perform a specific action on a model object.

        This method checks whether a user has the required permission for a specific
        action (e.g., "view", "change", "delete") on a given model object.

        Args:
            request (HttpRequest): The HTTP request object.
            obj (Model): The model object to check permissions on.
            action (str): The action to check permission for (e.g., "view").

        Returns:
            bool: True if the user has permission for the specified action, False otherwise.
        """
        opts = self.opts
        code_name = f"{action}_{opts.model_name}"
        if obj:
            return request.user.has_perm(f"{opts.app_label}.{code_name}", obj)
        return self.get_model_objects(request).exists()

    def has_view_permission(self, request, obj=None):
        """
        Checks if a user has permission to view a model object.

        This method checks if a user has permission to view the specified model object,
        either by being a superuser or by checking specific permissions for the object.

        Args:
            request (HttpRequest): The HTTP request object.
            obj (Model, optional): The model object to check permissions for.

        Returns:
            bool: True if the user has permission to view the object, False otherwise.
        """
        if request.user.is_superuser or request.user.groups.filter(name="admin"):
            return True
        return self.has_permission(request, obj, "view")

    def has_change_permission(self, request, obj=None):
        """
        Checks if a user has permission to change a model object.

        This method checks if a user has permission to change the specified model object,
        either by being a superuser, belonging to the "admin" group, or if the object
        is not published.

        Args:
            request (HttpRequest): The HTTP request object.
            obj (Model, optional): The model object to check permissions for.

        Returns:
            bool: True if the user has permission to change the object, False otherwise.
        """
        if request.user.is_superuser or request.user.groups.filter(name="admin"):
            return super().has_change_permission(request, obj)
        if obj is not None and obj.is_published:
            return False
        return self.has_permission(request, obj, "change")

    def has_delete_permission(self, request, obj=None):
        """
        Checks if a user has permission to delete a model object.

        This method checks if a user has permission to delete the specified model object,
        either by being a superuser, belonging to the "admin" group, or if the user
        has the required delete permission for the object.

        Args:
            request (HttpRequest): The HTTP request object.
            obj (Model, optional): The model object to check permissions for.

        Returns:
            bool: True if the user has permission to delete the object, False otherwise.
        """
        if request.user.is_superuser or request.user.groups.filter(name="admin"):
            return super().has_delete_permission(request, obj)
        return self.has_permission(request, obj, "delete")

    def has_module_permission(self, request):
        """
        Checks if the user has permission to view the Vacancy model module.

        This method checks whether a user has permission to access the Vacancy module
        based on their permissions for the Vacancy objects.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            bool: True if the user has permission to access the module, False otherwise.
        """
        if super().has_module_permission(request):
            return True
        return self.get_model_objects(request).exists()

    def get_queryset(self, request):
        """
        Returns the queryset of Vacancy objects based on user permissions.

        This method overrides the default `get_queryset` to return only the Vacancy
        objects the user has permission to access, depending on their user role.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            queryset: A queryset of Vacancy objects based on the user's permissions.
        """
        if request.user.is_superuser:
            return super().get_queryset(request)
        data = self.get_model_objects(request)
        return data


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

    def has_add_permission(self, request, obj=None):
        """
        Determines whether the user has permission to add a new MinimumRequirementAnswer.

        This method returns False, preventing the addition of new answers through
        the admin interface. The answers are assumed to be pre-populated.

        Args:
            request (HttpRequest): The HTTP request object.
            obj (Model, optional): The object being edited, if any.

        Returns:
            bool: False (users cannot add new answers).
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Determines whether the user has permission to delete a MinimumRequirementAnswer.

        This method returns False, preventing the deletion of answers through the
        admin interface.

        Args:
            request (HttpRequest): The HTTP request object.
            obj (Model, optional): The object being edited, if any.

        Returns:
            bool: False (users cannot delete answers).
        """
        return False

    def has_change_permission(self, request, obj=None):
        """
        Determines whether the user has permission to change a MinimumRequirementAnswer.

        This method returns False, preventing changes to the answers through the
        admin interface.

        Args:
            request (HttpRequest): The HTTP request object.
            obj (Model, optional): The object being edited, if any.

        Returns:
            bool: False (users cannot change answers).
        """
        return False

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
class ApplicationAdmin(ModelAdmin, GuardedModelAdmin, ExportActionModelAdmin):
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

    def get_model_objects(self, request, action=None, klass=None):
        """
        Retrieves model objects for the current user with the required permissions.

        Custom method to fetch application objects that the current user has permission
        to view or modify, based on the action (e.g., "view", "change").

        Args:
            request (HttpRequest): The HTTP request object.
            action (str): The action to check for permissions (optional).
            klass (Model): The model class for the object (optional).

        Returns:
            queryset: A filtered queryset of model objects.
        """
        opts = self.opts
        actions = [action] if action else ["view"]
        klass = klass if klass else opts.model
        model_name = klass._meta.model_name
        return get_objects_for_user(
            user=request.user,
            perms=[f"{perm}_{model_name}" for perm in actions],
            klass=klass,
            any_perm=True,
        )

    def has_permission(self, request, obj, action):
        """
        Checks if the user has permission to perform an action on the object.

        Args:
            request (HttpRequest): The HTTP request object.
            obj (Model, optional): The object being edited, if any.
            action (str): The action (view, change, delete, etc.).

        Returns:
            bool: True if the user has permission, otherwise False.
        """
        opts = self.opts
        code_name = f"{action}_{opts.model_name}"
        if obj:
            return request.user.has_perm(f"{opts.app_label}.{code_name}", obj)
        return self.get_model_objects(request).exists()

    def has_view_permission(self, request, obj=None):
        """
        Determines if the user has permission to view the application.

        Superusers and admin group members can always view. Other users can be restricted.

        Args:
            request (HttpRequest): The HTTP request object.
            obj (Model, optional): The object being viewed.

        Returns:
            bool: True if the user has permission to view the application.
        """
        if request.user.is_superuser or request.user.groups.filter(name__in=["admin", "recruiter"]).exists():
            return True
        return False

    def has_add_permission(self, request):
        """
        Prevents adding new Application objects.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            bool: False (users cannot add new applications).
        """
        return False

    def has_change_permission(self, request, obj=None):
        """
        Checks if the user can change an existing Application.

        - Superusers can change any application.
        - Admins can change applications, except those already submitted.
        - Users cannot change applications after submission if not the user who submitted it.

        Args:
            request (HttpRequest): The HTTP request object.
            obj (Model, optional): The object being changed.

        Returns:
            bool: True if the user can change the application, otherwise False.
        """
        if request.user.is_superuser:
            return super().has_change_permission(request, obj)
        self.has_permission(request, obj, "change")
        if obj is not None and obj.status != "submitted":
            return False
        return True

    def has_module_permission(self, request):
        """
        Checks if the user has permission to access the Application model.

        Returns:
            bool: True if the user has permission, otherwise False.
        """
        if super().has_module_permission(request):
            return True
        return self.get_model_objects(request).exists()

    def get_queryset(self, request):
        """
        Custom queryset to filter applications based on the user's permissions.

        Superusers get all applications. Non-superusers only see applications they have
        permission to view.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            queryset: A filtered queryset of applications.
        """
        if request.user.is_superuser:
            return super().get_queryset(request)
        data = self.get_model_objects(request)
        return data

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
class InterviewAdmin(ModelAdmin, GuardedModelAdmin, ExportActionModelAdmin):
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

    def get_model_objects(self, request, action=None, klass=None):
        """
        Returns the queryset of objects the user has permission to access.

        Args:
            request: The HTTP request object.
            action: The action (view, change, delete).
            klass: The model class to filter the queryset by. If None, defaults to the current model.

        Returns:
            Queryset of objects the user has permission to access.
        """
        opts = self.opts
        actions = [action] if action else ["view"]
        klass = klass if klass else opts.model
        model_name = klass._meta.model_name
        return get_objects_for_user(
            user=request.user,
            perms=[f"{perm}_{model_name}" for perm in actions],
            klass=klass,
            any_perm=True,
        )

    def has_permission(self, request, obj, action):
        """
        Checks if the user has the specified permission on the given object.

        Args:
            request: The HTTP request object.
            obj: The object for which the permission is being checked.
            action: The action (view, change, delete).

        Returns:
            True if the user has permission; False otherwise.
        """
        opts = self.opts
        code_name = f"{action}_{opts.model_name}"
        if obj:
            return request.user.has_perm(f"{opts.app_label}.{code_name}", obj)
        return self.get_model_objects(request).exists()

    def has_view_permission(self, request, obj=None):
        """
        Determines if the user has view permission on the given object.

        Args:
            request: The HTTP request object.
            obj: The object for which the permission is being checked.

        Returns:
            True if the user has view permission; False otherwise.
        """
        return self.has_permission(request, obj, "view")

    def has_delete_permission(self, request, obj=None):
        """
        Determines if the user has delete permission on the given object.

        Args:
            request: The HTTP request object.
            obj: The object for which the permission is being checked.

        Returns:
            True if the user has delete permission; False otherwise.
        """
        if request.user.is_superuser:
            return super().has_change_permission(request, obj)
        return False

    def has_change_permission(self, request, obj=None):
        """
        Determines if the user has change permission on the given object.

        Args:
            request: The HTTP request object.
            obj: The object for which the permission is being checked.

        Returns:
            True if the user has change permission; False otherwise.
        """
        if request.user.is_superuser:
            return super().has_change_permission(request, obj)
        if obj is not None and obj.status in [
            Interview.STATUS.ACCEPTED,
            Interview.STATUS.REJECTED,
        ]:
            return False  # Deny changes if status is ACCEPTED or REJECTED
        return self.has_permission(request, obj, "change")

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

    def has_module_permission(self, request):
        """
        Determines if the user has permission to access the module.

        Args:
            request: The HTTP request object.

        Returns:
            True if the user has module permission; False otherwise.
        """
        if super().has_module_permission(request):
            return True
        return self.get_model_objects(request).exists()

    def get_queryset(self, request):
        """
        Returns the queryset of interviews based on the user's permissions.

        Args:
            request: The HTTP request object.

        Returns:
            A filtered queryset of interviews the user can access.
        """
        if request.user.is_superuser:
            return super().get_queryset(request)
        data = self.get_model_objects(request)
        return data

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
