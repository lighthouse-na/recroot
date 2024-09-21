from datetime import datetime
from typing import Dict, List

from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from unfold.admin import ModelAdmin
from unfold.sites import UnfoldAdminSite

from apps.accounts.admin import CertificationAdmin, QualificationAdmin
from apps.accounts.models import Certification, Qualification
from apps.finaid.admin import FinancialAssistanceAdmin
from apps.finaid.models import (
    BursaryAdvert,
    FinancialAssistanceAdvert,
    FinancialAssistanceApplication,
)
from apps.pages.models import Announcement
from apps.recruitment.models import Application, Interview, Vacancy

from .views import StaffLoginView


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

    def index(self, request, extra_context=None):
        announcements = Announcement.objects.filter(
            deadline__gt=datetime.now(),
            is_visible=True,
        )
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
            "announcements": announcements,
            "vacancies": vacancies,
            "bursaries": bursaries,
            "financial_assistance_adverts": financial_assistance_adverts,
            "title": request.user,
        }
        return super().index(request, extra_context)

    def login(self, request, extra_context=None):
        return StaffLoginView.as_view()(request)

    def has_permission(self, request):
        return request.user.is_active and request.user.is_authenticated

    def get_sidebar_list(self, request: HttpRequest):
        return super().get_sidebar_list(request)


staff_dashboard_site = StaffDashboard(name="Staff")
staff_dashboard_site.register(Qualification, QualificationAdmin)
staff_dashboard_site.register(Certification, CertificationAdmin)
# staff_dashboard_site.register(Vacancy, VacancyAdmin)
staff_dashboard_site.register(Application, ApplicationAdmin)
staff_dashboard_site.register(Interview, InterviewAdmin)
staff_dashboard_site.register(FinancialAssistanceApplication, FinancialAssistanceAdmin)
