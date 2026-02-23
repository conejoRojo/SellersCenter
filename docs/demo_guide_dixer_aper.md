# Guión de Demostración al Cliente (Aper / Dixer)
**Proyecto SellersCenter**

Esta guía instruye paso a paso cómo conducir una demostración de impacto que compruebe que el RFI técnico fue cumplido y que superamos las expectativas en cuanto a resiliencia y escalabilidad empresarial.

---

## 1. Preparación del Entorno
Antes de iniciar la llamada con el cliente, el presentador debe ejecutar:
1.  `docker-compose up -d` en `infra/` para levantar Postgres, Redis y LocalStack.
2.  Levantar servidor web: `python src/manage.py runserver`
3.  Levantar celery en terminales separadas para mostrar el paralelismo:
    *   `celery -A config worker -n w1@%h -l info`
    *   `celery -A config worker -n w2@%h -l info`
4.  Mantener abierta una consola `awslocal` para listar las colas (SQS).

---

## 2. Apertura: Explicación de la Arquitectura Decoupled (5 mins)
Mostrar el diagrama actualizado de `architecture_v2.md`.
*   **Guion:** *"Hemos construido exactamente lo que pedían, un API-First modular. Pero fuimos un paso más allá para asegurar el SLA de 99.5%. Separamos la lectura/escritura veloz y delegamos el trabajo pesado no en la misma máquina, sino en colas SQS manejadas por Workers asíncronos."*

---

## 3. Demo 1: Ingesta Agresiva y Escalado (10 mins)
**Objetivo:** Mostrar que SellersCenter no se cuelga si 5.000 pedidos entran a la vez.

1.  **Acción:** Abrir Postman o Terminal frente al cliente. Ejecutar el script `scripts/emulate_catalog_migration.py`.
2.  **Guion:** *"Vamos a simular que un Seller está conectando su cuenta vieja de Mercado Libre e inyectando miles de productos simultáneamente a nuestra API"*.
3.  **Visualización:** Mostrar cómo el endpoint API responde `HTTP 202 Accepted` casi instantáneamente (milisegundos). 
4.  **Backend Magic:** Cambiar la pantalla hacia las 2 consolas de Celery Workers. Mostrar cómo *ambas* consumen en paralelo los "trozos" de información de la cola de SQS asíncronamente y cómo las insertan en PostgreSQL de forma transaccional. En este momento, mencionar la ventaja de RDS Proxy para evitar que Postgres muera por demasiadas conexiones simultáneas.

---

## 4. Demo 2: CiberMonday y Pruebas de Estrés (10 mins)
**Objetivo:** Demostrar cómo se comporta la aplicación bajo estrés comercial.

1.  **Acción:** Arrancar Locust (`locust -f scripts/stress_test_cybermonday.py`). Acceder a la interfaz web de Locust (localhost:8089).
2.  **Configuración frente al cliente:** Colocar 500 usuarios disparando pedidos al azar.
3.  **Visualización:** Mostrar el gráfico de tasa de éxito de la API (Request/sec altísimos, 0% fallos en API).  
4.  **Guion:** *"Incluso recibiendo 1000 requests por segundo, la API nunca falla ni bloquea a los clientes. ¿Por qué? Porque el API Gateway y DRF solo validan y mandan a SQS. El 'cuello de botella' intencional es nuestro modelo de encolado, permitiéndonos procesar todo a un ritmo seguro para la base de datos sin rechazar la conexión externa inicial"*.

---

## 5. Demo 3: Recupero de Desastres (DLQ) (5 mins)
**Objetivo:** ¿Qué pasa si la base de datos de un tercero falla?

1.  **Acción:** Provocar un fallo intencional en una tarea asíncrona (ej, detener el worker o forzar un timeout en el código).
2.  **Visualización:** Mostrar la cola "Dead Letter Queue" mediante `awslocal sqs receive-message --queue-url http://.../sync-outbound-dlq`.
3.  **Guion:** *"En arquitecturas baratas, un error rompe la cola y frena las ventas de todos los Sellers. En SellersCenter, implementamos AWS DLQ. El pedido fallido es aislado automáticamente a esta 'cárcel' para inspección humana o reintento de 24hs, mientras que el flujo de los demás pedidos sigue intacto al 100%."*

---

## 6. Cierre
*"SellersCenter no es un MVP; hemos generado una plataforma Resiliente, Segura (DevSecOps CI/CD) y Lista para AWS Grado Empresarial."*
