"""
    Django project settings.
    This module contains the base directory path and environment variable setup
    for the Django project.
"""

from pathlib import Path

import environ
import os

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
