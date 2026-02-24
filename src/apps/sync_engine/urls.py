from django.urls import path
from .views import IngestionWebhookView

app_name = "sync_engine"

urlpatterns = [
    path("webhook/", IngestionWebhookView.as_view(), name="ingestion-webhook"),
]
