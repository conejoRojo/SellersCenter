# Guía de Configuración: Entorno de Agente Orquestador

Este documento detalla cómo replicar exactamente el entorno de trabajo "Antigravity + NotebookLM + Claude CLI" en otra computadora (Windows, Mac o Linux) para mantener el mismo flujo de Ingeniería de Software Asistida por IA (Vibecoding / Delegación de Tareas).

## 1. El Orquestador Principal (Google / Antigravity)
Este es el cerebro central que planifica la arquitectura, revisa los archivos y orquesta a los demás.
*   **Prerrequisito:** Permisos o acceso al cliente de escritorio/consola que estás utilizando actualmente para comunicarte conmigo (Antigravity/Gemini).
*   **Archivos Base:** Necesitarás copiar el directorio del proyecto (`SellersCenter`) o al menos tu archivo `implementation_plan.md` y `task.md` para que el agente recupere el contexto inmediatamente en la nueva PC.

## 2. El Cerebro Documental (NotebookLM MCP Server)
Para que el Orquestador principal pueda leer cientos de páginas de manuales (ej: AWS, RFI, manuales de PrestaShop) sin llenar su memoria a corto plazo, usamos NotebookLM.

### Instalación del puente (MCP Server)
El Model Context Protocol (MCP) es el estándar que permite a Antigravity hablar con NotebookLM.
1. Instala Node.js (v18+) en la nueva PC.
2. Abre una terminal e instala el servidor globalmente:
   ```bash
   npm install -g notebooklm-mcp
   ```
   *(Nota: si el cliente orquestador soporta instalación vía Smithery, usa `npx @smithery/cli install notebooklm-mcp --client <nombre-del-cliente>`)*.

### Autenticación
1. Una vez instalado, desde el chat del orquestador pide: *"Ejecuta setup_auth para NotebookLM"*.
2. Se abrirá un navegador. Inicia sesión en la cuenta de Google que tiene el Notebook de "SellersCenter".
3. A partir de ese momento, el Orquestador podrá usar herramientas como `list_notebooks` y `ask_question` para consultar la documentación pesada.

## 3. La Fuerza Bruta de Código (Claude Code CLI / Codex)
Para evitar gastar dólares en tokens de API enviando miles de líneas de código desde el Orquestador, delegamos tareas pesadas de programación rutinaria (ej: "Aplica Tailwind a estos 50 componentes") a agentes CLI vinculados a suscripciones "Pro" de tarifa plana.

### Instalación de Claude Code
1. Requiere Node.js.
2. En la terminal ejecuta:
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```
3. Autentícate con tu cuenta Claude Pro:
   ```bash
   claude login
   ```
4. **Configuración "Vibecoding" (Bypass de Seguridad):**
   Para que el Orquestador pueda lanzar tareas a Claude en segundo plano sin que Claude pause pidiendo que "presiones Enter para confirmar", debes configurar permanentemente esta variable de entorno en la nueva PC:
   *   **Windows (PowerShell):** `[Environment]::SetEnvironmentVariable("CLAUDE_CODE_DANGEROUSLY_SKIP_PERMISSIONS_AGREEMENT", "1", "User")`
   *   **Mac/Linux:** Añadir `export CLAUDE_CODE_DANGEROUSLY_SKIP_PERMISSIONS_AGREEMENT=1` al `~/.zshrc` o `~/.bashrc`.

## Flujo de Trabajo (El Loop)
Una vez en la nueva PC, tu ciclo será:
1. **Analizar:** "Antigravity, revisa en NotebookLM cómo debe ser la arquitectura de X."
2. **Planear:** "Antigravity, diseña la estructura de archivos y actualiza el `implementation_plan.md`."
3. **Delegar:** "Antigravity, ejecuta un comando en la terminal ordenándole a `claude` (o ejecutando un pipeline de Codex) que respete este plan y escriba el código."
4. **Supervisar:** Revisar los pull requests o los diffs generados.
