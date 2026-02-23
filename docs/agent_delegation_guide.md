# Guía de Delegación a Agentes Externos (Claude Code & Codex)

Esta guía explica cómo configurar las herramientas de línea de comandos (CLI) de inteligencia artificial para delegarles tareas de programación dentro del proyecto SellersCenter. 

El objetivo principal de esta configuración es **utilizar suscripciones Pro (Anthropic Pro / GitHub Copilot)** mediante autenticación web (OAuth), en lugar de consumir saldos de API Keys (las cuales facturan por token). De esta forma, Antigravity puede derivarles comandos en la consola y ellos consumirán la cuota plana de la suscripción.

---

## 1. Integración con Claude Code (Anthropic)

Claude Code es la herramienta oficial de línea de comandos de Anthropic capaz de leer el código local, entender el contexto y ejecutar tareas de programación complejas.

### Instalación
Requiere Node.js instalado en tu sistema.
```bash
npm install -g @anthropic-ai/claude-code
```

### Autenticación (Modo Pro - Sin API Key)
Para enlazar la herramienta con tu cuenta de usuario (Anthropic Pro) en lugar de una API Key de consola de desarrollador:

1. Ejecuta el comando de inicio de sesión:
```bash
claude login
```
2. Se abrirá una ventana en tu navegador web.
3. Inicia sesión con tus credenciales de usuario (cuenta con suscripción Claude Pro activa).
4. Autoriza a la CLI. Una vez hecho esto, la terminal confirmará que estás autenticado.

### ¿Cómo le delego tareas Antigravity?
Una vez que `claude` funciona en tu terminal, yo (Antigravity) puedo ejecutar comandos como el siguiente para ordenarle que programe un componente específico:

```bash
claude "Por favor, ingresa a la carpeta frontend-seller/src/components y crea un nuevo componente React llamado DashboardMetrics.tsx usando Tailwind y la información del README. Actúa autónomamente."
```

---

## 2. Integración con Codex / GitHub Copilot CLI

GitHub Copilot CLI te permite consultar a la IA directamente en la terminal o pedirle que escriba/modifique código localmente. Utiliza tu suscripción a GitHub Copilot (la misma del IDE).

### Instalación
Para instalar la extensión de Copilot oficial en GitHub CLI:

1. Asegúrate de tener instalado GitHub CLI (`gh`). Si no lo tienes, descárgalo de [cli.github.com](https://cli.github.com/).
2. Instala la extensión de Copilot:
```bash
gh extension install github/gh-copilot
```

### Autenticación (Modo Pro / Copilot)
La herramienta utiliza la autenticación base de GitHub CLI. Para vincularla con tu cuenta pro:

1. Ejecuta:
```bash
gh auth login
```
2. Selecciona `GitHub.com` -> `HTTPS` -> `Login with a web browser`.
3. Pega el código que te da la terminal en el navegador web e inicia sesión con tu cuenta de GitHub (que debe tener la suscripción de Copilot activa).

### ¿Cómo le delego tareas Antigravity?
Para enviar prompts directamente a Copilot desde la consola, yo ejecutaría:

```bash
# Para sugerencias de comandos de consola:
gh copilot suggest "find all python files modified today and run pytest on them"

# Para pedirle explicaciones directamente sobre un archivo o bug:
gh copilot explain "frontend-seller/src/index.css"
```

*(Nota: Actualmente GitHub Copilot CLI está más orientado a asistencia de línea de comandos, mientras que Claude Code es un agente autónomo de ingeniería de software capaz de editar múltiples archivos de corrido).*

---

## 3. Consideraciones Financieras y de Rate Limits

*   **Tarifa Plana:** Al utilizar `claude login` y `gh auth login`, los tokens utilizados por los agentes en la terminal descuentan de los límites de uso horario de tus planes Pro (ej: X mensajes cada 5 horas en Claude Pro).
*   **Ahorro:** No generan facturación sorpresa a fin de mes por consumo de tokens de API.
*   **Límites:** Si yo (Antigravity) le envío peticiones muy agresivas a Claude Code a través de tu terminal local, es posible que agote "tu cuota de mensajes" como humano. Debemos usar esta delegación estratégicamente para tareas pesadas y repetitivas (ej: "escribe tests para estos 50 componentes").
