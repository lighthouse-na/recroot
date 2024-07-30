from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import Region, Town


# admin.site.register(Town)
class TownInline(TabularInline):
    model = Town
    extra = 1
    # tab = True


@admin.register(Region)
class RegionAdmin(ModelAdmin):
    inlines = [TownInline]
