"""
    Django project settings.
    This module contains the base directory path and environment variable setup
    for the Django project.
"""

from pathlib import Path

import environ

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent
