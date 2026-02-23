"""
SellersCenter — Configuración de Production (AWS)
RDS, ElastiCache, S3, Secrets Manager.
"""

from .base import *  # noqa: F403
from decouple import config
import boto3
import json

DEBUG = False
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=lambda v: [s.strip() for s in v.split(",")])

# --- Secretos desde AWS Secrets Manager ---
def get_secret(secret_name: str) -> dict:
    client = boto3.client("secretsmanager", region_name=config("AWS_DEFAULT_REGION"))
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])

_db_secret = get_secret(config("DB_SECRET_NAME", default="sellerscenter/prod/db"))

# --- Base de datos RDS ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": _db_secret["dbname"],
        "USER": _db_secret["username"],
        "PASSWORD": _db_secret["password"],
        "HOST": _db_secret["host"],
        "PORT": _db_secret["port"],
        "CONN_MAX_AGE": 60,
        "OPTIONS": {"sslmode": "require"},
    }
}

# --- Celery con ElastiCache Redis ---
CELERY_BROKER_URL = config("REDIS_URL")  # redis://elasticache-endpoint:6379/0

# --- Cache con ElastiCache Redis ---
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"ssl": True},
        },
    }
}

# --- Archivos media en S3 ---
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_STORAGE_BUCKET_NAME = config("S3_MEDIA_BUCKET")
AWS_S3_REGION_NAME = config("AWS_DEFAULT_REGION")
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = "private"
AWS_QUERYSTRING_AUTH = True
MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/"

# --- Seguridad ---
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# --- Email via SES ---
EMAIL_BACKEND = "django_ses.SESBackend"
AWS_SES_REGION_NAME = config("AWS_DEFAULT_REGION")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="no-reply@sellerscenter.com")

# --- Logging a CloudWatch ---
LOGGING["handlers"]["cloudwatch"] = {  # noqa: F405
    "class": "watchtower.CloudWatchLogHandler",
    "log_group": "/sellerscenter/api",
    "stream_name": "django",
    "formatter": "json",
}
LOGGING["root"]["handlers"] = ["console", "cloudwatch"]  # noqa: F405
