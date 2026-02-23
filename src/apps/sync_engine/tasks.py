from celery import shared_task
from django.db import transaction
from apps.catalog.models import Product, Category
from apps.orders.models import Order, OrderItem
from apps.sellers.models import Seller
from apps.channels.models import Channel
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, acks_late=True)
def process_inbound_webhook(self, payload: dict):
    """
    Procesamiento asíncrono de un webhook entrante desde un canal externo.
    Reside en SQS/Redis y es procesado por un worker de Celery.
    """
    integration_id = payload.get('integration_id')
    event_type = payload.get('event_type')
    channel_type = payload.get('channel_type')
    data = payload.get('data', {})

    logger.info(f"Procesando webhook asíncrono. Tenant: {integration_id} | Evento: {event_type}")

    try:
        seller = Seller.objects.get(tenant_id=integration_id)
        channel, _ = Channel.objects.get_or_create(slug=channel_type, defaults={'name': channel_type.capitalize()})
    except Seller.DoesNotExist:
        logger.error(f"Seller no encontrado para integration_id: {integration_id}")
        return False
        
    try:
        with transaction.atomic():
            if event_type in ['catalog.initial_sync', 'catalog.updated']:
                _process_catalog_sync(seller, channel, data)
            elif event_type == 'order.created':
                _process_order_creation(seller, channel, data)
            else:
                logger.warning(f"Evento no soportado: {event_type}")
                return False
        return True

    except Exception as e:
        logger.exception(f"Error procesando webhook. Re-encolando intento {self.request.retries}/3.")
        raise self.retry(exc=e, countdown=10 ** self.request.retries) # Backoff exponencial


def _process_catalog_sync(seller, channel, data):
    items = data.get('items', [])
    for item in items:
        sku = item.get('sku')
        title = item.get('title', f"Product {sku}")
        price = item.get('price', 0.0)
        stock = item.get('stock', 0)
        market_attrs = item.get('attributes', {})
        
        product, created = Product.objects.update_or_create(
            seller=seller, 
            sku=sku,
            defaults={
                'name': title,
                'base_price': price,
                'base_stock': stock,
                'is_active': item.get('status') == 'active'
            }
        )
        # Guardo en JSONB la metadata específica de este marketplace
        product.set_marketplace_attrs(channel.slug, market_attrs)
        product.save()

def _process_order_creation(seller, channel, data):
    ext_order_id = data.get('external_order_id')
    amount = data.get('total_amount', 0.0)
    
    order, created = Order.objects.get_or_create(
        seller=seller,
        channel=channel,
        external_order_id=ext_order_id,
        defaults={
            'total_amount': amount,
            'status': 'pending_payment'
        }
    )
    
    if created:
        for item in data.get('items', []):
            product = Product.objects.filter(seller=seller, sku=item.get('sku')).first()
            if product:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item.get('qty', 1),
                    unit_price=product.base_price
                )
