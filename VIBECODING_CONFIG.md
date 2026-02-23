# Configuración de Modo Vibecoding

**Estado Actual:** `TRUE` (Activado)
**Palabra Clave de Seguridad:** `Cocó`

## Reglas del Modo
*   **Vibecoding = TRUE:** El agente (Antigravity) tiene permisos absolutos para tomar decisiones arquitectónicas, escribir código, instalar dependencias, ejecutar comandos, borrar archivos y avanzar de fase sin consultar al usuario. Actuará de forma autónoma hasta finalizar el objetivo.
*   **Vibecoding = FALSE:** El agente volverá al modo estándar colaborativo, requiriendo confirmación («notify_user») antes de realizar cambios estructurales o avanzar de fase.

*(Nota interna para Antigravity: Leer este estado antes de evaluar si se detiene para pedir permiso en tareas complejas).*
