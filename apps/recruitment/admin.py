from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_objects_for_user
from import_export.admin import ExportActionModelAdmin
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.filters.admin import RangeDateFilter
from unfold.contrib.import_export.forms import SelectableFieldsExportForm

from .forms import (
    ApplicationForm,
    ApplicationReviewForm,
    InterviewForm,
    MinimumRequirementsAddForm,
    MinimumRequirementsAnswerForm,
    VacancyForm,
)
from .models import (
    ApplicantResponse,
    Application,
    Interview,
    Location,
    MinimumRequirement,
    Subscriber,
    Vacancy,
    VacancyType,
)

# **********************************************************************************************
#                                       VACANCY
# **********************************************************************************************
admin.site.register(VacancyType, ModelAdmin)


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
    ]
    list_filter = [
        "title",
        "deadline",
        "is_public",
    ]
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
        return self.has_permission(request, obj, "view")

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return super().has_change_permission(request, obj)
        elif obj is not None and obj.deadline > timezone.now():
            return False
        else:
            return self.has_permission(request, obj, "change")

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
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
    model = ApplicantResponse
    readonly_fields = ["requirement", "answer"]
    tab = True

    def has_add_permission(self, request, obj=None):
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
        "cv",
        "reviewed_by",
        "reviewed_at",
    ]
    form = ApplicationReviewForm
    list_display = [
        "first_name",
        "last_name",
        "email",
        "vacancy",
        "status",
    ]
    list_filter = (
        "first_name",
        "last_name",
        "email",
        "vacancy",
    )
    search_fields = (
        "first_name",
        "last_name",
        "email",
    )

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
        return self.has_permission(request, obj, "view")

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
            obj.reviewed_at = timezone.now()
            obj.reviewed_by = request.user

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

    def has_add_permission(self, request):
        return False


# **********************************************************************************************
#                                 RECRUITMENT DASHBOARD
# **********************************************************************************************
class RecruitmentAdminArea(admin.AdminSite):
    site_header = "Recruitment Admin"
    site_title = "Recruitment"
    index_title = "Recruitment Dashboard"
    index_template = ""
    enable_nav_sidebar = False
    login_template = "recruitment/admin/login.html"
    logout_template = "recruitment/admin/logout.html"
    password_change_template = "recruitment/admin/password_change.html"

    def has_permission(self, request):
        return (
            request.user.is_active
            and request.user.groups.filter(name="recruiter").exists()
        )


recruitment_admin_site = RecruitmentAdminArea(name="Recruitment")
recruitment_admin_site.register(Application, ApplicationAdmin)
recruitment_admin_site.register(Vacancy, VacancyAdmin)
recruitment_admin_site.register(Interview, InterviewAdmin)
