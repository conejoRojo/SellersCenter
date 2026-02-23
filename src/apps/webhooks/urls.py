from django.urls import path
from .views import WebhookReceiverView

urlpatterns = [
    path("<str:channel_slug>/<str:event_type>/", WebhookReceiverView.as_view(), name="webhook-receiver"),
]
