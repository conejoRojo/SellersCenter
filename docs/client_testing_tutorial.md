# Guía de Pruebas: SellersCenter (Entorno Staging / Local)

Este documento contiene las instrucciones y credenciales necesarias para que el cliente (Aper / Dixer) pueda probar los flujos de la plataforma SellersCenter desde el exterior.

> [!WARNING]
> **Aviso de Infraestructura Local:** Si el sistema aún no ha sido desplegado en AWS (Fase 7), estas pruebas requieren que la computadora host (donde corre el Docker y Django) exponga sus puertos a internet mediante un túnel seguro (ej. **ngrok**, **Cloudflare Tunnels** o **Tailscale**). Las URLs provistas aquí son ejemplos descriptivos.

## 🔗 URLs de Acceso

El sistema se compone de dos interfaces independientes:

1. **Dashboard de Comercio (Sellers)**
   *   **Objetivo:** Interfaz para que cada tienda vea su catálogo, órdenes y ventas centralizadas.
   *   **URL (Local):** `http://localhost:5173`
   *   **URL (Túnel Público):** `https://moody-symbols-throw.loca.lt`

2. **Consola de Administración (Aper Admin)**
   *   **Objetivo:** Interfaz de superadministrador para ver la salud del sistema global y métricas de integraciones.
   *   **URL (Local):** `http://localhost:5174`
   *   **URL (Túnel Público):** `https://full-tips-watch.loca.lt`

---

## 🔐 Credenciales de Prueba (Demo Users)

Se han generado perfiles pre-cargados mediante el script `init_demo_users`. Utiliza estos datos en las pantallas de Login de cada portal.

### 1. Perfil Administrador Global (Para "frontend-aper")
*   **Usuario (Email):** `admin@sellerscenter.local`
*   **Contraseña:** `admin123`
*   **Rol:** Superuser (Acceso total al hub de integraciones).

### 2. Perfil Tienda Beta (Para "frontend-seller")
*   **Usuario (Email):** `seller1@demo.com`
*   **Contraseña:** `seller123`
*   **Tenant ID:** `TENANT-ALFA-001`
*   **Rol:** Dueño de tienda (Solo ve los productos y órdenes de su propio Tenant).

---

## 🧪 Casos de Uso a Probar

Sugerimos al cliente ejecutar el siguiente flujo de pruebas para evaluar el MVP:

### Prueba 1: Vista General de Catálogo
1. Ingrese al **Dashboard de Comercio** con las credenciales de la Tienda Beta.
2. Navegue a la sección **Catálogo**.
3. Verifique la existencia de productos mockeados con disponibilidad de stock y estado de sincronización (Sincronizado/Agotado/Error).

### Prueba 2: Recepción Asíncrona (Backend)
*(Esta prueba requiere herramientas como Postman o cURL).*
1. Envíe un payload JSON simulando una actualización de producto desde PrestaShop al endpoint público del backend (`https://chilly-mirrors-sleep.loca.lt/api/v1/sync/ingesta/`).
2. Valide que el sistema de forma inmediata responda **HTTP 202 Accepted** (confirmando que Celery y la cola SQS tomaron el control).
3. Ingrese a la **Consola de Administración** y revise en el módulo *Integraciones & Webhooks* si hubo actividad reflejada.

### Prueba 3: Aislamiento de Datos (Multitenancy)
1. Estando en la **Consola de Administración**, inspeccione la lista global de Tenants. Note que existen múltiples tiendas.
2. En una pestaña incógnito, ingrese al **Dashboard de Comercio** con el perfil de Tienda Beta.
3. Valide que la información visible de ventas, órdenes y catálogos está estrictamente aislada y filtrada, perteneciendo únicamente al "tenant_id" de la Tienda Beta.
