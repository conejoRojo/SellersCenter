import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('sellerscenter')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Example: Task with Idempotency considered
@app.task(bind=True, max_retries=3, acks_late=True)
def sync_channel_product(self, product_id, channel_id):
    # acks_late=True combined with SQS DLQ ensures poison messages are handled safely
    pass
