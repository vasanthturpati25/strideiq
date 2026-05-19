"""
Django settings for StrideIQ
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ─────────────────────────────────────────────────────────────
# Load environment variables
# ─────────────────────────────────────────────────────────────

load_dotenv()

# ─────────────────────────────────────────────────────────────
# Base directory
# ─────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent.parent

# ─────────────────────────────────────────────────────────────
# Security
# ─────────────────────────────────────────────────────────────

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-change-me"
)

DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "127.0.0.1,localhost"
).split(",")

# ─────────────────────────────────────────────────────────────
# Installed apps
# ─────────────────────────────────────────────────────────────

INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party apps
    "rest_framework",
    "corsheaders",

    # Local apps
    "analysis",
]

# ─────────────────────────────────────────────────────────────
# Middleware
# ─────────────────────────────────────────────────────────────

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",

    "django.middleware.security.SecurityMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ─────────────────────────────────────────────────────────────
# URLs
# ─────────────────────────────────────────────────────────────

ROOT_URLCONF = "strideiq_project.urls"

# ─────────────────────────────────────────────────────────────
# Templates
# ─────────────────────────────────────────────────────────────

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

# ─────────────────────────────────────────────────────────────
# WSGI
# ─────────────────────────────────────────────────────────────

WSGI_APPLICATION = "strideiq_project.wsgi.application"

# ─────────────────────────────────────────────────────────────
# Database
# ─────────────────────────────────────────────────────────────

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ─────────────────────────────────────────────────────────────
# Password validation
# ─────────────────────────────────────────────────────────────

AUTH_PASSWORD_VALIDATORS = []

# ─────────────────────────────────────────────────────────────
# Internationalization
# ─────────────────────────────────────────────────────────────

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# ─────────────────────────────────────────────────────────────
# Static files
# ─────────────────────────────────────────────────────────────

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

# ─────────────────────────────────────────────────────────────
# Media files
# ─────────────────────────────────────────────────────────────

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"

# ─────────────────────────────────────────────────────────────
# Upload limits
# ─────────────────────────────────────────────────────────────

DATA_UPLOAD_MAX_MEMORY_SIZE = 100 * 1024 * 1024

FILE_UPLOAD_MAX_MEMORY_SIZE = 100 * 1024 * 1024

# ─────────────────────────────────────────────────────────────
# Django REST Framework
# ─────────────────────────────────────────────────────────────

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],

    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FormParser",
    ],

    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],

    "DEFAULT_AUTHENTICATION_CLASSES": [],

    "UNAUTHENTICATED_USER": None,
}

# ─────────────────────────────────────────────────────────────
# CORS
# ─────────────────────────────────────────────────────────────

CORS_ALLOW_ALL_ORIGINS = True

# ─────────────────────────────────────────────────────────────
# AWS S3
# ─────────────────────────────────────────────────────────────

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")

AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "")

# ─────────────────────────────────────────────────────────────
# Default primary key field type
# ─────────────────────────────────────────────────────────────

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"