from rest_framework import serializers

class WebhookItemSerializer(serializers.Serializer):
    sku = serializers.CharField(max_length=150)
    quantity = serializers.IntegerField(required=False)
    price = serializers.DecimalField(max_digits=12, decimal_places=2, required=False)
    title = serializers.CharField(max_length=500, required=False)
    stock = serializers.IntegerField(required=False)
    status = serializers.CharField(max_length=50, required=False)
    attributes = serializers.DictField(required=False)


class WebhookDataSerializer(serializers.Serializer):
    external_order_id = serializers.CharField(max_length=255, required=False)
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=False)
    batch_id = serializers.CharField(max_length=150, required=False)
    items = WebhookItemSerializer(many=True, required=False)
    raw_channel_payload = serializers.DictField(required=False)


class WebhookPayloadSerializer(serializers.Serializer):
    """
    Formato Estándar Agnóstico de Ingesta para SellersCenter.
    Todos los Webhooks externos deben ser mapeados a este formato por los Conectores de Aper.
    """
    integration_id = serializers.UUIDField()
    channel_type = serializers.ChoiceField(choices=["mercadolibre", "amazon", "vtex", "shopify", "woocommerce", "magento"])
    event_type = serializers.ChoiceField(choices=[
        "catalog.initial_sync",
        "catalog.updated",
        "order.created",
        "order.status_changed"
    ])
    timestamp = serializers.DateTimeField()
    data = WebhookDataSerializer()

