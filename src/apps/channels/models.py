"""
Channels — Marketplaces y canales de venta integrados al SC.
Cada canal tiene su adaptador propio en channels/adapters/
"""

from django.db import models
from apps.core.models import TimeStampedModel


class Channel(TimeStampedModel):
    """
    Representa un marketplace o canal de venta (MeLi, Amazon, Shopify, etc.)
    """

    class ChannelType(models.TextChoices):
        MARKETPLACE = "marketplace", "Marketplace"
        ECOMMERCE = "ecommerce", "E-Commerce propio"
        B2B = "b2b", "B2B / Mayorista"

    slug = models.SlugField(unique=True, help_text="Ej: mercadolibre, amazon, shopify")
    name = models.CharField(max_length=255)
    channel_type = models.CharField(max_length=20, choices=ChannelType.choices)
    is_active = models.BooleanField(default=True)
    logo_url = models.URLField(blank=True)
    # Configuración específica del canal (URLs base de API, versión, etc.)
    config = models.JSONField(default=dict)

    def __str__(self):
        return self.name

    def get_adapter(self):
        """Factory que devuelve el adaptador correcto para este canal."""
        from .adapters import get_adapter
        return get_adapter(self.slug)


class SellerChannelCredential(TimeStampedModel):
    """
    Credenciales de un seller específico para un canal específico.
    Los tokens/API keys se guardan encriptados (o en Secrets Manager en prod).
    """
    seller = models.ForeignKey(
        "sellers.Seller", on_delete=models.CASCADE, related_name="channel_credentials"
    )
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="seller_credentials")
    # En dev: guardamos en JSONB. En prod: referencia a Secrets Manager
    credentials = models.JSONField(default=dict)
    is_valid = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = [("seller", "channel")]

    def __str__(self):
        return f"{self.seller} @ {self.channel}"
