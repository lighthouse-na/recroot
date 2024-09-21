from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "sakariandadi@gmail.com"
EMAIL_HOST_PASSWORD = "ahfw byeg zvzb qslq"
# EMAIL_KEYFILE = env("EMAIL_SSL_KEYFILE")
# EMAIL_CERTFILE = env("EMAIL_SSL_CERTFILE")


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
