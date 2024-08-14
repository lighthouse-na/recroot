from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "SITE_TITLE": "<Your Title>",
    "SITE_HEADER": "<Your Title>",
    "SITE_SYMBOL": "speed",  # symbol from icon set
    "SHOW_HISTORY": True,  # show/hide "History" button, default: True
    "SHOW_VIEW_ON_SITE": True,  # show/hide "View on site" button, default: True
    "COLORS": {
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
            "950": "59 7 100",
        },
    },
    # "EXTENSIONS": {
    #     "modeltranslation": {
    #         "flags": {
    #             "en": "🇬🇧",
    #             "fr": "🇫🇷",
    #             "nl": "🇧🇪",
    #         },
    #     },
    # },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                # "title": _("Navigation"),
                # "separator": True,  # Top border
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        # "link": reverse_lazy("admin:index"),
                        "link": "/admin/",
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "title": _("Authentication"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "people",
                        # "link": reverse_lazy("admin:auth_user_changelist"),
                        "link": "/admin/auth/user/",
                        "permission": lambda request: request.user.has_perm(
                            "auth.view_user"
                        ),
                    },
                    {
                        "title": _("Emails"),
                        "icon": "email",
                        # "link": reverse_lazy("admin:account_emailaddress_changelist"),
                        "link": "/admin/account/emailaddress",
                        "permission": lambda request: request.user.has_perm(
                            "account.view_emailaddress"
                        ),
                    },
                    {
                        "title": _("Groups"),
                        "icon": "groups",
                        # "link": reverse_lazy("admin:auth_group_changelist"),
                        "link": "/admin/auth/group/",
                        "permission": lambda request: request.user.has_perm(
                            "auth.view_group"
                        ),
                    },
                ],
            },
            {
                "title": _("Organisation"),
                # "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Regions"),
                        "icon": "location_on",
                        # "link": reverse_lazy("admin:organisation_region_changelist"),
                        "link": "/admin/organisation/region",
                        "permission": lambda request: request.user.has_perm(
                            "view_region"
                        ),
                    },
                    # {
                    #     "title": _("Divisions"),
                    #     "icon": "location_on",
                    #     # "link": reverse_lazy("admin:organisation_division_changelist"),
                    #     "link": "/admin/organisation/division",
                    #     "permission": lambda request: request.user.has_perm(
                    #         "view_region"
                    #     ),
                    # },
                    {
                        "title": _("Positions"),
                        "icon": "location_on",
                        # "link": reverse_lazy("admin:organisation_position_changelist"),
                        "link": "/admin/organisation/position",
                        "permission": lambda request: request.user.has_perm(
                            "view_position"
                        ),
                    },
                ],
            },
            {
                "title": _("Recruitment"),
                # "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Applications"),
                        "icon": "stacks",
                        # "link": reverse_lazy(
                        #     "admin:recruitment_application_changelist"
                        # ),
                        "link": "/admin/recruitment/application",
                        "permission": lambda request: request.user.has_perm(
                            "view_application"
                        ),
                    },
                    {
                        "title": _("Interviews"),
                        "icon": "event",
                        # "link": reverse_lazy("admin:recruitment_interview_changelist"),
                        "link": "/admin/recruitment/interview",
                        "permission": lambda request: request.user.has_perm(
                            "view_interview"
                        ),
                    },
                    {
                        "title": _("Vacancies"),
                        "icon": "people",
                        # "link": reverse_lazy("admin:recruitment_vacancy_changelist"),
                        "link": "/admin/recruitment/vacancy",
                        "permission": lambda request: request.user.has_perm(
                            "view_vacancy"
                        ),
                    },
                ],
            },
            {
                "title": _("Financial Aid"),
                # "separator": True,
                "collapsible": True,
                "items": [
                    # {
                    #     "title": _("Financial Assistance Adverts"),
                    #     "icon": "people",
                    #     # "link": reverse_lazy(
                    #     #     "admin:finaid_financialassistanceadvert_changelist"
                    #     # ),
                    #     "link": "/admin/finaid/financialassistanceadvert",
                    #     "permission": lambda request: request.user.has_perm(
                    #         "view_financialassistanceadvert"
                    #     ),
                    # },
                    {
                        "title": _("Financial Assistance Applications"),
                        "icon": "request_quote",
                        # "link": reverse_lazy(
                        #     "admin:finaid_financialassistanceapplication_changelist"
                        # ),
                        "link": "/admin/finaid/financialassistanceapplication",
                        "permission": lambda request: request.user.has_perm(
                            "view_financialassistanceapplication"
                        ),
                    },
                    {
                        "title": _("Bursary Adverts"),
                        "icon": "people",
                        # "link": reverse_lazy("admin:finaid_bursaryadvert_changelist"),
                        "link": "/admin/finaid/bursaryadvert",
                        "permission": lambda request: request.user.has_perm(
                            "view_bursaryadvert"
                        ),
                    },
                    {
                        "title": _("Bursary Applications"),
                        "icon": "request_quote",
                        # "link": reverse_lazy(
                        #     "admin:finaid_bursaryapplication_changelist"
                        # ),
                        "link": "/admin/finaid/bursaryapplication",
                        "permission": lambda request: request.user.has_perm(
                            "view_bursaryapplication"
                        ),
                    },
                ],
            },
        ],
    },
}
