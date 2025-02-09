from django.contrib import admin
from unfold.admin import ModelAdmin

from .forms import FAQForm
from .models import FAQ, Announcement


@admin.register(Announcement)
class AnnouncementAdmin(ModelAdmin): ...


@admin.register(FAQ)
class FAQAdmin(ModelAdmin):
    form = FAQForm
