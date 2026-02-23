"""
SellersCenter — Configuración de Development
SQLite/PostgreSQL local, DEBUG=True, sin S3.
"""

from .base import *
from decouple import config

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

# --- Base de datos local ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME", default="sellerscenter"),
        "USER": config("DB_USER", default="sc_user"),
        "PASSWORD": config("DB_PASSWORD", default="sc_password"),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5433"),
        "OPTIONS": {
            "options": "-c search_path=public",
        },
    }
}

# --- AWS LocalStack y Simulaciones ---
AWS_ACCESS_KEY_ID = "test"
AWS_SECRET_ACCESS_KEY = "test"
AWS_DEFAULT_REGION = "us-east-1"
AWS_ENDPOINT_URL = "http://localhost:4566"

# --- Celery con SQS broker (LocalStack) ---
CELERY_BROKER_URL = f"sqs://test:test@localhost:4566"
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'region': AWS_DEFAULT_REGION,
    'is_secure': False,
}

# --- Cache con Redis local (Puerto modificado) ---
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config("REDIS_URL", default="redis://localhost:6380/1"),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

# --- En dev, los archivos media son locales ---
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

# --- Email en consola durante desarrollo ---
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# --- Debug toolbar (opcional) ---
# INSTALLED_APPS += ["debug_toolbar"]
