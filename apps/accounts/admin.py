from allauth.account.admin import EmailAddressAdmin as BaseEmailAddressAdmin
from allauth.account.models import EmailAddress
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from unfold.admin import ModelAdmin, TabularInline

from .models import Profile

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(EmailAddress)


class ProfileInline(TabularInline):
    model = Profile
    can_delete = False
    max_num = 1
    extra = 0
    tab = True


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    readonly_fields = ["is_superuser", "date_joined", "last_login"]
    inlines = [ProfileInline]


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin): ...


@admin.register(EmailAddress)
class EmailAddressAdmin(BaseEmailAddressAdmin, ModelAdmin): ...
