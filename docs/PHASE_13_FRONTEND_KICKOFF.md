# Fase 13: Kickoff de Desarrollo Frontend (Multi-agente) e Integración UI

Este documento sirve como contexto explícito (Memoria de Estado) para iniciar la próxima sesión de trabajo, así como manual operativo para la coordinación con el equipo de Diseño UI/UX.

## 🚀 Prompt de Inicialización (Copiar y pegar en el nuevo chat)

> "Asume tu rol de Maestro de Ceremonias / Orquestador. Lee el archivo `docs/PHASE_13_FRONTEND_KICKOFF.md`. Hemos finalizado con éxito la Fase 12 (CI/CD y Túneles Cloudflare). El backend API, la base de datos PostgreSQL, Celery/RabbitMQ y los dos frontends Vite están funcionales locales.
>
> Iniciaremos la **Fase 13: Desarrollo React y Conexión de API**. Quiero que despliegues subagentes de forma paralela (Multi-agente) para maquetar el `frontend-seller` y el `frontend-aper` simultáneamente, usando los datos de `admin@sellerscenter.local` y los endpoints MVP que ya existen. Ten en cuenta la Guía de Diseño estipulada abajo para no pisarnos con mi equipo creativo humano."

---

## 🎨 Coordinación con el Equipo Humano de Diseño

SellersCenter utiliza un stack moderno: **React 18 + Vite + TailwindCSS v4**.
Ya que tu equipo de diseño está acostumbrado a trabajar con HTML puro y CSS tradicional, aquí explicamos el flujo de trabajo para que el equipo de Inteligencia Artificial (Agentes) y el equipo Humano (Diseñadores) colaboren sin romper el código.

### 1. ¿Cómo trabajaremos juntos (El Flujo)?
1. **Paso 1 (Los Agentes construyen los 'Ladrillos'):** Nosotros (la IA) armaremos la estructura base (los archivos `.jsx`), el enrutamiento y la *lógica* de conexión a Django (Axios, JWT, manejo de estados). Implementaremos un diseño MVP funcional "en blanco y negro" o con colores pálidos usando TailwindCSS estructural.
2. **Paso 2 (Los Diseñadores aplican 'La Pintura'):** Tu equipo humano entrará a los archivos generados y meterá mano libremente para reemplazar clases, embeber sus estilos o ajustar las dimensiones y la identidad de marca (tipografías, colores de Aper, etc.).

### 2. ¿Qué archivos PUEDE tocar libremente el equipo de diseño?

Los diseñadores deben enfocarse exclusivamente en las carpetas `src/` de los dos frontends (`frontend-seller/src/` y `frontend-aper/src/`).

✅ **`src/index.css` (CSS Tradicional):**
*   **Permitido:** Aquí pueden escribir CSS clásico, reglas anidadas, declarar `@font-face` o animaciones pesadas `@keyframes`. Como usamos TailwindCSS v4, este archivo es el lugar perfecto para declarar sus *Design Tokens* globales (ejemplo: `@theme { --color-aper-blue: #003366; }`).

✅ **Los archivos `src/components/.../*.jsx` y `src/pages/.../*.jsx` (El "HTML"):**
*   **Permitido:** En React, el HTML vive dentro de archivos `.jsx`. Los diseñadores pueden abrir estos archivos y modificar libremente la propiedad `className="..."` de las etiquetas. Si prefieren no usar Tailwind, pueden simplemente agregar una clase clásica (ej. `className="btn-primario"`) y luego darle estilo en `index.css`.
*   **Cuidado:** Solo deben modificar el contenido visual que está dentro del bloque `return ( ... )`. No deben borrar llaves lógicas (ejemplo: `{producto.nombre}`) ni funciones que estén arriba del `return`, ya que ahí vive la programación de los agentes lógicos.

✅ **`src/assets/` (Imágenes y Fuentes):**
*   Pueden agregar todos los `.svg`, `.png`, iconos, logos y tipografías que el MVP necesite.

### 3. ¿Qué archivos NO DEBEN tocar los diseñadores?
❌ `package.json` y `vite.config.js`: Son archivos de configuración del motor.
❌ Carpetas de Backend (`src/`, fuera de los frontends) o Infraestructura (`infra/`, `docker-compose.yml`).
❌ Estados en JSX y llamadas Axios (Ejemplo: `const [data, setData] = useState()`).

### 4. Alternativa de Trabajo Bimodal (Cero fricción)
Si el equipo de diseño siente mucha fricción tocando código `.jsx` de React:
1. Ellos pueden maquetar el HTML puro y el CSS en una carpeta separada por fuera (Ej. `disenos_html/`).
2. Nosotros (la Inteligencia Artificial) nos encargaremos de "traducir" o "componentizar" de forma automática sus hojas de estilo `.css` y código `.html` a componentes de React, incrustando las variables lógicas de Django dentro de su obra de arte.

¡Todo listo para orquestar los agentes paralelos y levantar el Front!
