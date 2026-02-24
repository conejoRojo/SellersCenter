from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import WebhookPayloadSerializer
from .tasks import process_inbound_webhook
import logging

logger = logging.getLogger(__name__)

class IngestionWebhookView(APIView):
    """
    Endpoint de Ingesta Unificada (Sync Engine).
    Recibe los payloads estandarizados de las integraciones de Aper.
    Debe responder lo más rápido posible (HTTP 202) y derivar a Celery/SQS.
    """
    permission_classes = [] # En el MVP permitiremos sin auth para testear fácil con Locust. En Prod va IsAuthenticated.

    def post(self, request, *args, **kwargs):
        serializer = WebhookPayloadSerializer(data=request.data)
        
        if serializer.is_valid():
            # El payload es válido según el RFI. Enviar a SQS/Redis mediante Celery.
            payload = serializer.validated_data
            
            # Casteamos UUIDs y Decimals a string/float para json serialization en Celery
            if 'integration_id' in payload:
                payload['integration_id'] = str(payload['integration_id'])
            if 'timestamp' in payload:
                payload['timestamp'] = payload['timestamp'].isoformat()
            
            # Invocar tarea asíncrona
            process_inbound_webhook.delay(payload)
            
            logger.info(f"Webhook aceptado y encolado en SQS/Redis. Tenant: {payload['integration_id']}")
            
            return Response(
                {"status": "accepted", "message": "Payload safely enqueued for asynchronous processing."},
                status=status.HTTP_202_ACCEPTED
            )
            
        else:
            logger.warning(f"Payload inválido recibido: {serializer.errors}")
            return Response(
                {"status": "error", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
