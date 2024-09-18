from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _

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
                        "link": "/admin/",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Auth"),
                        "icon": "people",
                        "link": "/admin/auth/user",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Organisation"),
                        "icon": "home",
                        "link": "/admin/organisation",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Recruitment"),
                        "icon": "people",
                        "link": "/admin/recruitment",
                        "permission": lambda request: request.user.has_perm(
                            "view_application"
                        ),
                    },
                    {
                        "title": _("Financial Aid"),
                        "icon": "request_quote",
                        "link": "/admin/finaid/",
                        "permission": lambda request: request.user.has_perm(
                            "view_application"
                        ),
                    },
                    # -----------------------------------------------------------------------
                    # Admin Dashboard Urls
                    # -----------------------------------------------------------------------
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": "/dashboard/admin/",
                        "permission": lambda request: request.user.groups.filter(
                            name="admin"
                        ).exists()
                        and request.path.startswith("/dashboard/admin/"),
                    },
                    {
                        "title": _("Auth"),
                        "icon": "people",
                        "link": "/dashboard/admin/auth/",
                        "permission": lambda request: request.user.groups.filter(
                            name="admin"
                        ).exists()
                        and request.path.startswith("/dashboard/admin/"),
                    },
                    {
                        "title": _("Organisation"),
                        "icon": "home",
                        "link": "/dashboard/admin/organisation",
                        "permission": lambda request: request.user.groups.filter(
                            name="admin"
                        ).exists()
                        and request.path.startswith("/dashboard/admin/"),
                    },
                    {
                        "title": _("Recruitment"),
                        "icon": "people",
                        "link": "/dashboard/admin/recruitment",
                        "permission": lambda request: request.user.groups.filter(
                            name="admin"
                        ).exists()
                        and request.path.startswith("/dashboard/admin/"),
                    },
                    {
                        "title": _("Financial Aid"),
                        "icon": "request_quote",
                        "link": "/dashboard/admin/finaid/",
                        "permission": lambda request: request.user.groups.filter(
                            name="admin"
                        ).exists()
                        and request.path.startswith("/dashboard/admin/"),
                    },
                    # -----------------------------------------------------------------------
                    # Staff Dashboard Urls
                    # -----------------------------------------------------------------------
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("Staff:index"),
                        "permission": lambda request: request.path.startswith(
                            "/dashboard/staff/"
                        ),
                        "permission": lambda request: request.user.groups.filter(
                            name="staff"
                        ).exists()
                        and request.path.startswith("/dashboard/staff/"),
                    },
                    {
                        "title": _("Qualifications"),
                        "icon": "clinical_notes",
                        "link": "/dashboard/staff/accounts",
                        "permission": lambda request: request.user.groups.filter(
                            name="staff"
                        ).exists()
                        and request.path.startswith("/dashboard/staff/"),
                    },
                    {
                        "title": _("Recruitment"),
                        "icon": "people",
                        "link": "/dashboard/staff/recruitment",
                        "permission": lambda request: request.user.groups.filter(
                            name="staff"
                        ).exists()
                        and request.path.startswith("/dashboard/staff/"),
                    },
                    {
                        "title": _("Financial Aid"),
                        "icon": "request_quote",
                        "link": "/dashboard/staff/finaid/financialassistanceapplication/",
                        "permission": lambda request: request.user.groups.filter(
                            name="staff"
                        ).exists()
                        and request.path.startswith("/dashboard/staff/"),
                    },
                ],
            },
            # {
            #     "title": _("Authentication"),
            #     "separator": True,
            #     "collapsible": True,
            #     "permission": lambda request: request.user.is_superuser,
            #     "items": [
            #         {
            #             "title": _("Users"),
            #             "icon": "people",
            #             # "link": reverse_lazy("admin:auth_user_changelist"),
            #             "link": "/admin/auth/user/",
            #             "permission": lambda request: request.user.has_perm(
            #                 "auth.view_user"
            #             ),
            #         },
            #         {
            #             "title": _("Emails"),
            #             "icon": "email",
            #             # "link": reverse_lazy("admin:account_emailaddress_changelist"),
            #             "link": "/admin/account/emailaddress",
            #             "permission": lambda request: request.user.has_perm(
            #                 "account.view_emailaddress"
            #             ),
            #         },
            #         {
            #             "title": _("Groups"),
            #             "icon": "groups",
            #             # "link": reverse_lazy("admin:auth_group_changelist"),
            #             "link": "/admin/auth/group/",
            #             "permission": lambda request: request.user.has_perm(
            #                 "auth.view_group"
            #             ),
            #         },
            #     ],
            # },
            # {
            #     "title": _("Organisation"),
            #     # "separator": True,
            #     "collapsible": True,
            #     "items": [
            #         {
            #             "title": _("Regions"),
            #             "icon": "location_on",
            #             # "link": reverse_lazy("admin:organisation_region_changelist"),
            #             "link": "/admin/organisation/region",
            #             "permission": lambda request: request.user.has_perm(
            #                 "view_region"
            #             ),
            #         },
            #         # {
            #         #     "title": _("Divisions"),
            #         #     "icon": "location_on",
            #         #     # "link": reverse_lazy("admin:organisation_division_changelist"),
            #         #     "link": "/admin/organisation/division",
            #         #     "permission": lambda request: request.user.has_perm(
            #         #         "view_region"
            #         #     ),
            #         # },
            #         {
            #             "title": _("Positions"),
            #             "icon": "location_on",
            #             # "link": reverse_lazy("admin:organisation_position_changelist"),
            #             "link": "/admin/organisation/position",
            #             "permission": lambda request: request.user.has_perm(
            #                 "view_position"
            #             ),
            #         },
            #     ],
            # },
            # {
            #     "title": _("Recruitment"),
            #     # "separator": True,
            #     "collapsible": True,
            #     "items": [
            #         {
            #             "title": _("Applications"),
            #             "icon": "stacks",
            #             # "link": reverse_lazy(
            #             #     "admin:recruitment_application_changelist"
            #             # ),
            #             "link": "/admin/recruitment/application",
            #             "permission": lambda request: request.user.has_perm(
            #                 "view_application"
            #             ),
            #         },
            #         {
            #             "title": _("Interviews"),
            #             "icon": "event",
            #             # "link": reverse_lazy("admin:recruitment_interview_changelist"),
            #             "link": "/admin/recruitment/interview",
            #             "permission": lambda request: request.user.has_perm(
            #                 "view_interview"
            #             ),
            #         },
            #         {
            #             "title": _("Vacancies"),
            #             "icon": "people",
            #             # "link": reverse_lazy("admin:recruitment_vacancy_changelist"),
            #             "link": "/admin/recruitment/vacancy",
            #             "permission": lambda request: request.user.has_perm(
            #                 "view_vacancy"
            #             ),
            #         },
            #     ],
            # },
            # {
            #     "title": _("Financial Aid"),
            #     # "separator": True,
            #     "collapsible": True,
            #     "items": [
            #         # {
            #         #     "title": _("Financial Assistance Adverts"),
            #         #     "icon": "people",
            #         #     # "link": reverse_lazy(
            #         #     #     "admin:finaid_financialassistanceadvert_changelist"
            #         #     # ),
            #         #     "link": "/admin/finaid/financialassistanceadvert",
            #         #     "permission": lambda request: request.user.has_perm(
            #         #         "view_financialassistanceadvert"
            #         #     ),
            #         # },
            #         {
            #             "title": _("Financial Assistance Applications"),
            #             "icon": "request_quote",
            #             # "link": reverse_lazy(
            #             #     "admin:finaid_financialassistanceapplication_changelist"
            #             # ),
            #             "link": "/admin/finaid/financialassistanceapplication",
            #             "permission": lambda request: request.user.has_perm(
            #                 "view_financialassistanceapplication"
            #             ),
            #         },
            #         {
            #             "title": _("Bursary Adverts"),
            #             "icon": "people",
            #             # "link": reverse_lazy("admin:finaid_bursaryadvert_changelist"),
            #             "link": "/admin/finaid/bursaryadvert",
            #             "permission": lambda request: request.user.has_perm(
            #                 "view_bursaryadvert"
            #             ),
            #         },
            #         {
            #             "title": _("Bursary Applications"),
            #             "icon": "request_quote",
            #             # "link": reverse_lazy(
            #             #     "admin:finaid_bursaryapplication_changelist"
            #             # ),
            #             "link": "/admin/finaid/bursaryapplication",
            #             "permission": lambda request: request.user.has_perm(
            #                 "view_bursaryapplication"
            #             ),
            #         },
            #     ],
            # },
        ],
    },
    "TABS": [
        {
            "models": [
                "auth.user",
                "auth.group",
                "account.emailaddress",
            ],
            "items": [
                {
                    "title": _("Users"),
                    # "link": reverse_lazy("admin:auth_user_changelist"),
                    "link": "/admin/auth/user/",
                    "permission": lambda request: request.user.is_superuser
                    or request.user.has_perm("view_user"),
                },
                {
                    "title": _("Groups"),
                    # "link": reverse_lazy("admin:auth_group_changelist"),
                    "link": "/admin/auth/group/",
                    "permission": lambda request: request.user.is_superuser
                    or request.user.has_perm("view_group"),
                },
                {
                    "title": _("Emails"),
                    # "link": reverse_lazy("admin:auth_group_changelist"),
                    "link": "/admin/account/emailaddress/",
                    "permission": lambda request: request.user.is_superuser
                    or request.user.has_perm("view_emailaddress"),
                },
            ],
        },
        {
            "models": [
                "organisation.position",
                "organisation.costcentre",
                "organisation.region",
                "organisation.location",
            ],
            "items": [
                {
                    "title": _("Positions"),
                    "link": "/admin/organisation/position/",
                    "permission": lambda request: request.user.is_superuser
                    or request.user.has_perm("view_position"),
                },
                {
                    "title": _("Locations"),
                    "link": "/admin/organisation/location/",
                    "permission": lambda request: request.user.is_superuser
                    or request.user.has_perm("view_location"),
                },
                {
                    "title": _("Cost Centres"),
                    "link": "/admin/organisation/costcentre/",
                    "permission": lambda request: request.user.is_superuser
                    or request.user.has_perm("view_costcentre"),
                },
                {
                    "title": _("Regions"),
                    "link": "/admin/organisation/region/",
                    "permission": lambda request: request.user.is_superuser
                    or request.user.has_perm("view_region"),
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
                    "link": "/admin/recruitment/application/",
                    "permission": lambda request: request.user.is_superuser
                    or request.user.has_perm("view_application"),
                },
                {
                    "title": _("Vacancies"),
                    "link": "/admin/recruitment/vacancy/",
                    "permission": lambda request: request.user.is_superuser
                    or request.user.has_perm("view_vacancy"),
                },
                {
                    "title": _("Interviews"),
                    "link": "/admin/recruitment/interview/",
                    "permission": lambda request: request.user.is_superuser
                    or request.user.has_perm("view_interview"),
                },
            ],
        },
    ],
}
