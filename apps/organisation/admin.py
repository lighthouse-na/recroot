from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from unfold.admin import ModelAdmin, TabularInline
from import_export.admin import ImportExportActionModelAdmin
from unfold.contrib.import_export.forms import ImportForm, SelectableFieldsExportForm

from .models import CostCentre, Department, Division, Position, Region, Town


class TownInline(TabularInline):
    model = Town
    extra = 1
    # tab = True


@admin.register(Region)
class RegionAdmin(ModelAdmin, GuardedModelAdmin):
    inlines = [TownInline]


class DepartmentInline(TabularInline):
    model = Department
    extra = 1
    # tab = True


@admin.register(Division)
class DivisionAdmin(ModelAdmin, GuardedModelAdmin):
    inlines = [DepartmentInline]


@admin.register(CostCentre)
class CostCentreAdmin(ModelAdmin, GuardedModelAdmin, ImportExportActionModelAdmin):
    model = CostCentre
    export_form_class = SelectableFieldsExportForm
    import_form_class = ImportForm


class PositionInline(TabularInline):
    model = Position
    extra = 1
    # tab = True
@admin.register(Position)
class PositionAdmin(ModelAdmin, GuardedModelAdmin, ImportExportActionModelAdmin):
    model = Position
    export_form_class = SelectableFieldsExportForm
    import_form_class = ImportForm
    # inlines = [PositionInline]