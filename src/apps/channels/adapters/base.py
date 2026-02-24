"""
Interfaz base que todo adaptador de marketplace debe implementar.
Garantiza que el SC pueda hablar con cualquier canal de la misma manera.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from decimal import Decimal


@dataclass
class PublishResult:
    success: bool
    external_id: Optional[str] = None  # ID del producto en el marketplace
    error_message: Optional[str] = None
    raw_response: Optional[dict] = None


@dataclass
class OrderData:
    external_id: str
    buyer_name: str
    buyer_email: str
    items: list
    total_amount: Decimal
    currency: str
    status: str
    raw_data: dict  # Datos originales del marketplace (para debugging)


class BaseMarketplaceAdapter(ABC):
    """
    Contrato que todos los adaptadores de marketplace deben cumplir.
    Normaliza las diferencias entre APIs de distintos marketplaces.
    """

    @abstractmethod
    def publish_product(self, product, credentials: dict) -> PublishResult:
        """
        Publica o actualiza un producto en el marketplace.
        Recibe el modelo Product de SC y las credenciales del seller.
        """
        ...

    @abstractmethod
    def update_price(self, external_id: str, price: Decimal, credentials: dict) -> PublishResult:
        """Actualiza el precio de un producto ya publicado."""
        ...

    @abstractmethod
    def update_stock(self, external_id: str, stock: int, credentials: dict) -> PublishResult:
        """Actualiza el stock de un producto ya publicado."""
        ...

    @abstractmethod
    def pause_listing(self, external_id: str, credentials: dict) -> PublishResult:
        """Pausa la publicación de un producto."""
        ...

    @abstractmethod
    def parse_order_webhook(self, raw_payload: dict) -> OrderData:
        """
        Normaliza un webhook de pedido del marketplace al formato interno de SC.
        Cada marketplace tiene un formato diferente; este método lo unifica.
        """
        ...

    @abstractmethod
    def confirm_order(self, external_id: str, credentials: dict) -> bool:
        """Confirma la recepción/aceptación de un pedido al marketplace."""
        ...

    def validate_webhook_signature(self, payload: bytes, signature: str, secret: str) -> bool:
        """
        Valida la firma HMAC del webhook.
        Por defecto devuelve True (cada adapter puede sobreescribir).
        En producción, SIEMPRE sobreescribir este método.
        """
        return True
