# Plan de Implementación: Maestro de Ceremonias para SellersCenter

Este documento detalla la estrategia para regenerar el proyecto SellersCenter, cumpliendo estrictamente con el RFI de APER, la propuesta de DIXER y las mejoras arquitectónicas propuestas (RDS Proxy intermedio, Dead Letter Queues, separación de caché y broker). Todo será validado localmente utilizando LocalStack.

## 1. Estrategia de Subagentes (El Equipo Orquestado)
Como "Maestro de Ceremonias", crearé y desplegaré subagentes (scripts de Python autónomos) simulando un equipo de desarrollo completo en `D:\Desarrollo\NotebookLM\agents\`:

*   **`agent_sc_infra.py` (Ingeniero Cloud / DevOps):**
    *   **Misión:** Generar archivos de orquestación (`docker-compose.yml`, scripts de inicialización).
    *   **Estado:** [x] Completado.
*   **`agent_sc_backend.py` (Desarrollador Backend Python):**
    *   **Misión:** Scaffolding del código de aplicación en Django DRF, implementación de lógica de negocio (MVP) y tests.
    *   **Estado:** [/] En Progreso (Falta lógica MVP).
*   **`agent_sc_frontend.py` (Desarrollador Frontend React/Vite):**
    *   **Misión:** Generar los portales SPA (Seller Dashboard y Aper Admin) y conectarlos a la API REST.
    *   **Estado:** [ ] Pendiente.
*   **`agent_sc_qa.py` (Ingeniero QA / Automation):**
    *   **Misión:** Ejecutar y documentar pruebas unitarias sistemáticas de cada endpoint y lógica de Celery, verificando el comportamiento.
    *   **Estado:** [ ] Pendiente.
*   **`agent_sc_docs.py` (Technical Writer):**
    *   **Misión:** Redactar la documentación técnica y playbooks operativos.
    *   **Estado:** [x] Completado.

## 2. Cambios Propuestos en Archivos

### 2.1. Sistema Orquestador (Directorio Raíz)
*   `[NEW]` `D:\Desarrollo\NotebookLM\agents\agent_sc_infra.py`
*   `[NEW]` `D:\Desarrollo\NotebookLM\agents\agent_sc_backend.py`
*   `[NEW]` `D:\Desarrollo\NotebookLM\agents\agent_sc_docs.py`

### 2.2. Infraestructura SellersCenter (`projects/SellersCenter/infra/`)
*(Archivos generados por `agent_sc_infra.py`)*
*   `[NEW/MODIFY]` `docker-compose.yml` (Incluyendo LocalStack, PgBouncer, Postgres, Redis, Django, Celery Workers).
*   `[NEW]` `init-localstack.sh` (Para arrancar automáticamente colas SQS, DLQs y buckets S3).
*   `[NEW/MODIFY]` `.env.local`

### 2.3. Backend SellersCenter (`projects/SellersCenter/src/`)
*(Archivos generados por `agent_sc_backend.py`)*
*   `[NEW/MODIFY]` `config/settings.py` (Ajustado para integrarse con LocalStack vía boto3).
*   `[NEW]` `config/celery.py` (Configurado para leer y escribir de SQS LocalStack y soportar DLQs).
*   `[NEW]` `apps/catalog/models.py`, `apps/orders/models.py`, `apps/webhooks/views.py`.

### 2.4. Documentación Exhaustiva (`projects/SellersCenter/docs/`)
*(Archivos generados por `agent_sc_docs.py`)*
*   `[NEW]` `aws_localstack_guide.md` (Guía "para dummies").
*   `[NEW]` `architecture_v2.md` (La arquitectura final consolidada con RDS Proxy, DLQs y Redis desacoplado).

## 3. Plan de Verificación (Testing Local)

### 3.1. Validación de Infraestructura Local:
1. Ejecutaremos `docker-compose up -d` en el directorio de SellersCenter.
2. Ejecutaremos comandos de prueba contra LocalStack: `aws --endpoint-url=http://localhost:4566 sqs list-queues` para verificar colas de pedidos y DLQs.

