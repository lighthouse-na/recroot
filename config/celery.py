import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
app = Celery("config")
app.config_from_object("config.settings.base", namespace="CELERY")
app.autodiscover_tasks()
