# Manual Exhaustivo de CI/CD para SellersCenter

Este documento detalla el flujo de Integración Continua (CI) y Despliegue Continuo (CD) configurado mediante **GitHub Actions** para el proyecto SellersCenter. Estas medidas garantizan la calidad del código, previenen regresiones técnicas y obligan al cumplimiento de prácticas DevSecOps (OWASP) de cara al usuario comprador y a los sellers.

---

## 1. Arquitectura de Ramas (Git Flow)

Adoptamos un modelo de branching simplificado que se adapta a las Pipelines de CI/CD:

*   `main`: **Producción.** Refleja lo que está desplegado y funcionando para los clientes. Entorno totalmente protegido.
*   `develop`: **Staging / Integración.** Donde convergen todas las funcionalidades (features). Representa el próximo release.
*   Ramas de Trabajo: `feature/*`, `bugfix/*`, `hotfix/*`. Creadas siempre a partir de `develop` (o de `main` en caso de `hotfix`).

---

## 2. Reglas de Protección de Ramas (Branch Protection Rules)

La configuración del repositorio en GitHub obliga a las siguientes políticas para proteger `main` y `develop`:

1.  **Require Pull Request before merging:** Deshabilitado el commit directo a estas ramas.
2.  **Require approvals:** Todo PR requiere al menos **1 (idealmente 2) aprobaciones** de revisores autorizados.
3.  **Require status checks to pass before merging:** 
    *   Esta es la regla más importante. El PR **NO** podrá mergearse si los flujos automáticos de GitHub Actions (Linters, SAST, Tests) fallan.
    *   Las ramas deben estar actualizadas antes del merge.
4.  **No Bypass:** Nadie, ni siquiera los administradores, puede saltarse estas reglas para `main`.

---

## 3. Flujos de Trabajo (Workflows) de GitHub Actions

Los archivos de definición de workflows residen en `.github/workflows/`.  Se dividen en dos etapas principales: Validación de Código (Integración Continua) y Despliegue (Despliegue Continuo).

### Etapa 1: Validaciones de CI (Se ejecutan en CADA Pull Request)

Archivo referente: `.github/workflows/ci_checks.yml`

Este flujo se dispara ante cualquier creación o actualización de un PR apuntando a `develop` o `main`. Cuenta con los siguientes trabajos (*jobs*) distribuidos en paralelo:

#### A. Linting y Formateo (El Estándar)
Aseguramos que el código sea uniforme y legible para cualquier desarrollador actual o futuro.
*   **Herramienta:** `flake8`, `black`, `isort`.
*   **Condición de fallo:** Formato incorrecto de código o violaciones sintácticas.

#### B. Pruebas Unitarias y Cobertura (La Estabilidad)
Asegura que la lógica de negocio no se ha roto.
*   **Herramienta:** `pytest`, `coverage`.
*   **Configuración interna:** Action de GitHub levanta un contenedor PostgreSQL ligero (Service Container) y un Redis local para que las pruebas tengan un entorno real de conexión, idéntico al LocalStack.
*   **Condición de fallo:** Tests que fallen o que la cobertura total del proyecto disminuya (regla recomendada: cobertura mínima del 80%).

#### C. Análisis de Seguridad SAST (La Fortaleza DevSecOps)
Asegura el cumplimiento temprano de OWASP (Prevención de inyección, secretos crudos).
*   **Herramientas:**
    *   **TruffleHog / GitLeaks:** Escaneo de los commits en búsqueda de contraseñas, tokens JWT, o Secret Keys (ej. credenciales AWS, claves de MeLi) hardcodeadas en el código.
    *   **Bandit:** Escaneo estático de código Python buscando malas prácticas comunes de seguridad estructural.
    *   **Safety / Dependabot:** Validación de `requirements.txt` frente a bases de datos públicas de vulnerabilidades (CVEs).
*   **Condición de fallo:** Detección de código malicioso, secretos expuestos, bibliotecas comprometidas o con CVSS Severo.

---

### 3.1. Gestión de Entorno y Variables Sensibles (GitHub Secrets)

