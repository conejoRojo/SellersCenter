from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import uuid

class SyncEngineIngestionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('sync_engine:ingestion-webhook')
        self.valid_payload = {
            "integration_id": str(uuid.uuid4()),
            "channel_type": "mercadolibre",
            "event_type": "catalog.updated",
            "timestamp": "2024-04-12T15:00:22Z",
            "data": {
                "batch_id": "test-batch-1",
                "items": [
                    {"sku": "TEST-SKU-1", "price": 100.50, "stock": 10}
                ]
            }
        }

    def test_webhook_ingestion_valid_payload_returns_202(self):
        """ Prueba que un JSON agnóstico válido retorne 202 Inmediato para encolar en Celery """
        response = self.client.post(self.url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn('accepted', response.data['status'])

    def test_webhook_ingestion_invalid_payload_returns_400(self):
        """ Prueba que si falta algun campo requerido en el JSON estándar, rebota con 400 Bad Request """
        invalid_payload = self.valid_payload.copy()
        invalid_payload.pop('integration_id') # Campo requerido

        response = self.client.post(self.url, data=invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
