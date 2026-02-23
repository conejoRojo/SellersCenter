# SellersCenter — Dockerfile
# Multi-stage build: imagen final liviana sin herramientas de build

# ──────────────────────────────────────────────
# Stage 1: Build de dependencias
# ──────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /build

# Dependencias del sistema para compilar psycopg2 y otros paquetes C
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python en un virtualenv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ──────────────────────────────────────────────
# Stage 2: Imagen de producción
# ──────────────────────────────────────────────
FROM python:3.12-slim AS production

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH" \
    DJANGO_SETTINGS_MODULE="config.settings.development"

# Runtime: solo libpq (cliente PostgreSQL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar el virtualenv del stage anterior
COPY --from=builder /opt/venv /opt/venv

# Crear usuario no-root para seguridad
RUN useradd --create-home --shell /bin/bash appuser
WORKDIR /app
RUN chown appuser:appuser /app
USER appuser

# Copiar código de la aplicación
COPY --chown=appuser:appuser src/ .

# collectstatic se ejecuta en el entrypoint (docker-compose command),
# no aquí, para evitar depender de DB/Redis durante el build.

EXPOSE 8000

# Health check (para ECS y ALB)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Gunicorn como servidor WSGI en producción
CMD ["gunicorn", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--worker-class", "gthread", \
     "--threads", "2", \
     "--timeout", "60", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "config.wsgi:application"]
