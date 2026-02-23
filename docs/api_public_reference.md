# Referencia Pública Estándar: API-REST SellersCenter

*(Esta documentación está diseñada para consumo de las agencias de integración conectando nuevos Marketplaces o ERPs hacia SellersCenter).*

---

## Filosofía de Integración

SellersCenter emplea una arquitectura **API-First** bajo un esquema de **Petición e Idempotencia Asíncrona**. 
Esto significa que las agencias integradoras (Los Conectores de MKs que diseña Aper) interactúan a través de un **Sync Engine** estandarizado.

**URL Base de Staging:** `https://api.staging.sellerscenter.io/v1/`
**Autenticación:** Token JWT provisto al momento de la configuración inicial en el panel "Developers" de SC. Enviar por Header: `Authorization: Bearer <TKN>`

---

## Endpoint Estrella: Ingestion de Cambios (Sync Engine)

Este endpoint recibe todas las notificaciones externas. No importa si es un pedido de Shopify, un cambio de stock de Vtex o una pregunta de MeLi. El motor enruta de manera agnóstica basándose en el payload.

`POST /sync-engine/webhook/`

### Payload Body (Agnóstico)

El payload entrante debe estar uniformizado según la estructura de SellersCenter independientemente del Marketplace de origen.

```json
{
  "integration_id": "uuid-v4-of-api-tenant",
  "channel_type": "mercadolibre", // enum: [mercadolibre, shopify, vtex, amazon]
  "event_type": "order.created", // catalog.updated, order.status_changed, etc.
  "timestamp": "2024-04-12T15:00:22Z",
  "data": {
     // Información específica de SellersCenter unificada
     "external_order_id": "1298418000",
     "items": [
         {"sku": "ZAP-AIR-001", "quantity": 1, "price": 125.00}
     ],
     "raw_channel_payload": { ... } // El Request original completo (guardado en DB JSONB para debug audit)
  }
}
```

### Respuesta y Comportamiento Asíncrono

La API **nunca** procesará en caliente el payload para evitar tiempos de espera largos (Timeouts) a las plataformas originadoras perdiendo las Notificaciones (Webhooks).

**Response Exitoso:** `HTTP 202 Accepted`
SellersCenter recibe el JSON, comprueba la autorización, lo guarda estáticamente en Redis o PostgreSQL efímero y arroja el mensaje en la cola SQS configurada al Celery Worker. 

**Response de Fallo (Auth):** `HTTP 401 Unauthorized`

---

## Endpoint Saliente (Webhooks de SC hacia Integradores)

Dada una acción manual o regla de negocio iniciada por un Seller desde el Frontend (Ej: Pausar una publicación o cambiar masivamente el esquema de precios), el flujo se invierte.

Celery procesará la regla interna en SellersCenter y enviará hacia la URL configurada por los Integradores el comando final listo. El equipo de Integración (Aper) tiene como máxima tarea recibir, traducir al API del Marketplace externo (ej: API Meli PUT `/items/{id}`) y ejecutar.

`POST https://{api-conector-aper.com}/sc-inbound-sync/`

**Ejemplo Payload Generado por SC hacia Aper Connectors:**

```json
{
  "source": "SellersCenter::SyncOutbound",
  "event": "product.price.modified",
  "seller_id": "uid-seller-abc",
  "target_channels": ["mercadolibre_AR", "vtex_CL"],
  "unified_product": {
     "sc_id": "prd-90123",
     "sku_base": "MACB-PRO-M3",
     "new_price": 2500000.00
  }
}
```

## Rate Limiting

La entrada a `/sync-engine/` posee Throttle rate limiting configurado mediante el API Gateway de AWS para proteger RDS PostgreSQL y sus workers. Las respuestas emitirán error `HTTP 429 Too Many Requests` adjuntando el encabezado `Retry-After: {seconds}` en caso de sobrepasar el pico contratado.
