import os
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).parent

DEBUG = os.environ.get("DEBUG", "") == "1"

SECRET_KEY = "secret"

# Dangerous: disable host header validation
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "todoapp",
    "django_htmx",
    "template_partials",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.csrf.CsrfViewMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "todoapp.urls"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR.parent / "workdir/db.sqlite3",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "example.context_processors.debug",
            ]
        },
    }
]

USE_TZ = True


STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
