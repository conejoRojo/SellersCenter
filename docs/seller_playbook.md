# Playbook Operativo del Seller (SellersCenter)

¡Bienvenido a SellersCenter! Esta plataforma es tu única parada para gobernar el inventario y los pedidos de todos tus canales de venta (Mercado Libre, Amazon, Tiendanube, Shopify).

---

## 1. Misión del Seller
Centralizar. En lugar de cambiar un precio 4 veces en 4 páginas distintas, lo haces una vez aquí, y SellersCenter se encarga de gritarlo ("sincronizarlo") a todos los canales. El tiempo promedio de sincronización es menor a **3 segundos**.

## 2. Gestión de Catálogo

Tu catálogo en SC es el "Catálogo Maestro".

### Regla del Origen de la Verdad (Single Source of Truth)
*   Nunca actualices precios, inventarios o variantes directamente en los portales de Mercado Libre o Amazon. Si lo haces, el sistema podría sobrescribirlos en la próxima sincronización.
*   **Acción:** Siempre utiliza el Panel de SellersCenter (o conecta tu propio ERP a nuestra API).

### Pausa Masiva
*   Si notas un error grave en precios o te quedaste sin stock crítico global, usa el botón "Pausar Venta Omnicanal" en el dashboard principal. Esto enviará webhooks de emergencia a todas las integraciones para pausar tus publicaciones externamente.

## 3. Resolución de Errores de Sincronización

A veces, Mercado Libre rechaza un cambio tuyo (ej. un título contiene una palabra prohibida o la imagen es muy pequeña).

1.  **Tablero de Sincronización:** Revisa la campana de notificaciones del panel.
2.  **Estado "Fallido":** Si un producto figura como fallido para Shopify, haz clic en "Ver Detalle". SC te mostrará exactamente el JSON / Mensaje de rechazo que devolvió el canal externo.
3.  **Corrección:** Corrige el error en el catálogo de SC y guarda. El sistema re-encolará el producto para intentar actualizarlo inmediatamente en todos los Marketplaces.

## 4. Gestión de Pedidos Multicanal

Cualquier venta que caiga en cualquiera de tus canales aparece unificada en *Órdenes*.

*   **Identificación:** Verás el ID interno de SC, y un ícono mostrando el origen (Amazon, MeLi, manual, etc) con su ID Externo (External_ID).
*   **Facturación (ERP):** Si tienes conectado tu sistema Contable, tan pronto como la orden cambia al estado `Paid` (Pagada), SC avisa a tu ERP mediante un webhook para que emitas la factura electrónica.
*   **Logística:** No despaches el producto hasta que el estado no sea `ReadyToShip`. 

Si necesitas asistencia avanzada, contacta al Account Manager en `soporte-sc@aper.com`.
