from config.env import env

from .base import *

DEBUG = False

ADMINS = [
    ("Sakaria Ndadi", "oipapi.ndadi@gmail.com"),
]

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST", default="localhost"),
        "PORT": env("POSTGRES_PORT", default="5432"),
    },
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
# EMAIL_KEYFILE = env("EMAIL_KEYFILE")
# EMAIL_CERTFILE = env("EMAIL_CERTFILE")

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": env("REDIS_URL"),
    }
}


# CORS
CORS_ALLOW_ALL_ORIGINS = False
CORS_ORIGIN_WHITELIST = env.list("CORS_ORIGIN_WHITELIST", default=[])

# Security
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True
# X_FRAME_OPTIONS = "DENY"

CSRF_TRUSTED_ORIGINS = [
    "https://training.telecom.na",
    "https://www.training.telecom.na",
    "https://192.168.215.146",
    "https://197.188.250.244",
]
