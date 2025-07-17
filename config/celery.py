import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
<<<<<<< HEAD
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
=======
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
>>>>>>> upstream/main

# Create a Celery instance
app = Celery("config")

# Using configuration from the base settings (CELERY_ prefix)
app.config_from_object("config.settings.base", namespace="CELERY")

# Automatically discover tasks in each app's 'tasks.py' file
app.autodiscover_tasks()
<<<<<<< HEAD
=======
app.conf.broker_connection_retry_on_startup = True
>>>>>>> upstream/main
