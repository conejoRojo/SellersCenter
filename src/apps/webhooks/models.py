from django.db import models
from apps.core.models import TimeStampedModel


class WebhookEvent(TimeStampedModel):
    """
    Log de todos los webhooks recibidos. Permite auditoría y reintentos.
    """

    class EventType(models.TextChoices):
        ORDER = "order", "Pedido"
        PAYMENT = "payment", "Pago"
        SHIPMENT = "shipment", "Envío"
        CATALOG = "catalog", "Catálogo"
        OTHER = "other", "Otro"

    class Status(models.TextChoices):
        RECEIVED = "received", "Recibido"
        QUEUED = "queued", "En cola"
        PROCESSING = "processing", "Procesando"
        PROCESSED = "processed", "Procesado"
        FAILED = "failed", "Fallido"

    channel = models.ForeignKey(
        "channels.Channel", on_delete=models.SET_NULL, null=True, blank=True
    )
    event_type = models.CharField(max_length=20, choices=EventType.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.RECEIVED)
    payload = models.JSONField(default=dict)
    headers = models.JSONField(default=dict)
    error_message = models.TextField(blank=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    retries = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "evento webhook"
        verbose_name_plural = "eventos webhook"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Webhook {self.event_type} — {self.status} — {self.created_at:%Y-%m-%d %H:%M}"
