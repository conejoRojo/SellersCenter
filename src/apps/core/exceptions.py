import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Handler de excepciones de DRF personalizado.
    Normaliza todos los errores al formato:
    { "error": "mensaje", "detail": {...} }
    """
    response = exception_handler(exc, context)

    if response is not None:
        error_data = {
            "error": _get_error_message(response),
            "detail": response.data,
        }
        response.data = error_data
    else:
        # Excepción no manejada por DRF — loguear y devolver 500
        logger.exception("Unhandled exception in view: %s", context.get("view"))
        response = Response(
            {"error": "Error interno del servidor.", "detail": None},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response


def _get_error_message(response) -> str:
    status_messages = {
        400: "Datos inválidos.",
        401: "Autenticación requerida.",
        403: "Sin permisos para realizar esta acción.",
        404: "Recurso no encontrado.",
        405: "Método no permitido.",
        429: "Demasiadas solicitudes. Intentá más tarde.",
        500: "Error interno del servidor.",
    }
    return status_messages.get(response.status_code, "Error inesperado.")
