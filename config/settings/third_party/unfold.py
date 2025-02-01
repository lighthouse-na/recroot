import os

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

module = os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

UNFOLD = {
    "SITE_TITLE": "Telecom Namibia",
    "SITE_HEADER": "Telecom Namibia",
    "SITE_SYMBOL": "speed",  # symbol from icon set
    "SHOW_HISTORY": True,  # show/hide "History" button, default: True
    "SHOW_VIEW_ON_SITE": True,  # show/hide "View on site" button, default: True
    "COLORS": {
        "primary": {
            "DEFAULT": "#E56114",
            "50": "#FFF7ED",
            "100": "#FFEDD5",
            "200": "#FED7AA",
            "300": "#FDBA74",
            "400": "#FB923C",
            "500": "#F97316",
            "600": "#EA580C",
            "700": "#C2410C",
            "800": "#9A3412",
            "900": "#7C2D12",
            "950": "#66240D",
        },
        "secondary": {
            "DEFAULT": "#0057B8",
            "50": "#F0F5F9",
            "100": "#D9E2EC",
            "200": "#A0AEC0",
            "300": "#6886A0",
            "400": "#4F748E",
            "500": "#013569",
            "600": "#012D5A",
            "700": "#00274E",
            "800": "#002145",
            "900": "#001D3E",
            "950": "#001833",
        },
    },
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "en": "🇬🇧",
                "fr": "🇫🇷",
                "nl": "🇧🇪",
            },
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                # "title": _("Navigation"),
                # "separator": True,  # Top border
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": "/" + ("admin/" if module == "config.settings.development" else "oshimashakula/"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Auth"),
                        "icon": "people",
                        "link": "/"
                        + ("admin/" if module == "config.settings.development" else "oshimashakula/")
                        + "accounts/user",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Organisation"),
                        "icon": "home",
                        "link": "/"
                        + ("admin/" if module == "config.settings.development" else "oshimashakula/")
                        + "organisation",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Recruitment"),
                        "icon": "people",
                        "link": "/"
                        + ("admin/" if module == "config.settings.development" else "oshimashakula/")
                        + "recruitment",
                        "permission": lambda request: request.user.has_perm("view_application"),
                    },
                    # -----------------------------------------------------------------------
                    # Admin Dashboard Urls
                    # -----------------------------------------------------------------------
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": "/"
                        + (
                            "dashboard/admin/"
                            if module == "config.settings.development"
                            else "dashboard/telecom/administrator/"
                        )
                        + "accounts/user",
                        "permission": lambda request: request.user.groups.filter(name="admin").exists()
                        and request.path.startswith("/dashboard/admin/"),
                    },
                    {
                        "title": _("Auth"),
                        "icon": "people",
                        "link": "/"
                        + (
                            "dashboard/admin/"
                            if module == "config.settings.development"
                            else "dashboard/telecom/administrator/"
                        )
                        + "accounts/user",
                        "permission": lambda request: request.user.groups.filter(name="admin").exists()
                        and request.path.startswith("/dashboard/admin/"),
                    },
                    {
                        "title": _("Organisation"),
                        "icon": "home",
                        "link": "/"
                        + (
                            "dashboard/admin/"
                            if module == "config.settings.development"
                            else "dashboard/telecom/administrator/"
                        )
                        + "accounts/user",
                        "permission": lambda request: request.user.groups.filter(name="admin").exists()
                        and request.path.startswith("/dashboard/admin/"),
                    },
                    {
                        "title": _("Recruitment"),
                        "icon": "people",
                        "link": "/"
                        + (
                            "dashboard/admin/"
                            if module == "config.settings.development"
                            else "dashboard/telecom/administrator/"
                        )
                        + "accounts/user",
                        "permission": lambda request: request.user.groups.filter(name="admin").exists()
                        and request.path.startswith("/dashboard/admin/"),
                    },
                    # -----------------------------------------------------------------------
                    # Staff Dashboard Urls
                    # -----------------------------------------------------------------------
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("Staff:index"),
                        "permission": lambda request: request.path.startswith("/dashboard/staff/"),
                        "permission": lambda request: request.user.groups.filter(name="staff").exists()
                        and request.path.startswith("/dashboard/staff/"),
                    },
                    {
                        "title": _("Recruitment"),
                        "icon": "people",
                        "link": "/dashboard/staff/recruitment",
                        "permission": lambda request: request.user.groups.filter(name="staff").exists()
                        and request.path.startswith("/dashboard/staff/"),
                    },
                ],
            },
        ],
    },
    "TABS": [
        {
            "models": [
                "accounts.user",
                "auth.group",
                "account.emailaddress",
            ],
            "items": [
                {
                    "title": _("Users"),
                    "link": "/"
                    + ("admin/" if module == "config.settings.development" else "oshimashakula/")
                    + "accounts/user",
                    "permission": lambda request: request.user.is_superuser or request.user.has_perm("view_user"),
                },
                {
                    "title": _("Groups"),
                    "link": "/"
                    + ("admin/" if module == "config.settings.development" else "oshimashakula/")
                    + "auth/group",
                    "permission": lambda request: request.user.is_superuser or request.user.has_perm("view_group"),
                },
                {
                    "title": _("Emails"),
                    "link": "/"
                    + ("admin/" if module == "config.settings.development" else "oshimashakula/")
                    + "account/emailaddress",
                    "permission": lambda request: request.user.is_superuser
                    or request.user.has_perm("view_emailaddress"),
                },
            ],
        },
        {
            "models": [
                "organisation.division",
                "organisation.position",
                "organisation.costcentre",
                "organisation.region",
                "organisation.location",
            ],
            "items": [
                {
                    "title": _("Divisions"),
                    "link": "/"
                    + ("admin/" if module == "config.settings.development" else "oshimashakula/")
                    + "organisation/division",
                    "permission": lambda request: request.user.is_superuser or request.user.has_perm("view_division"),
                },
                {
                    "title": _("Positions"),
                    "link": "/"
                    + ("admin/" if module == "config.settings.development" else "oshimashakula/")
                    + "organisation/position",
                    "permission": lambda request: request.user.is_superuser or request.user.has_perm("view_position"),
                },
                {
                    "title": _("Locations"),
                    "link": "/"
                    + ("admin/" if module == "config.settings.development" else "oshimashakula/")
                    + "organisation/location",
                    "permission": lambda request: request.user.is_superuser or request.user.has_perm("view_location"),
                },
                {
                    "title": _("Cost Centres"),
                    "link": "/"
                    + ("admin/" if module == "config.settings.development" else "oshimashakula/")
                    + "organisation/costcentre",
                    "permission": lambda request: request.user.is_superuser or request.user.has_perm("view_costcentre"),
                },
                {
                    "title": _("Regions"),
                    "link": "/"
                    + ("admin/" if module == "config.settings.development" else "oshimashakula/")
                    + "organisation/region",
                    "permission": lambda request: request.user.is_superuser or request.user.has_perm("view_region"),
                },
            ],
        },
        {
            "models": [
                "recruitment.vacancy",
                "recruitment.application",
                "recruitment.interview",
            ],
            "items": [
                {
                    "title": _("Applications"),
                    "link": "/"
                    + ("admin/" if module == "config.settings.development" else "oshimashakula/")
                    + "recruitment/application",
                    "permission": lambda request: request.user.is_superuser
                    or request.user.has_perm("view_application"),
                },
                {
                    "title": _("Vacancies"),
                    "link": "/"
                    + ("admin/" if module == "config.settings.development" else "oshimashakula/")
                    + "recruitment/vacancy",
                    "permission": lambda request: request.user.is_superuser or request.user.has_perm("view_vacancy"),
                },
                {
                    "title": _("Interviews"),
                    "link": "/"
                    + ("admin/" if module == "config.settings.development" else "oshimashakula/")
                    + "recruitment/interview",
                    "permission": lambda request: request.user.is_superuser or request.user.has_perm("view_interview"),
                },
            ],
        },
    ],
}
