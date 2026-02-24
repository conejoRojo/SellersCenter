from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    """
    Usuario personalizado de SellersCenter.
    Extiende AbstractUser agregando rol y UUID como PK.
    """

    class Role(models.TextChoices):
        ADMIN = "admin", "Administrador (Aper)"
        SELLER = "seller", "Seller"
        API_CLIENT = "api_client", "Cliente API (Marketplace)"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.SELLER)
    phone = models.CharField(max_length=30, blank=True)
    avatar_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"

    def is_admin(self):
        return self.role == self.Role.ADMIN

    def is_seller(self):
        return self.role == self.Role.SELLER

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})"
