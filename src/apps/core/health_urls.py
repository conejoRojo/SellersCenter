from django.urls import path
from django.http import JsonResponse
from django.db import connection


def health_check(request):
    """
    Health check endpoint para ALB y ECS.
    Verifica que Django y la DB estén respondiendo.
    """
    try:
        connection.ensure_connection()
        db_ok = True
    except Exception:
        db_ok = False

    status = 200 if db_ok else 503
    return JsonResponse({"status": "ok" if db_ok else "degraded", "db": db_ok}, status=status)


urlpatterns = [
    path("", health_check, name="health-check"),
]
