from django.db import models
from apps.core.models import TimeStampedModel


class Shipment(TimeStampedModel):

    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        READY = "ready", "Listo para retirar"
        IN_TRANSIT = "in_transit", "En tránsito"
        OUT_FOR_DELIVERY = "out_for_delivery", "En camino"
        DELIVERED = "delivered", "Entregado"
        FAILED = "failed", "Entrega fallida"
        RETURNED = "returned", "Devuelto"

    class Provider(models.TextChoices):
        OCA = "oca", "OCA"
        ANDREANI = "andreani", "Andreani"
        DHL = "dhl", "DHL"
        CORREO_ARG = "correo_argentino", "Correo Argentino"
        CUSTOM = "custom", "Propio"

    order = models.OneToOneField(
        "orders.Order", on_delete=models.CASCADE, related_name="shipment"
    )
    provider = models.CharField(max_length=30, choices=Provider.choices)
    tracking_number = models.CharField(max_length=255, blank=True)
    tracking_url = models.URLField(blank=True)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PENDING)
    estimated_delivery = models.DateField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    # Historial de eventos del envío
    events = models.JSONField(default=list)
    raw_data = models.JSONField(default=dict)

    class Meta:
        verbose_name = "envío"
        verbose_name_plural = "envíos"

    def __str__(self):
        return f"Envío {self.provider} #{self.tracking_number} — {self.status}"
