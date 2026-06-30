# Dockerfile para Sistema de Validación de Informes v2.0 - UNTELS
# Multi-stage build para optimización

# ==========================================
# STAGE 1: Builder
# ==========================================
FROM python:3.12-slim as builder

# Metadatos
LABEL maintainer="UNTELS"
LABEL description="Sistema de Validación de Informes - Backend v2.0"
LABEL version="2.0"

# Variables de entorno para Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependencias del sistema necesarias para compilar
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias de Python en un directorio separado
RUN pip install --user --no-cache-dir -r requirements.txt

# ==========================================
# STAGE 2: Runtime
# ==========================================
FROM python:3.12-slim

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/root/.local/bin:$PATH \
    DJANGO_SETTINGS_MODULE=config.settings.production

# Instalar dependencias del sistema para runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root para seguridad
RUN useradd -m -u 1000 untels && \
    mkdir -p /app/media /app/staticfiles && \
    chown -R untels:untels /app

# Copiar dependencias de Python del builder
COPY --from=builder --chown=untels:untels /root/.local /root/.local

# Establecer directorio de trabajo
WORKDIR /app

# Copiar código de la aplicación
COPY --chown=untels:untels . .

# Crear directorios necesarios
RUN mkdir -p media/informes media/bancos_observaciones staticfiles

# Cambiar al usuario no-root
USER untels

# Exponer puerto
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health/', timeout=5)" || exit 1

# Script de entrada
COPY --chown=untels:untels docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh

ENTRYPOINT ["/app/docker-entrypoint.sh"]

# Comando por defecto
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120", "config.wsgi:application"]
