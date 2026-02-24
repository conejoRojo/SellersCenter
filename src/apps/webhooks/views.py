import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import WebhookEvent

logger = logging.getLogger(__name__)


class WebhookReceiverView(APIView):
    """
    Endpoint genérico de recepción de webhooks externos.
    Registra el evento y lo encola para procesamiento async.
    Siempre responde 200 rápidamente (el procesamiento real es async).
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, channel_slug, event_type):
        try:
            event = WebhookEvent.objects.create(
                event_type=event_type,
                payload=request.data,
                headers=dict(request.headers),
                status=WebhookEvent.Status.QUEUED,
            )
            # TODO: encolar en SQS/Celery para procesamiento
            # process_webhook_task.delay(event.id)
            logger.info("Webhook recibido: id=%s type=%s channel=%s", event.id, event_type, channel_slug)
        except Exception:
            logger.exception("Error registrando webhook")

        return Response({"status": "received"}, status=200)
