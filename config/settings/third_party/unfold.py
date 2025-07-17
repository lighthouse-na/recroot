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
                        ),
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
                        + "organisation",
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
                        + "recruitment",
                        "permission": lambda request: request.user.groups.filter(name="admin").exists()
                        and request.path.startswith("/dashboard/admin/"),
                    },
                    {
                        "title": _("Pages"),
                        "icon": "note",
                        "link": "/"
                        + (
                            "dashboard/admin/"
                            if module == "config.settings.development"
                            else "dashboard/telecom/administrator/"
                        )
                        + "pages/announcement/",
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
<<<<<<< HEAD
                    "permission": lambda request: request.user.is_superuser or request.user.has_perm("view_user"),
=======
                    "permission": lambda request: request.user.is_superuser,
>>>>>>> upstream/main
                },
                {
                    "title": _("Groups"),
                    "link": "/"
                    + ("admin/" if module == "config.settings.development" else "oshimashakula/")
                    + "auth/group",
<<<<<<< HEAD
                    "permission": lambda request: request.user.is_superuser or request.user.has_perm("view_group"),
=======
                    "permission": lambda request: request.user.is_superuser,
>>>>>>> upstream/main
                },
                {
                    "title": _("Emails"),
                    "link": "/"
                    + ("admin/" if module == "config.settings.development" else "oshimashakula/")
                    + "account/emailaddress",
<<<<<<< HEAD
                    "permission": lambda request: request.user.is_superuser
                    or request.user.has_perm("view_emailaddress"),
=======
                    "permission": lambda request: request.user.is_superuser,
>>>>>>> upstream/main
                },
                {
                    "title": _("Users"),
                    "link": "/"
                    + (
                        "dashboard/admin/"
                        if module == "config.settings.development"
                        else "dashboard/telecom/administrator/"
                    )
                    + "accounts/user",
<<<<<<< HEAD
                    "permission": lambda request: request.user.groups.filter(name="admin").exists()
                    or request.user.has_perm("view_user"),
=======
                    "permission": lambda request: request.user.groups.filter(name="admin").exists(),
>>>>>>> upstream/main
                },
                {
                    "title": _("Groups"),
                    "link": "/"
                    + (
                        "dashboard/admin/"
                        if module == "config.settings.development"
                        else "dashboard/telecom/administrator/"
                    )
                    + "auth/group",
<<<<<<< HEAD
                    "permission": lambda request: request.user.groups.filter(name="admin").exists()
                    or request.user.has_perm("view_group"),
=======
                    "permission": lambda request: request.user.groups.filter(name="admin").exists(),
>>>>>>> upstream/main
                },
                {
                    "title": _("Emails"),
                    "link": "/"
                    + (
                        "dashboard/admin/"
                        if module == "config.settings.development"
                        else "dashboard/telecom/administrator/"
                    )
                    + "account/emailaddress",
<<<<<<< HEAD
                    "permission": lambda request: request.user.groups.filter(name="admin").exists()
                    or request.user.has_perm("view_emailaddress"),
=======
                    "permission": lambda request: request.user.groups.filter(name="admin").exists(),
>>>>>>> upstream/main
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
<<<<<<< HEAD
                    "permission": lambda request: request.user.is_superuser or request.user.has_perm("view_division"),
=======
                    "permission": lambda request: request.user.is_superuser,
>>>>>>> upstream/main
                },
                {
                    "title": _("Positions"),
                    "link": "/"
                    + ("admin/" if module == "config.settings.development" else "oshimashakula/")
                    + "organisation/position",
<<<<<<< HEAD
                    "permission": lambda request: request.user.is_superuser or request.user.has_perm("view_position"),
=======
                    "permission": lambda request: request.user.is_superuser,
>>>>>>> upstream/main
                },
                {
                    "title": _("Locations"),
                    "link": "/"
                    + ("admin/" if module == "config.settings.development" else "oshimashakula/")
                    + "organisation/location",
<<<<<<< HEAD
                    "permission": lambda request: request.user.is_superuser or request.user.has_perm("view_location"),
=======
                    "permission": lambda request: request.user.is_superuser,
>>>>>>> upstream/main
                },
                {
                    "title": _("Cost Centres"),
                    "link": "/"
                    + ("admin/" if module == "config.settings.development" else "oshimashakula/")
                    + "organisation/costcentre",
<<<<<<< HEAD
                    "permission": lambda request: request.user.is_superuser or request.user.has_perm("view_costcentre"),
=======
                    "permission": lambda request: request.user.is_superuser,
>>>>>>> upstream/main
                },
                {
                    "title": _("Regions"),
                    "link": "/"
                    + ("admin/" if module == "config.settings.development" else "oshimashakula/")
                    + "organisation/region",
<<<<<<< HEAD
                    "permission": lambda request: request.user.is_superuser or request.user.has_perm("view_region"),
=======
                    "permission": lambda request: request.user.is_superuser,
>>>>>>> upstream/main
                },
                {
                    "title": _("Divisions"),
                    "link": "/"
                    + (
                        "dashboard/admin/"
                        if module == "config.settings.development"
                        else "dashboard/telecom/administrator/"
                    )
                    + "organisation/division",
<<<<<<< HEAD
                    "permission": lambda request: request.user.groups.filter(name="admin").exists()
                    or request.user.has_perm("view_division"),
=======
                    "permission": lambda request: request.user.groups.filter(name="admin").exists(),
>>>>>>> upstream/main
                },
                {
                    "title": _("Positions"),
                    "link": "/"
                    + (
                        "dashboard/admin/"
                        if module == "config.settings.development"
                        else "dashboard/telecom/administrator/"
                    )
                    + "organisation/position",
<<<<<<< HEAD
                    "permission": lambda request: request.user.groups.filter(name="admin").exists()
                    or request.user.has_perm("view_position"),
=======
                    "permission": lambda request: request.user.groups.filter(name="admin").exists(),
>>>>>>> upstream/main
                },
                {
                    "title": _("Locations"),
                    "link": "/"
                    + (
                        "dashboard/admin/"
                        if module == "config.settings.development"
                        else "dashboard/telecom/administrator/"
                    )
                    + "organisation/location",
<<<<<<< HEAD
                    "permission": lambda request: request.user.groups.filter(name="admin").exists()
                    or request.user.has_perm("view_location"),
=======
                    "permission": lambda request: request.user.groups.filter(name="admin").exists(),
>>>>>>> upstream/main
                },
                {
                    "title": _("Cost Centres"),
                    "link": "/"
                    + (
                        "dashboard/admin/"
                        if module == "config.settings.development"
                        else "dashboard/telecom/administrator/"
                    )
                    + "organisation/costcentre",
<<<<<<< HEAD
                    "permission": lambda request: request.user.groups.filter(name="admin").exists()
                    or request.user.has_perm("view_costcentre"),
=======
                    "permission": lambda request: request.user.groups.filter(name="admin").exists(),
>>>>>>> upstream/main
                },
                {
                    "title": _("Regions"),
                    "link": "/"
                    + (
                        "dashboard/admin/"
                        if module == "config.settings.development"
                        else "dashboard/telecom/administrator/"
                    )
                    + "organisation/region",
<<<<<<< HEAD
                    "permission": lambda request: request.user.is_superuser or request.user.has_perm("view_region"),
=======
                    "permission": lambda request: request.user.is_superuser,
>>>>>>> upstream/main
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
<<<<<<< HEAD
                    "permission": lambda request: request.user.is_superuser
                    or request.user.has_perm("view_application"),
=======
                    "permission": lambda request: request.user.is_superuser,
>>>>>>> upstream/main
                },
                {
                    "title": _("Vacancies"),
                    "link": "/"
                    + ("admin/" if module == "config.settings.development" else "oshimashakula/")
                    + "recruitment/vacancy",
<<<<<<< HEAD
                    "permission": lambda request: request.user.is_superuser or request.user.has_perm("view_vacancy"),
=======
                    "permission": lambda request: request.user.is_superuser,
>>>>>>> upstream/main
                },
                {
                    "title": _("Interviews"),
                    "link": "/"
                    + ("admin/" if module == "config.settings.development" else "oshimashakula/")
                    + "recruitment/interview",
<<<<<<< HEAD
                    "permission": lambda request: request.user.is_superuser or request.user.has_perm("view_interview"),
=======
                    "permission": lambda request: request.user.is_superuser,
>>>>>>> upstream/main
                },
                {
                    "title": _("Applications"),
                    "link": "/"
                    + (
                        "dashboard/admin/"
                        if module == "config.settings.development"
                        else "dashboard/telecom/administrator/"
                    )
                    + "recruitment/application",
<<<<<<< HEAD
                    "permission": lambda request: request.user.groups.filter(name="admin").exists()
                    or request.user.has_perm("view_application"),
=======
                    "permission": lambda request: request.user.groups.filter(name="admin").exists(),
>>>>>>> upstream/main
                },
                {
                    "title": _("Vacancies"),
                    "link": "/"
                    + (
                        "dashboard/admin/"
                        if module == "config.settings.development"
                        else "dashboard/telecom/administrator/"
                    )
                    + "recruitment/vacancy",
<<<<<<< HEAD
                    "permission": lambda request: request.user.groups.filter(name="admin").exists()
                    or request.user.has_perm("view_vacancy"),
=======
                    "permission": lambda request: request.user.groups.filter(name="admin").exists(),
>>>>>>> upstream/main
                },
                {
                    "title": _("Interviews"),
                    "link": "/"
                    + (
                        "dashboard/admin/"
                        if module == "config.settings.development"
                        else "dashboard/telecom/administrator/"
                    )
                    + "recruitment/interview",
<<<<<<< HEAD
                    "permission": lambda request: request.user.groups.filter(name="admin").exists()
                    or request.user.has_perm("view_interview"),
=======
                    "permission": lambda request: request.user.groups.filter(name="admin").exists(),
>>>>>>> upstream/main
                },
            ],
        },
        {
            "models": [
                "pages.announcement",
                "pages.faq",
            ],
            "items": [
                {
                    "title": _("Announcements"),
                    "link": "/"
                    + ("admin/" if module == "config.settings.development" else "oshimashakula/")
                    + "pages/announcement",
<<<<<<< HEAD
                    "permission": lambda request: request.user.is_superuser
                    or request.user.has_perm("view_announcement"),
=======
                    "permission": lambda request: request.user.is_superuser,
>>>>>>> upstream/main
                },
                {
                    "title": _("FAQs"),
                    "link": "/"
                    + ("admin/" if module == "config.settings.development" else "oshimashakula/")
                    + "pages/faq",
<<<<<<< HEAD
                    "permission": lambda request: request.user.is_superuser or request.user.has_perm("view_faq"),
=======
                    "permission": lambda request: request.user.is_superuser,
>>>>>>> upstream/main
                },
                {
                    "title": _("Announcements"),
                    "link": "/"
                    + (
                        "dashboard/admin/"
                        if module == "config.settings.development"
                        else "dashboard/telecom/administrator/"
                    )
                    + "pages/announcement",
<<<<<<< HEAD
                    "permission": lambda request: request.user.groups.filter(name="admin").exists()
                    or request.user.has_perm("view_announcement"),
=======
                    "permission": lambda request: request.user.groups.filter(name="admin").exists(),
>>>>>>> upstream/main
                },
                {
                    "title": _("FAQs"),
                    "link": "/"
                    + (
                        "dashboard/admin/"
                        if module == "config.settings.development"
                        else "dashboard/telecom/administrator/"
                    )
                    + "pages/faq",
<<<<<<< HEAD
                    "permission": lambda request: request.user.groups.filter(name="admin").exists()
                    or request.user.has_perm("view_faq"),
=======
                    "permission": lambda request: request.user.groups.filter(name="admin").exists(),
>>>>>>> upstream/main
                },
            ],
        },
    ],
}