Las pruebas unitarias y el despliegue automático requieren conectarse a servicios (bases de datos, APIs de pago, claves secretas Django). **JAMÁS** deben incluirse estas credenciales directamente en los archivos `.yml` del repositorio público o privado.

Se utiliza el almacén seguro **GitHub Secrets** (`Settings > Secrets and variables > Actions`). Las claves allí configuradas permanecen encriptadas y se inyectan dinámicamente durante el pipeline:
- `DATABASE_URL`: URI de conexión a la base de datos (Ej: `postgres://admin:password@localhost:5432/sellerscenter`).
- `DJANGO_SECRET_KEY`: Llave de seguridad criptográfica del entorno de pruebas.
- `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` (Opcional si no se usa OIDC): Credenciales para el push a ECR.

Dentro del archivo `ci.yml`, estas variables se invocan usando la sintaxis de GitHub Actions: `${{ secrets.NOMBRE_DEL_SECRETO }}`.

---

### Etapa 2: Flujo de Despliegue a Staging (Se ejecuta al mergear a `develop`)

Archivo referente: `.github/workflows/deploy_staging.yml`

Una vez que el PR supera el CI y es aprobado por los pares, se consolida (merge) a la rama `develop`. Este evento dispara:

1.  **Construcción de Imágenes Seguras:** Construye la imagen Docker de la aplicación.
2.  **Trivy Vulnerability Scan:** Escaneo adicional de vulnerabilidades a nivel de sistema operativo y contenedores dentro de la imagen Docker generada.
3.  **Amazon ECR Push:** El Action asume un rol IAM en AWS (via OIDC - *OpenID Connect*, sin credenciales a largo plazo hardcodeadas) y sube la imagen etiquetada con el hash del commit a Amazon Elastic Container Registry (ECR).
4.  **Actualización de ECS Fargate:** Mediante AWS CLI, fuerza a los servicios del entorno Staging en ECS a reiniciar y desplegar la nueva imagen recién construida.
5.  **Migraciones de BD Automatizadas:** Un contenedor efímero (*Task*) de ECS, con la nueva imagen, ejecuta `python manage.py migrate` contra el RDS de Staging.

---

### Etapa 3: Flujo de Despliegue a Producción (Se ejecuta al mergear a `main`)

Archivo referente: `.github/workflows/deploy_production.yml`

Este entorno es crítico y asegura que la plataforma para los Compradores y Sellers se mantenga estable (99.5% SLA).

1.  El despliegue a `main` se realiza mediante **Release Tags** (Ej: `v1.2.0`) o un Pull Request estrictamente controlado desde `develop`.
2.  Repite internamente el empaquetado y push seguro a ECR para producción.
3.  **Despliegue Blue/Green (AWS CodeDeploy):** En producción NO se reinician los contenedores ECS "en el lugar". Se despliega el entorno "Green", se evalúa la salud interna durante un tiempo (Time buffer), y AWS ALB switchea internamente un porcentaje el tráfico sin que el sistema experimente caída (Zero Downtime).
4.  **Notificación Externa:** Si el despliegue es exitoso, una señal reporta el nuevo nivel de la versión, si algo falla el proceso de despliegue detiene todo e invoca un _rollback_ de red al ambiente estable ("Blue").

---

## 4. Guía Resolución de Problemas (Troubleshooting) para el Developer

*   **"Mi PR no me deja hacer merge (Botón gris)."**
    *   *Solución:* Revisa en la parte inferior del PR ("Checks"). Alguno falló (X roja). Dale clic a "Details" para leer los logs (Flake8 falló un espaciado, Pytest rompió un módulo). Haz fix en tu código local y haz push otra vez en tu rama; Actions correrá nuevamente de modo automático.
*   **"Commit bloqueado porque TruffleHog encontró clave expuesta."**
    *   *Solución:* Remueve las credenciales que publicaste erróneamente en el código. ¡NUNCA pongas contraseñas directas! Utiliza módulos como `python-decouple` para llamar llaves del sistema (`config('DB_PASSWORD')`).

Este sistema de orquestación protege a los usuarios y obliga el estándar del RFI DIXER y la resiliencia operativa de AWS.
