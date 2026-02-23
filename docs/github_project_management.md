# Manual de Gestión del Proyecto con GitHub (SellersCenter)

Este documento establece los estándares y metodologías obligatorias para la gestión del proyecto **SellersCenter** utilizando las herramientas integradas de GitHub. El objetivo es mantener una trazabilidad absoluta, facilitar la colaboración y asegurar que cada línea de código responda a un requerimiento de negocio o mejora técnica documentada.

---

## 1. Visión General del Flujo de Trabajo

Emplearemos un enfoque basado en **GitHub Flow** combinado con elementos de gestión de proyectos ágiles (Kanban/Scrum) a través de **GitHub Projects**. Todo el trabajo debe comenzar con un [Issue](#2-gestión-de-issues) documentado.

**Ciclo de vida básico de una tarea:**
1.  **Idea/Requisito:** Se crea un Issue.
2.  **Planificación:** El Issue se asigna a un *Milestone* (Sprint o Release) y se ubica en el tablero del *GitHub Project*.
3.  **Desarrollo:** Un desarrollador se auto-asigna el Issue, mueve la tarjeta a "In Progress" y crea una rama local.
4.  **Revisión:** Se abre un *Pull Request (PR)* vinculado al Issue. Se ejecutan automáticamente las validaciones (CI/CD).
5.  **Aprobación:** Al menos 1 revisor aprueba el código (Code Review).
6.  **Despliegue/Cierre:** El PR se mergea a `develop` (o `main` según el caso), lo que cierra automáticamente el Issue asociado.

---

## 2. Gestión de Issues 

Los Issues son la única fuente de la verdad para bugs, nuevas features, tareas técnicas o deuda técnica. **NUNCA se debe escribir código sin un Issue que lo respalde.**

### 2.1 Plantillas de Issues (Templates)

Para asegurar la consistencia, el repositorio está configurado con plantillas. Al abrir un Issue, debes seleccionar el tipo correcto:

*   **🐛 Bug Report:** Para informar de fallos en producción o entornos de desarrollo.
    *   *Debe contener:* Pasos para reproducir, Comportamiento esperado, Comportamiento real, Logs relevantes, Entorno (Browser, SO, Versión).
*   **✨ Feature Request:** Para solicitar nuevas funcionalidades.
    *   *Debe contener:* Historia de usuario ("Como [rol], quiero [acción] para [beneficio]"), Criterios de aceptación claros.
*   **🛠️ Technical Task:** Para tareas de infraestructura, refactorización, o DevOps.

### 2.2 Uso de Etiquetas (Labels)

Las etiquetas son fundamentales para filtrar y categorizar en el tablero.

*   **Tipos (`type:*`):** `type:bug`, `type:feature`, `type:enhancement`, `type:documentation`, `type:tech-debt`.
*   **Prioridad (`priority:*`):** `priority:critical` (hotfix), `priority:high`, `priority:medium`, `priority:low`.
*   **Estado Módulos (`module:*`):** `module:catalog`, `module:orders`, `module:sync-engine`, `module:infra`.

---

## 3. GitHub Projects (Tablero Ágil)

Utilizaremos un *GitHub Project V2* (tipo tablero Kanban) a nivel de la organización para tener visibilidad transversal.

### 3.1 Columnas del Tablero

*   **Todo (Backlog):** Tareas priorizadas listas para ser tomadas.
*   **In Progress:** Tareas actualmente en desarrollo. *Regla: Un desarrollador no debe tener más de 2 tareas en esta columna simultáneamente (WIP Limit).*
*   **In Review:** El desarrollo terminó y hay un Pull Request abierto esperando revisión de pares.
*   **In QA / Staging:** El PR fue mergeado a `develop` y está desplegado en el entorno de pruebas para validación funcional.
*   **Done:** El código está en producción (`main`) y validado.

### 3.2 Automatización del Tablero

Conecta los PRs con los Issues usando palabras clave (ver sección 5). Al abrir un PR vinculado, la tarjeta del Issue se moverá automáticamente a "In Review". Al cerrar el PR, se moverá a "Done" (vía configuración de workflows de GitHub Projects).

---

## 4. Milestones (Gestión de Releases/Sprints)

Los *Milestones* agrupan Issues y Pull Requests en ventanas de tiempo o entregables específicos.

1.  **Nombrado:** Usa nombres semánticos como `v1.0.0-MVP` o de Sprints cronológicos como `Sprint 24 - Octubre`.
2.  **Fechas:** Todo Milestone debe tener una fecha límite (*due date*).
3.  **Seguimiento:** Utiliza la vista del Milestone para medir el progreso (% completado) en tiempo real durante la reunión diaria (Daily Standup) o el cierre de ciclo. No se puede dar por cerrado un Milestone si quedan Issues abiertos asociados a él.

---

## 5. Pull Requests (PR) y Code Review

El Pull Request es el punto de control de calidad. 

### 5.1 Reglas para abrir un PR
1.  **Título Descriptivo:** Sé claro sobre lo que hace el PR. Ejemplo: `feat(orders): agrega soporte para validación de DNI`.
2.  **Vinculación:** Usa "Closing keywords" en la descripción del PR para vincularlo al Issue correspondiente. Ej: `Closes #42` o `Resolves #105`. Esto cerrará mágicamente el Issue cuando el PR sea aprobado y mergeado.
3.  **Size Matters:** Los PRs deben ser pequeños y enfocados en una sola responsabilidad. PRs de más de 500 líneas de código añadido tendrán altas chances de ser rechazados sin revisión.

### 5.2 El Proceso de Code Review

*   El autor debe asignar al menos a 1 revisor (*Reviewer*).
*   **Reviewer Checklist:**
    *   ¿El código soluciona el problema descrito en el Issue asociado?
    *   ¿El código es legible y sigue las guías de estilo del proyecto?
    *   ¿Se han incluido tests unitarios que cubren los casos de éxito y de borde?
    *   ¿La integración continua (GitHub Actions) está en verde?
*   Nadie debe *mergear* su propio PR.
*   Si se requiere que el PR no se revise de inmediato y es solo colaborativo, usar la función **Draft Pull Request**.

## Resumen Ejecutivo para Developers
1. No toques código si no hay un Issue.
2. Si agarras un Issue, asígnatelo y muévelo a "In Progress".
3. Vincula tu PR al Issue con `Closes #num`.
4. El CI/CD verde y un `Approve` son obligatorios para hacer merge.
