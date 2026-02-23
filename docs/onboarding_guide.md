# Guía de Onboarding para Nuevos Clientes (Sellers)

Este documento detalla el viaje de un nuevo Gran Seller corporativo desde la firma comercial hasta su operación full en SellersCenter.

---

## Fase 1: Kick-Off (Día 1)
El Account Manager de Aper organiza una videollamada de 45 mins. En esta llamada:
1.  Se define el *Tenant_ID* y acceso al portal.
2.  El Seller define cuántos catálogos o canales de marketplace ya posee vivos.
3.  Se le entregan al Seller o a su equipo técnico las **Credentiales API (JWT Token)** (referirles la documentación pública de API en `/docs/api_public_reference.md`).

## Fase 2: Ingesta Técnica Inicial (La Emigración a SC)
SC debe llenarse de datos antes de mandar reglas hacia afuera. El equipo técnico enviará un dump estandarizado del catálogo histórico pre-existente para cargar postgres, incluyendo los mapeos relacionales.

1.  Uso del Script de Emigración de Catálogos Masivos (ver `scripts/emulate_catalog_migration.py`). 
2.  Se validan SKUs duplicados e imágenes.
3.  *Gatekeeper Check:* La tabla Catalog de SC debe coincidir exactamente en tamaño (SKUs y precio) con el ERP de la marca antes de conectar nada más.

## Fase 3: Conexión de Marketplaces 
SC debe establecer conexión con cada Marketplace que el cliente utilice. 
*Acción del Seller:* Ingresan a la pantalla **"Integraciones"**, donde eligen sus canales (Vtex, Amazon, Meli). 
Autorizan mediante OAuth (o API Keys en sistemas legacy) que Aper hable en su nombre hacia esos Marketplaces. Los conectores de Aper reciben las credenciales validadas y se quedan a la espera.

## Fase 4: Sincronización Piloto (Full-Sync Inicial)
1.  Un operario de SC o el Seller, hacen clic en *"Sincronización Completa"*.
2.  Los Celery Workers disparan la primera bomba de mensajes asíncronos para sobreescribir / crear publicaciones activas de todos sus productos en los marketplaces enganchados.
3.  Se ejecuta un QA menor para evaluar si hay desfase en variaciones (Ej. Talle L color Rojo subió como Blanco).

## Fase 5: Go/Live (Mantenimiento reactivo)
A partir de este instante, el panel de SC es la ley. El Seller ya no trabajará a 4 manos, cualquier carga manual o actualización de stock desde su ERP pasará únicamente a través de SellersCenter, y SC emitirá los eventos al *Sync Engine*. El Seller ha subido exitosamente a la plataforma.