### 3.2. Validación de API y Worker:
1. Lanzaremos la aplicación web y los workers de Celery.
2. Se realizará un test funcional inyectando un payload JSON al endpoint de webhooks y observando si el worker asíncrono consume el mensaje de SQS.

## 4. Plan de Extensión y Tareas Detalladas (Progreso)

### Fase 5: Emulación y Pruebas de Estrés
*   **Estado:** [x] Completado
*   - [x] Script de emulación de migración de catálogos masivos.
*   - [x] Suite de pruebas de estrés (Locust) para el CyberMonday.

### Fase 6: DevSecOps y Gestión de Proyecto (GitHub)
*   **Estado:** [x] Completado
*   - [x] `docs/github_project_management.md`.
*   - [x] `docs/github_ci_cd_manual.md`.

### Fase 7: Infraestructura Cloud Reales (AWS)
*   **Estado:** [/] En Progreso
*   - [x] `docs/aws_services_implementation.md` (Manual detallado implementado).
*   - [x] Scripts IaC (Terraform) para desplegar VPC, RDS, ECS y SQS en AWS.

### Fase 8: Documentación Externa y Playbooks
*   **Estado:** [x] Completado
*   - [x] `docs/api_public_reference.md`.
*   - [x] `docs/seller_playbook.md`.
*   - [x] `docs/onboarding_guide.md`.

### Fase 9: Demostración al Cliente
*   **Estado:** [x] Completado
*   - [x] `docs/demo_guide_dixer_aper.md` (Guion de Demo Final).

### Fase 10: Scaffolding de Frontends (React/Vite)
*   **Estado:** [x] Completado (A cargo de `agent_sc_frontend`)
*   - [x] Configurar monorepo/carpetas para `frontend-seller` y `frontend-aper`.
*   - [x] Programar boilerplate con Vite + React + TailwindCSS.
*   - [x] Configurar Axios y auth JWT para consumo de API Django.

### Fase 11: Programación Core del MVP Backend y Testing (Celery/Django)
*   **Estado:** [x] Completado (A cargo de `agent_sc_backend` y `agent_sc_qa`)

#### Funcionalidades MVP (A Revisar por Aper):
*   - [x] Recepción unificada de Webhooks de múltiples Marketplaces en un solo endpoint.
*   - [x] Autenticación de integradores mediante JWT en los endpoints API (Bypass local via HMCA config).
*   - [x] Encolado asíncrono (HTTP 202) para procesamiento diferido sin bloquear al emisor.
*   - [x] Procesamiento asíncrono robusto (Celery + SQS) con tolerancia a fallos y reintentos (DLQ ready).
*   - [x] Persistencia del payload crudo como Snapshot histórico de auditoría.
*   - [x] Creación/Actualización automática del catálogo de Seller e Inserción de nuevas Órdenes Unificadas.
*   - [x] Tablero operativo Básico de Sellers (Ventas/Órdenes) consumible vía REST.

#### Tareas de Programación MVP:
*   - [x] **Auth & Superuser:** Script para crear usuarios base (admin, seller1, seller2).
*   - [x] **Serializers:** Crear `WebhookPayloadSerializer` en `sync_engine` para validar el JSON agnóstico de entrada.
*   - [x] **Views (Endpoints):** Escribir la vista `IngestionWebhookView` (POST `sync-engine/webhook/`) que retorne HTTP 202.
*   - [x] **Celery Tasks:** Escribir la tarea asíncrona `@shared_task: process_inbound_webhook` que busque/cree el catálogo en PostgreSQL.
*   - [x] **Endpoints REST Exposición:** Crear `ModelViewSet` para `orders` y `catalog`.

#### Pruebas Unitarias (TDD / QA):
*   - [x] Completar `tests/test_sync_engine.py` validando la inyección de errores (Rate Limits simulados) y asserts de creación en base de datos.
*   - [x] Testear con django/pytest el Celery Task.
