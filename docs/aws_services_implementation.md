# Manual de Implementación y Configuración AWS (SellersCenter Producción)

Este manual es la guía definitiva para instanciar la arquitectura productiva de SellersCenter en Amazon Web Services (AWS), garantizando el cumplimiento del SLA de 99.5% exigido en el RFI y las mejores prácticas de disponibilidad y seguridad.

---

## 1. Topología de Redes (VPC)

El despliegue debe realizarse en una **Virtual Private Cloud (VPC)** dedicada para SellersCenter, abarcando al menos 2, preferiblemente 3 Zonas de Disponibilidad (AZs) para cumplir con el SLA.

*   **Subredes Públicas (2+):** Solo alojarán el Application Load Balancer (ALB) y NAT Gateways. Tienen ruta directa a Internet (IGW).
*   **Subredes Privadas (2+):** Alojarán los contenedores de ECS Fargate (Django API y Celery Workers). La salida a internet se hace a través de los NAT Gateways públicos.
*   **Subredes de Base de Datos (2+):** Completamente aisladas. Alojarán Amazon RDS, ElastiCache y RDS Proxy. Cero conectividad a Internet.

---

## 2. Amazon RDS PostgreSQL & RDS Proxy (Capa de Datos)

Dado el alto volumen transaccional (40k+ transacciones en picos) y el escalado masivo de contenedores serverless, la configuración de la BD requiere ajustes críticos:

1.  **Motor:** Amazon Aurora PostgreSQL (Serverless v2 recomendado para picos impredecibles) o RDS PostgreSQL Estándar de clase `r6g` (Memoria optimizada).
2.  **Multi-AZ:** Obligatorio activar la opción Multi-AZ Cluster (Aurora) o Standby Instance (RDS clásico) para failover automático en menos de 60 segundos.
3.  **RDS Proxy (CRÍTICO):** 
    *   Cualquier conexión hacia la BD desde ECS (Django o Celery) **debe pasar por el endpoint de RDS Proxy**.
    *   *Razón:* Previene el agotamiento de conexiones (Connection exhaustion) multiplexando las conexiones de los workers Celery hacia el clúster.

---

## 3. Amazon Elastic Container Service (ECS Fargate)

Las cargas de trabajo de computación se despliegan utilizando Fargate, evitando la gestión de servidores EC2 subyacentes.

*   **Cluster ECS:** Un solo cluster `sellerscenter-prod-cluster`.
*   **Servicios (Services):**
    *   `sc-api-service`: Corre los contenedores de la API de Django. Está conectado al Application Load Balancer. Se configura un Auto Scaling asociado a la CPU (Target 70%) para invocar más contenedores en CyberMondays.
    *   `sc-worker-service`: Corre los workers de Celery. No está expuesto a Load Balancers. Escala (Service Auto Scaling) basado en la profundidad de la cola de SQS (`ApproximateNumberOfMessagesVisible`).
    *   `sc-beat-service`: Corre un único contenedor `celery-beat` para tareas programadas. Fijo en `DesiredCount=1` para evitar ejecución múltiple.

---

## 4. Amazon SQS (Procesamiento Asíncrono)

Sustituimos el uso de Redis como Broker (usado en entorno local) por SQS de AWS para garantizar persistencia y manejo de errores empresarial.

*   `incoming-webhooks`: Cola estándar. Recibe los payloads masivos de los conectores MK.
*   `sync-outbound`: Cola FIFO o estándar. Encola las actualizaciones desde los Sellers hacia los MKs.
*   **Dead-Letter Queues (DLQ):** Por cada cola, debe existir su correspondiente DLQ (Ej: `incoming-webhooks-dlq`).
    *   *Configuración:* Especificar un `maxReceiveCount=3`. Si un worker falla 3 veces en tratar de procesar un mensaje (por errores de la DB temporal o bug en datos), se retira de la cola principal y va al DLQ, levantando una alarma en CloudWatch para inspección humana. Evita el bloqueo del resto del procesamiento.

---

## 5. ElastiCache Redis

Exclusivamente para Caché de resultados costosos de la API y manejo de sesiones, **NO** para broker de mensajes.

*   Configuración: Clúster de Redis versión 7.x, con *Cluster Mode Disabled* pero con *Replicas* (Primary + Replica) distribuido en 2 Zonas de Disponibilidad. Activación obligatoria de *Multi-AZ with Auto-Failover*.

---

## 6. Seguridad (WAF, IAM y Secrets Manager)

1.  **AWS Secrets Manager:** Absolutamente ninguna contraseña, JWT Secret o Key de integración se guarda en texto plano ni en variables de entorno del `docker-compose.yml`. El `TaskDefinition` de Fargate debe hacer *reference* al Secret Manager para inyectar estos valores al inicio del contenedor.
2.  **AWS WAF (Web Application Firewall):** Acoplado directamente a CloudFront (Frontend) o al API Gateway. Obligatorio reglas administradas anti-bot, mitigación SQL injection (OWASP T10) y Rate Limiting por IP para evitar ataques de fuerza bruta al endpoint de Webhooks.

---

## 7. Observabilidad Completa (CloudWatch y X-Ray)

Para demostrar y resolver problemas del SLA comprometido:
*   **CloudWatch Logs:** Logs centralizados mediante formato JSON estructurado desde los Task Definitions a `awslogs` driver.
*   **CloudWatch Alarms:**
    *   Mensajes > 0 en cualquier fila DLQ (Severidad: Alta).
    *   CPU/RAM Load en RDS Proxy (Severidad: Crítica).
    *   HTTP 500s > 2% en Target Group de ALB (Severidad: Alta).
*   **AWS X-Ray (Opcional pero Recomendable):** Instalación del daemon `aws-otel` (OpenTelemetry) como sidecar en Fargate para rastrear la vida de una Request desde el ALB hasta la caída en Postgres y posterior consumo en Celery Worker.
