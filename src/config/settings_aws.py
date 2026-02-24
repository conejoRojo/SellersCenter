
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-do-not-use-in-prod')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']

# CELERY & AWS LOCALSTACK SETTINGS
AWS_ACCESS_KEY_ID = 'test'
AWS_SECRET_ACCESS_KEY = 'test'
AWS_DEFAULT_REGION = 'us-east-1'
AWS_ENDPOINT_URL = os.environ.get('AWS_ENDPOINT_URL', 'http://localstack:4566') # Points to Localstack in docker

# Celery SQS Broker via LocalStack
CELERY_BROKER_URL = f"sqs://test:test@{AWS_ENDPOINT_URL.replace('http://', '')}"
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'region': AWS_DEFAULT_REGION,
    'is_secure': False,
}
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'

# DATABASES
# Utilizing PgBouncer connection port in production/docker
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'sellerscenter'),
        'USER': os.environ.get('POSTGRES_USER', 'sc_user'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'sc_password'),
        'HOST': os.environ.get('POSTGRES_HOST', 'db'), # Point to PgBouncer if used
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        'CONN_MAX_AGE': 60, # Manage connections carefully
    }
}
