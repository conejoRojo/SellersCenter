import os
import random
import requests
import json
import time

# Script para emular la migración masiva de un catálogo inicial de un MK hacia SellersCenter
# Uso: python emulate_catalog_migration.py --seller_id 123 --items 5000

SC_API_URL = os.environ.get("SC_API_URL", "http://localhost:8000/api/v1/sync-engine/webhook/")
AUTH_TOKEN = os.environ.get("SC_AUTH_TOKEN", "dev-secret-jwt")

def generate_fake_product(index):
    return {
        "sku": f"MK-ITEM-{index}-{random.randint(1000, 9999)}",
        "title": f"Producto Emulado {index}",
        "price": round(random.uniform(10.0, 5000.0), 2),
        "stock": random.randint(0, 500),
        "status": random.choice(["active", "paused", "out_of_stock"]),
        "attributes": {
            "brand": "Genérica",
            "condition": "new"
        }
    }

def emulate_migration(seller_id="tenant-alpha-001", total_items=1000, batch_size=100):
    print(f"Iniciando emulación de migración para Seller: {seller_id}")
    print(f"Total ítems a ingerir: {total_items} (Batch size: {batch_size})")

    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

    success_count = 0
    failed_count = 0

    for i in range(0, total_items, batch_size):
        batch_items = [generate_fake_product(j) for j in range(i, min(i + batch_size, total_items))]
        
        payload = {
            "integration_id": seller_id,
            "channel_type": "mercadolibre",
            "event_type": "catalog.initial_sync",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "data": {
                "batch_id": f"batch-{i//batch_size}",
                "items": batch_items
            }
        }

        try:
            # En entorno real, esto encola en SQS y responde 202
            response = requests.post(SC_API_URL, json=payload, headers=headers)
            if response.status_code in [200, 202]:
                success_count += len(batch_items)
                print(f"[{success_count}/{total_items}] Lote enviado correctamente.")
            else:
                failed_count += len(batch_items)
                print(f"Error {response.status_code}: {response.text}")
        except requests.exceptions.ConnectionError:
            print("Error: No se pudo conectar al Sync Engine de SellersCenter. Está corriendo el servidor en localhost:8000?")
            return

        time.sleep(0.5) # Throttle leve para no saturar la red local

    print("\n--- Migración Finalizada ---")
    print(f"Items Exitosos (Encolados): {success_count}")
    print(f"Items Fallidos: {failed_count}")

if __name__ == "__main__":
    emulate_migration(total_items=5000)
