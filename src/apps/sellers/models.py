from django.db import models
from apps.core.models import TimeStampedModel


class Seller(TimeStampedModel):
    """
    Seller registrado en SellersCenter.
    Un User puede tener un perfil Seller asociado.
    """

    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente de aprobación"
        ACTIVE = "active", "Activo"
        SUSPENDED = "suspended", "Suspendido"

    user = models.OneToOneField(
        "accounts.User", on_delete=models.CASCADE, related_name="seller_profile"
    )
    tenant_id = models.CharField(max_length=255, unique=True, null=True, help_text="ID único de integración (UUID) para Webhooks")
    business_name = models.CharField(max_length=255, verbose_name="Razón social")
    tax_id = models.CharField(max_length=50, unique=True, verbose_name="CUIT/RUT")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    commission_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=0,
        help_text="Porcentaje de comisión del SC sobre ventas del seller."
    )
    # Configuración general del seller
    settings = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = "seller"
        verbose_name_plural = "sellers"

    def __str__(self):
        return f"{self.business_name} ({self.tax_id})"

    def is_active(self):
        return self.status == self.Status.ACTIVE
