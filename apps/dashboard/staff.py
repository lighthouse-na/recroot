from datetime import datetime
from typing import Dict, List

from django.contrib import admin
from django.http import HttpRequest
from unfold.admin import ModelAdmin
from unfold.sites import UnfoldAdminSite

from apps.accounts.admin import ProfileAdmin, QualificationAdmin, CertificationAdmin
from apps.accounts.models import Certification, Profile, Qualification
from apps.recruitment.models import Vacancy, Interview, Application
from apps.finaid.models import (
    BursaryAdvert,
    FinancialAssistanceAdvert,
    FinancialAssistanceApplication,
)
from apps.finaid.admin import FinancialAssistanceAdmin


# @admin.register(Vacancy)
class VacancyAdmin(ModelAdmin):
    list_display = ["title", "vacancy_type", "deadline", "is_public"]
    list_filter = []
    search_fields = []
    ordering = ["title", "vacancy_type", "deadline", "is_public"]

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(user=request.user)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return super().has_view_permission(request, obj)


# @admin.register(Application)
class ApplicationAdmin(ModelAdmin):
    list_display = ["vacancy", "status", "submitted_at"]
    list_filter = []
    search_fields = []
    ordering = []

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs
        return qs.filter(email=request.user.email)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return super().has_view_permission(request, obj)


# @admin.register(Interview)
class InterviewAdmin(ModelAdmin):
    list_display = ["application", "status"]
    list_filter = []
    search_fields = []
    ordering = []

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return super().has_view_permission(request, obj)


# class StaffDashboard(admin.AdminSite):
class StaffDashboard(UnfoldAdminSite):
    site_header = "Staff Dashboard"
    site_title = "Staff Dashboard"
    # index_title = "Staff Dashboard"
    index_template = "dashboard/staff/index.html"
    enable_nav_sidebar = True
    # login_template = "admin/login.html"
    # logout_template = "admin/logout.html"
    # password_change_template = "admin/password_change.html"

    def each_context(self, request):
        return super().each_context(request)

    def index(self, request, extra_context=None):
        vacancies = Vacancy.objects.filter(
            is_published=True, deadline__gt=datetime.now()
        ).order_by("-created_at")
        bursaries = BursaryAdvert.objects.filter(
            is_visible=True, deadline__gt=datetime.now()
        ).order_by("-created_at")
        financial_assistance_adverts = FinancialAssistanceAdvert.objects.filter(
            is_visible=True, deadline__gt=datetime.now()
        ).order_by("-created_at")
        extra_context = {
            **self.each_context(request),
            "vacancies": vacancies,
            "bursaries": bursaries,
            "financial_assistance_adverts": financial_assistance_adverts,
            "title": request.user.profile,
        }
        return super().index(request, extra_context)

    def has_permission(self, request):
        return request.user.is_active and request.user.is_authenticated

    def get_sidebar_list(self, request: HttpRequest):
        return super().get_sidebar_list(request)


staff_dashboard_site = StaffDashboard(name="Staff")
staff_dashboard_site.register(Profile, ProfileAdmin)
staff_dashboard_site.register(Qualification, QualificationAdmin)
staff_dashboard_site.register(Certification, CertificationAdmin)
# staff_dashboard_site.register(Vacancy, VacancyAdmin)
staff_dashboard_site.register(Application, ApplicationAdmin)
staff_dashboard_site.register(Interview, InterviewAdmin)
staff_dashboard_site.register(FinancialAssistanceApplication, FinancialAssistanceAdmin)
