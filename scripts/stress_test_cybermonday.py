from locust import HttpUser, task, between
import uuid
import random
import time

# Pruebas de Estrés para SellersCenter (CyberMonday Simulator)
# Comando para ejecutar (requiere pip install locust):
# locust -f stress_test_cybermonday.py --host=http://localhost:8000

class SCTrafficSimulator(HttpUser):
    wait_time = between(0.1, 0.5) # Simula usuarios/sistemas golpeando rápido
    
    def on_start(self):
        """ Inicialización: Simularemos que somos una integración externa (ej. MeLi) """
        self.headers = {
            "Authorization": "Bearer stress-test-token",
            "Content-Type": "application/json"
        }
        self.tenant_id = str(uuid.uuid4())
        
    @task(3)
    def simulate_order_creation_webhook(self):
        """ Simula la llegada agresiva de nuevos pedidos desde un Marketplace (Alto volumen en CyberMonday) """
        order_id = random.randint(1000000, 9999999)
        payload = {
            "integration_id": self.tenant_id,
            "channel_type": random.choice(["mercadolibre", "vtex", "amazon"]),
            "event_type": "order.created",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "data": {
                "external_order_id": str(order_id),
                "total_amount": round(random.uniform(500, 150000), 2),
                "items": [
                    {"sku": f"SKU-{random.randint(1, 1000)}", "qty": random.randint(1, 3)}
                ]
            }
        }
        # Hacemos POST al Sync Engine. Esperamos un HTTP 202 Accepted inmediato (encolado en SQS).
        with self.client.post("/api/v1/sync-engine/webhook/", json=payload, headers=self.headers, catch_response=True) as response:
            if response.status_code == 202:
                response.success()
            elif response.status_code == 429:
                response.failure("Rate limit alcanzado (Esto es esperado si el WAF frena el estrés)")
            else:
                response.failure(f"Error inesperado: {response.status_code}")

    @task(1)
    def simulate_seller_dashboard_read(self):
        """ Simula a un Seller recargando desesperadamente su dashboard de ventas """
        # Para evitar colapsar la base de datos de lectura, esto debería tocar caché Redis
        self.client.get("/api/v1/orders/dashboard-metrics/", headers=self.headers)

# Configuración sugerida para correr:
# locust -f src/scripts/stress_test_cybermonday.py --users 500 --spawn-rate 50 --host http://<ALB_URL_OW_LOCAL>
