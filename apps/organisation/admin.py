from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.import_export.forms import ImportForm, SelectableFieldsExportForm

from .models import CostCentre, Department, Division, Position, Region, Town


class TownInline(TabularInline):
    model = Town
    extra = 1
    # tab = True


@admin.register(Region)
class RegionAdmin(ModelAdmin):
    inlines = [TownInline]


class DepartmentInline(TabularInline):
    model = Department
    extra = 1
    # tab = True


@admin.register(Division)
class DivisionAdmin(ModelAdmin):
    inlines = [DepartmentInline]


@admin.register(CostCentre)
class CostCentreAdmin(ModelAdmin, ImportExportActionModelAdmin):
    model = CostCentre
    export_form_class = SelectableFieldsExportForm
    import_form_class = ImportForm


class PositionInline(TabularInline):
    model = Position
    extra = 1
    # tab = True


@admin.register(Position)
class PositionAdmin(ModelAdmin, ImportExportActionModelAdmin):
    model = Position
    export_form_class = SelectableFieldsExportForm
    import_form_class = ImportForm
    # inlines = [PositionInline]
