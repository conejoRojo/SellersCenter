from django.db import models
from apps.core.models import TimeStampedModel


class Order(TimeStampedModel):

    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        CONFIRMED = "confirmed", "Confirmado"
        PAID = "paid", "Pagado"
        PREPARING = "preparing", "En preparación"
        SHIPPED = "shipped", "Enviado"
        DELIVERED = "delivered", "Entregado"
        CANCELLED = "cancelled", "Cancelado"
        REFUNDED = "refunded", "Reembolsado"

    channel = models.ForeignKey(
        "channels.Channel", on_delete=models.PROTECT, related_name="orders"
    )
    seller = models.ForeignKey(
        "sellers.Seller", on_delete=models.PROTECT, related_name="orders"
    )
    external_id = models.CharField(max_length=255, db_index=True,
                                   help_text="ID del pedido en el marketplace")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    buyer_name = models.CharField(max_length=255)
    buyer_email = models.EmailField(blank=True)
    buyer_phone = models.CharField(max_length=30, blank=True)
    shipping_address = models.JSONField(default=dict)
    currency = models.CharField(max_length=3, default="ARS")
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    # Datos originales del marketplace (para auditoría)
    raw_data = models.JSONField(default=dict)

    class Meta:
        unique_together = [("channel", "external_id")]
        verbose_name = "pedido"
        verbose_name_plural = "pedidos"

    def __str__(self):
        return f"Orden #{self.external_id} — {self.channel} — {self.status}"


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    variant = models.ForeignKey(
        "catalog.ProductVariant", on_delete=models.PROTECT, related_name="order_items",
        null=True, blank=True
    )
    external_item_id = models.CharField(max_length=255, blank=True)
    sku = models.CharField(max_length=100)
    name = models.CharField(max_length=500)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.order} × {self.quantity} {self.sku}"
