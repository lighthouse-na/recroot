import os

from config.env import BASE_DIR, env

ADMINS = [("Sakaria Ndadi", "sakariandadi@gmail.com")]

env.read_env(os.path.join(BASE_DIR, ".env"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")


# Application definition
LOCAL_APPS = [
    "apps.accounts",
    "apps.organisation",
    "apps.recruitment",
    "apps.pages",
    "apps.dashboard",
    "apps.utils",
]
THIRD_PARTY_APPS = [
    "django_extensions",
    "phonenumber_field",
    "crispy_forms",
    "crispy_tailwind",
    "tinymce",
    "widget_tweaks",
    "debug_toolbar",
    "import_export",
    "django_cleanup.apps.CleanupConfig",
    "rest_framework",
    "django_recaptcha",
    "django_cotton",
    "django_cotton_components",
    "django_browser_reload",
]
INSTALLED_APPS = (
    [
        "unfold",
        "unfold.contrib.import_export",
        "unfold.contrib.filters",
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "whitenoise.runserver_nostatic",
        "django.contrib.staticfiles",
        "django.contrib.sites",
        "django.contrib.humanize",
        "allauth",
        "allauth.account",
    ]
    + LOCAL_APPS
    + THIRD_PARTY_APPS
)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # whitenoise
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "apps.recruitment.middleware.InternalAccessMiddleware",  # recruitment middleware
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",  # allauth
    "debug_toolbar.middleware.DebugToolbarMiddleware",  # debug toolbar
    "django_browser_reload.middleware.BrowserReloadMiddleware",  # browser reload
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
# ASGI_APPLICATION = "config.asgi.application"


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-uk"

TIME_ZONE = "Africa/Windhoek"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

INTERNAL_IPS = [
    "127.0.0.1",
]

SITE_ID = 1

X_FRAME_OPTIONS = "SAMEORIGIN"

UBLOCK_ORIGIN_EXCEPTIONS = [
    "http://localhost:8000/*",
    # Add your domain here
]

AUTH_USER_MODEL = "accounts.User"
CELERY_BROKER_URL = env("BROKER_URL")

INTRANET_IP_RANGES = env.list("INTRANET_IP_RANGES", default=["127.0."])


from .third_party.allauth import *
from .third_party.channels import *
from .third_party.crispy_forms import *
from .third_party.drf import *
from .third_party.recaptcha import *
from .third_party.tinymce import *
from .third_party.unfold import *
