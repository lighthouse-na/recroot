from django.contrib import admin
from import_export.admin import ExportActionModelAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.import_export.forms import SelectableFieldsExportForm

from .forms import (
    BursaryAdvertForm,
    BursaryApplicationForm,
    FinancialAssistanceApplicationForm,
)
from .models import (
    BursaryAdvert,
    BursaryApplication,
    FinancialAssistanceAdvert,
    FinancialAssistanceApplication,
)

# admin.site.register(FinancialAssistanceAdvert, ModelAdmin)
# admin.site.register(Bursary, ModelAdmin)
# admin.site.register(BursaryApplications, ModelAdmin)


@admin.register(FinancialAssistanceAdvert)
class FinancialAssistanceAdvertAdmin(ModelAdmin, ExportActionModelAdmin):
    model = FinancialAssistanceAdvert


@admin.register(FinancialAssistanceApplication)
class FinancialAssistanceAdmin(ModelAdmin, ExportActionModelAdmin):
    model = FinancialAssistanceApplication
    form = FinancialAssistanceApplicationForm
    export_form_class = SelectableFieldsExportForm
    readonly_fields = [
        "applicant",
        "status",
    ]
    list_display = [
        "applicant",
        "study_mode",
        "status",
    ]
    list_filter = (
        "applicant",
        "study_mode",
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if (
            request.user.is_superuser
            or request.user.groups.filter(name="admin").exists()
        ):
            return qs
        return qs.filter(applicant=request.user)

    def has_permission(self, request, obj, action):
        opts = self.opts
        code_name = f"{action}_{opts.model_name}"
        if obj:
            return request.user.has_perm(f"{opts.app_label}.{code_name}", obj)
        # else:
        #     return self.get_model_objects(request).exists()

    # def has_view_permission(self, request, obj=None):
    #     return self.has_permission(request, obj, "view")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        if (
            request.user.is_superuser
            or request.user.groups.filter(name="admin").exists()
        ):
            return super().has_change_permission(request, obj)
        else:
            self.has_permission(request, obj, "change")
            if obj is not None and obj.status != "submitted":
                return False
            return True

    def save_model(self, request, obj, form, change):
        obj.applicant = request.user
        super().save_model(request, obj, form, change)


@admin.register(BursaryApplication)
class BursaryApplicationsAdmin(ModelAdmin, ExportActionModelAdmin):
    model = BursaryApplication
    form = BursaryApplicationForm
    export_form_class = SelectableFieldsExportForm
    readonly_fields = [
        "bursary",
        "status",
    ]
    list_display = [
        "bursary",
        "status",
    ]
    list_filter = (
        "bursary",
        "status",
    )

    def has_add_permission(self, request):
        return False

    # def has_view_permission(self, request):
    #     return self.has_view_permission(request, "view")


@admin.register(BursaryAdvert)
class BursaryAdvertAdmin(ModelAdmin, ExportActionModelAdmin):
    model = BursaryAdvert
    form = BursaryAdvertForm
    export_form_class = SelectableFieldsExportForm
    # readonly_fields = []

    def has_add_permission(self, request):
        if (
            request.user.is_superuser
            or request.user.groups.filter(name="admin").exists()
        ):
            return super().has_change_permission(request)
