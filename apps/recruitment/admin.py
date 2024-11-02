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
class VacancyAdmin(ModelAdmin, GuardedModelAdmin):
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
        opts = self.opts
        code_name = f"{action}_{opts.model_name}"
        if obj:
            return request.user.has_perm(f"{opts.app_label}.{code_name}", obj)
        else:
            return self.get_model_objects(request).exists()

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.groups.filter(name="admin"):
            return True
        return self.has_permission(request, obj, "view")

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.groups.filter(name="admin"):
            return super().has_change_permission(request, obj)
        elif obj is not None and obj.is_published:
            return False
        else:
            return self.has_permission(request, obj, "change")

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.groups.filter(name="admin"):
            return super().has_delete_permission(request, obj)
        else:
            return self.has_permission(request, obj, "delete")

    def has_module_permission(self, request):
        if super().has_module_permission(request):
            return True
        return self.get_model_objects(request).exists()

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            data = self.get_model_objects(request)
            return data


# **********************************************************************************************
#                                       APPLICATION
# **********************************************************************************************
class ApplicantResponseInline(TabularInline):
    model = MinimumRequirementAnswer
    fields = ["answer"]
    tab = True

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if self.parent_model == Application and hasattr(self, "parent_obj"):
            qs = qs.filter(application=self.parent_obj)
        return qs

    def get_formset(self, request, obj=None, **kwargs):
        self.parent_obj = obj
        return super().get_formset(request, obj, **kwargs)

    def has_module_permission(self, request):
        if super().has_module_permission(request):
            return False


@admin.register(Application)
class ApplicationAdmin(ModelAdmin, GuardedModelAdmin, ExportActionModelAdmin):
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
    list_filter = (
        "vacancy",
        "status",
        "submitted_at",
    )
    search_fields = (
        "first_name",
        "last_name",
        "email",
    )
    ordering = ("submitted_at",)
    inlines = [ApplicantResponseInline]

    def get_model_objects(self, request, action=None, klass=None):
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
        opts = self.opts
        code_name = f"{action}_{opts.model_name}"
        if obj:
            return request.user.has_perm(f"{opts.app_label}.{code_name}", obj)
        else:
            return self.get_model_objects(request).exists()

    def has_view_permission(self, request, obj=None):
        # return self.has_permission(request, obj, "view")
        if (
            request.user.is_superuser
            or request.user.groups.filter(name="admin").exists()
        ):
            return True
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return super().has_change_permission(request, obj)
        else:
            self.has_permission(request, obj, "change")
            if obj is not None and obj.status != "submitted":
                return False
            return True

    def has_module_permission(self, request):
        if super().has_module_permission(request):
            return True
        return self.get_model_objects(request).exists()

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            data = self.get_model_objects(request)
            return data

    def view_cv(self, obj):
        if obj.cv:
            return format_html('<a href="{}" target="_blank">View CV</a>', obj.cv.url)
        return "No CV uploaded"

    def save_model(self, request, obj, form, change):

        if obj.status in [Application.STATUS.ACCEPTED, Application.STATUS.REJECTED]:
            user = get_user_model().objects.get(id=request.user.id)

            obj.reviewed_at = timezone.now()
            obj.reviewed_by = user

        super().save_model(request, obj, form, change)

    view_cv.short_description = "CV"


# **********************************************************************************************
#                                       INTERVIEW
# **********************************************************************************************
admin.site.register(Location, ModelAdmin)


@admin.register(Interview)
class InterviewAdmin(ModelAdmin, GuardedModelAdmin, ExportActionModelAdmin):
    form = InterviewForm
    export_form_class = SelectableFieldsExportForm
    readonly_fields = ["application"]
    list_display = ["application", "status", "schedule_datetime"]
    list_filter = ["status", ("schedule_datetime", RangeDateFilter)]
    list_filter_submit = True

    def get_model_objects(self, request, action=None, klass=None):
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
        opts = self.opts
        code_name = f"{action}_{opts.model_name}"
        if obj:
            return request.user.has_perm(f"{opts.app_label}.{code_name}", obj)
        else:
            return self.get_model_objects(request).exists()

    def has_view_permission(self, request, obj=None):
        return self.has_permission(request, obj, "view")

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return super().has_change_permission(request, obj)
        else:
            return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return super().has_change_permission(request, obj)
        else:
            self.has_permission(request, obj, "change")
            if obj is not None and obj.status == None:
                return False
            return True

    def get_readonly_fields(self, request, obj=None):
        if obj is not None and obj.status in [
            Interview.STATUS.ACCEPTED,
            Interview.STATUS.REJECTED,
        ]:
            return [field.name for field in self.model._meta.fields]
        return super().get_readonly_fields(request, obj)

    def has_module_permission(self, request):
        if super().has_module_permission(request):
            return True
        return self.get_model_objects(request).exists()

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            data = self.get_model_objects(request)
            return data

    def save_model(self, request, obj, form, change):
        if not obj.status:
            obj.clean()
            obj.status = Interview.STATUS.SCHEDULED
        super().save_model(request, obj, form, change)


# **********************************************************************************************
#                                       SUBSCRIBER
# **********************************************************************************************
@admin.register(Subscriber)
class SubscriberAdmin(ModelAdmin):
    model = Subscriber
    readonly_fields = ["email", "vacancy_types", "subscribed"]

    def has_add_permission(self, request):
        return False
