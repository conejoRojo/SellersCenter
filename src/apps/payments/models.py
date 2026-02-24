from django.db import models
from apps.core.models import TimeStampedModel


class Payment(TimeStampedModel):

    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        APPROVED = "approved", "Aprobado"
        REJECTED = "rejected", "Rechazado"
        REFUNDED = "refunded", "Reembolsado"

    class Provider(models.TextChoices):
        MERCADOPAGO = "mercadopago", "MercadoPago"
        PAYPAL = "paypal", "PayPal"
        STRIPE = "stripe", "Stripe"
        BANK_TRANSFER = "bank_transfer", "Transferencia bancaria"
        OTHER = "other", "Otro"

    order = models.OneToOneField(
        "orders.Order", on_delete=models.CASCADE, related_name="payment"
    )
    provider = models.CharField(max_length=30, choices=Provider.choices)
    external_id = models.CharField(max_length=255, blank=True,
                                   help_text="ID del pago en el gateway")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default="ARS")
    paid_at = models.DateTimeField(null=True, blank=True)
    raw_data = models.JSONField(default=dict)

    class Meta:
        verbose_name = "pago"
        verbose_name_plural = "pagos"

    def __str__(self):
        return f"Pago {self.provider} — {self.status} — ${self.amount}"
