from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
MIDDLEWARE.append("django_browser_reload.middleware.BrowserReloadMiddleware")
INSTALLED_APPS.append("debug_toolbar")
INSTALLED_APPS.append("django_browser_reload")
