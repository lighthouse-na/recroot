from django.contrib import admin
from import_export.admin import ExportActionModelAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.import_export.forms import SelectableFieldsExportForm

from .forms import FinancialAssistanceApplicationForm
from .models import (
    Bursary,
    BursaryApplications,
    FinancialAssistance,
    FinancialAssistanceApplication,
)

admin.site.register(FinancialAssistance, ModelAdmin)
admin.site.register(Bursary, ModelAdmin)
admin.site.register(BursaryApplications, ModelAdmin)


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
    ]
    list_filter = (
        "applicant",
        "study_mode",
    )

    def has_permission(self, request, obj, action):
        opts = self.opts
        code_name = f"{action}_{opts.model_name}"
        if obj:
            return request.user.has_perm(f"{opts.app_label}.{code_name}", obj)
        else:
            return self.get_model_objects(request).exists()

    # def has_view_permission(self, request, obj=None):
    #     return self.has_permission(request, obj, "view")

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

    def save_model(self, request, obj, form, change):
        obj.applicant = request.user
        super().save_model(request, obj, form, change)
