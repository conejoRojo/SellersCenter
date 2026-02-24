"""
Adapter pattern para marketplaces.
Cada marketplace implementa la interfaz BaseMarketplaceAdapter.
"""

from .base import BaseMarketplaceAdapter


def get_adapter(channel_slug: str) -> BaseMarketplaceAdapter:
    """
    Factory que devuelve el adaptador correcto según el slug del canal.
    Lanza NotImplementedError si el canal no tiene adaptador implementado.
    """
    adapters = {
        "mercadolibre": "apps.channels.adapters.mercadolibre.MercadoLibreAdapter",
        "amazon": "apps.channels.adapters.amazon.AmazonAdapter",
        "shopify": "apps.channels.adapters.shopify.ShopifyAdapter",
    }

    if channel_slug not in adapters:
        raise NotImplementedError(f"No hay adaptador implementado para: {channel_slug}")

    module_path, class_name = adapters[channel_slug].rsplit(".", 1)
    import importlib
    module = importlib.import_module(module_path)
    return getattr(module, class_name)()
