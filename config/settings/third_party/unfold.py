from django.urls import reverse_lazy
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
                        "link": reverse_lazy("admin:index"),
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
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                    {
                        "title": _("Emails"),
                        "icon": "email",
                        "link": reverse_lazy("admin:account_emailaddress_changelist"),
                    },
                    {
                        "title": _("Groups"),
                        "icon": "groups",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
            {
                "title": _("Organisation"),
                # "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Region"),
                        "icon": "location_on",
                        "link": reverse_lazy("admin:organisation_region_changelist"),
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
                        "link": reverse_lazy(
                            "admin:recruitment_application_changelist"
                        ),
                    },
                    {
                        "title": _("Interviews"),
                        "icon": "event",
                        "link": reverse_lazy("admin:recruitment_interview_changelist"),
                    },
                    {
                        "title": _("Vacancies"),
                        "icon": "people",
                        "link": reverse_lazy("admin:recruitment_vacancy_changelist"),
                    },
                ],
            },
        ],
    },
}
