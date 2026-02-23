"""
Catálogo de productos — modelo central con JSONB para atributos por marketplace.
"""

from django.db import models
from django.contrib.postgres.fields import ArrayField
from apps.core.models import SoftDeleteModel


class Category(SoftDeleteModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="children"
    )

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Product(SoftDeleteModel):
    """
    Producto base en el catálogo del seller.
    El campo marketplace_data almacena atributos específicos por canal.

    Ejemplo de marketplace_data:
    {
        "mercadolibre": {
            "category_id": "MLA1234",
            "listing_type": "gold_special",
            "condition": "new",
            "attributes": [{"id": "BRAND", "value_name": "Nike"}]
        },
        "amazon": {
            "asin": "B0XXXX",
            "brand": "Nike",
            "bullet_points": ["Punto 1", "Punto 2"]
        },
        "shopify": {
            "handle": "zapatilla-nike",
            "vendor": "Nike",
            "tags": ["ropa", "deportes"]
        }
    }
    """
    seller = models.ForeignKey(
        "sellers.Seller", on_delete=models.CASCADE, related_name="products"
    )
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL, related_name="products"
    )
    sku = models.CharField(max_length=100)
    name = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=12, decimal_places=2)
    base_stock = models.IntegerField(default=0)
    # JSONB — atributos específicos por marketplace
    marketplace_data = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    images = ArrayField(models.URLField(), default=list, blank=True)

    class Meta:
        unique_together = [("seller", "sku")]

    def __str__(self):
        return f"{self.seller} — {self.sku}: {self.name}"

    def get_marketplace_attrs(self, channel_slug: str) -> dict:
        """Devuelve los atributos específicos del producto para un canal."""
        return self.marketplace_data.get(channel_slug, {})

    def set_marketplace_attrs(self, channel_slug: str, attrs: dict):
        """Actualiza atributos de un canal específico sin pisar los demás."""
        self.marketplace_data[channel_slug] = attrs


class ProductVariant(SoftDeleteModel):
    """
    Variantes del producto (talle, color, etc.).
    Cada variante tiene su propio SKU, precio y stock.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)  # "Talle M - Rojo"
    price_override = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        help_text="Si está vacío, usa el precio base del producto."
    )
    stock = models.IntegerField(default=0)
    attributes = models.JSONField(default=dict)  # {"color": "rojo", "talle": "M"}

    @property
    def price(self):
        return self.price_override or self.product.base_price

    def __str__(self):
        return f"{self.product.sku} | {self.sku} — {self.name}"


class ChannelListing(SoftDeleteModel):
    """
    Representa la publicación de un producto en un marketplace específico.
    Es la unión entre Product y Channel.
    """

    class Status(models.TextChoices):
        DRAFT = "draft", "Borrador"
        ACTIVE = "active", "Activo"
        PAUSED = "paused", "Pausado"
        OUT_OF_STOCK = "out_of_stock", "Sin stock"
        ERROR = "error", "Error de sincronización"

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="channel_listings")
    channel = models.ForeignKey(
        "channels.Channel", on_delete=models.CASCADE, related_name="listings"
    )
    external_id = models.CharField(
        max_length=255, blank=True,
        help_text="ID del producto en el marketplace externo."
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    price_override = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        help_text="Precio específico para este canal. Si vacío, usa precio base."
    )
    last_sync_at = models.DateTimeField(null=True, blank=True)
    sync_errors = models.JSONField(default=list)

    class Meta:
        unique_together = [("product", "channel")]

    def __str__(self):
        return f"{self.product.sku} @ {self.channel}"
