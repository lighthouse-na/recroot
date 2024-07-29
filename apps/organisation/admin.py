from django.contrib import admin
from .models import Town, Region
from unfold.admin import ModelAdmin, TabularInline


# admin.site.register(Town)
class TownInline(TabularInline):
    model = Town
    extra = 1
    # tab = True


@admin.register(Region)
class RegionAdmin(ModelAdmin):
    inlines = [TownInline]
