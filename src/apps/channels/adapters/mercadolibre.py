"""
Adaptador para Mercado Libre.
Documentación API: https://developers.mercadolibre.com/
"""

import hashlib
import hmac
import logging
from decimal import Decimal

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .base import BaseMarketplaceAdapter, OrderData, PublishResult

logger = logging.getLogger(__name__)

ML_API_BASE = "https://api.mercadolibre.com"


class MercadoLibreAdapter(BaseMarketplaceAdapter):
    """
    Adaptador para la API de Mercado Libre.
    Normaliza productos, pedidos y actualizaciones al formato SC.
    """

    def _get_session(self) -> requests.Session:
        """Sesión con retry automático para resiliencia."""
        session = requests.Session()
        retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503])
        session.mount("https://", HTTPAdapter(max_retries=retry))
        return session

    def _headers(self, access_token: str) -> dict:
        return {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

    def publish_product(self, product, credentials: dict) -> PublishResult:
        """Publica el producto en MeLi usando el formato de su API."""
        access_token = credentials.get("access_token")
        ml_attrs = product.get_marketplace_attrs("mercadolibre")

        payload = {
            "title": product.name,
            "category_id": ml_attrs.get("category_id", "MLA1000"),
            "price": float(product.base_price),
            "currency_id": "ARS",
            "available_quantity": product.base_stock,
            "buying_mode": "buy_it_now",
            "listing_type_id": ml_attrs.get("listing_type", "gold_special"),
            "condition": ml_attrs.get("condition", "new"),
            "description": {"plain_text": product.description},
            "pictures": [{"source": url} for url in product.images[:12]],
            "attributes": ml_attrs.get("attributes", []),
        }

        try:
            session = self._get_session()
            response = session.post(
                f"{ML_API_BASE}/items",
                json=payload,
                headers=self._headers(access_token),
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            logger.info("MeLi publish success: product=%s, meli_id=%s", product.sku, data["id"])
            return PublishResult(success=True, external_id=data["id"], raw_response=data)

        except requests.HTTPError as e:
            error_msg = f"MeLi API error {e.response.status_code}: {e.response.text}"
            logger.error("MeLi publish failed: product=%s, error=%s", product.sku, error_msg)
            return PublishResult(success=False, error_message=error_msg)
        except Exception as e:
            logger.exception("MeLi publish unexpected error: product=%s", product.sku)
            return PublishResult(success=False, error_message=str(e))

    def update_price(self, external_id: str, price: Decimal, credentials: dict) -> PublishResult:
        try:
            session = self._get_session()
            response = session.put(
                f"{ML_API_BASE}/items/{external_id}",
                json={"price": float(price)},
                headers=self._headers(credentials["access_token"]),
                timeout=15,
            )
            response.raise_for_status()
            return PublishResult(success=True, external_id=external_id)
        except requests.HTTPError as e:
            return PublishResult(success=False, error_message=str(e))

    def update_stock(self, external_id: str, stock: int, credentials: dict) -> PublishResult:
        try:
            session = self._get_session()
            response = session.put(
                f"{ML_API_BASE}/items/{external_id}",
                json={"available_quantity": stock},
                headers=self._headers(credentials["access_token"]),
                timeout=15,
            )
            response.raise_for_status()
            return PublishResult(success=True, external_id=external_id)
        except requests.HTTPError as e:
            return PublishResult(success=False, error_message=str(e))

    def pause_listing(self, external_id: str, credentials: dict) -> PublishResult:
        try:
            session = self._get_session()
            response = session.put(
                f"{ML_API_BASE}/items/{external_id}",
                json={"status": "paused"},
                headers=self._headers(credentials["access_token"]),
                timeout=15,
            )
            response.raise_for_status()
            return PublishResult(success=True, external_id=external_id)
        except requests.HTTPError as e:
            return PublishResult(success=False, error_message=str(e))

    def parse_order_webhook(self, raw_payload: dict) -> OrderData:
        """
        Normaliza el payload de webhook de pedido de MeLi al formato SC.
        MeLi notifica el ID del pedido; hay que hacer GET para obtener los detalles.
        """
        # MeLi solo envía una notificación con el ID, el detalle se obtiene por API
        # En un webhook real, el Worker haría el GET al recibirlo
        order_id = raw_payload.get("resource", "").split("/")[-1]

        return OrderData(
            external_id=order_id,
            buyer_name=raw_payload.get("buyer", {}).get("nickname", ""),
            buyer_email="",  # Se obtiene con GET /orders/{id}
            items=[],        # Se obtiene con GET /orders/{id}/items
            total_amount=Decimal("0"),
            currency="ARS",
            status=raw_payload.get("status", "unknown"),
            raw_data=raw_payload,
        )

    def confirm_order(self, external_id: str, credentials: dict) -> bool:
        # MeLi no requiere confirmación explícita; el pedido se acepta automáticamente
        return True

    def validate_webhook_signature(self, payload: bytes, signature: str, secret: str) -> bool:
        """
        MeLi firma los webhooks con HMAC-SHA256.
        Header: x-signature contiene 'ts={timestamp},v1={hash}'
        """
        try:
            parts = dict(item.split("=") for item in signature.split(","))
            ts = parts.get("ts", "")
            v1 = parts.get("v1", "")
            message = f"{ts}.{payload.decode()}"
            expected = hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()
            return hmac.compare_digest(expected, v1)
        except Exception:
            logger.warning("MeLi webhook signature validation failed")
            return False
