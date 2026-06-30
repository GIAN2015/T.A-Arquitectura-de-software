# CAPA DE INFRAESTRUCTURA

Sistema de Validación de Informes - UNTELS

---

## ¿QUÉ ES LA CAPA DE INFRAESTRUCTURA?

Es **todo lo que soporta la aplicación**:

- Configuración de Django (settings)
- Docker y orquestación
- Servidor web (Gunicorn)
- Archivos estáticos (Whitenoise)
- Variables de entorno
- Deployment

**NO** contiene lógica de aplicación.

---

## ARCHIVOS DE ESTA CAPA

```
proyecto_untels/
├── config/
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py              # ← Settings base
│   │   ├── development.py       # ← Settings desarrollo
│   │   └── production.py        # ← Settings producción
│   ├── urls.py                  # ← URLs principales
│   └── wsgi.py                  # ← WSGI config
├── docker-compose.yml           # ← Docker desarrollo
├── docker-compose.prod.yml      # ← Docker producción
├── Dockerfile                   # ← Imagen Docker
├── requirements.txt             # ← Dependencias Python
├── .env.example                 # ← Ejemplo variables de entorno
├── .env.production.example      # ← Ejemplo para producción
├── .gitignore                   # ← Archivos ignorados por Git
└── run.sh                       # ← Script de ayuda
```

---

## 1. CONFIGURACIÓN DJANGO (config/settings/)

### 1.1 base.py (77 líneas)

**Propósito:** Configuración común para todos los entornos

**Ubicación:** `/home/chapitec/Documents/chapitec/andre/T.A-Arquitectura-de-software/proyecto_untels/config/settings/base.py`

```python
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config('DJANGO_SECRET_KEY', default='django-insecure-change-me')

# APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Apps del proyecto
    'apps.usuarios',
    'apps.informes',
    'apps.reglamento',
    'apps.observaciones',
    'apps.core',
]

# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Archivos estáticos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ARCHIVOS ESTÁTICOS
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ARCHIVOS MEDIA
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# API KEYS
GROQ_API_KEY = config('GROQ_API_KEY', default='')

# SESIONES
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# VALIDADORES DE CONTRASEÑA
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# LOCALIZACIÓN
LANGUAGE_CODE = 'es-pe'
TIME_ZONE = 'America/Lima'
USE_I18N = True
USE_TZ = True
```

---

### 1.2 development.py (28 líneas)

**Propósito:** Configuración para desarrollo local

**Ubicación:** `/home/chapitec/Documents/chapitec/andre/T.A-Arquitectura-de-software/proyecto_untels/config/settings/development.py`

```python
from .base import *
import dj_database_url

# DEBUG ACTIVADO
DEBUG = True

# HOSTS PERMITIDOS (todos en desarrollo)
ALLOWED_HOSTS = ['*']

# BASE DE DATOS (SQLite)
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default='sqlite:////ruta/al/proyecto/database/db.sqlite3')
    )
}

# IPs INTERNAS (para Django Debug Toolbar futuro)
INTERNAL_IPS = ['127.0.0.1']

# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```

**Características:**
- DEBUG=True (muestra errores detallados)
- SQLite (base de datos en archivo)
- ALLOWED_HOSTS='*' (acepta cualquier host)
- Logging simple a consola

---

### 1.3 production.py (52 líneas)

**Propósito:** Configuración para producción

**Ubicación:** `/home/chapitec/Documents/chapitec/andre/T.A-Arquitectura-de-software/proyecto_untels/config/settings/production.py`

```python
from .base import *
import dj_database_url

# DEBUG DESACTIVADO
DEBUG = False

# HOSTS PERMITIDOS (desde variable de entorno)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# BASE DE DATOS (PostgreSQL con SSL)
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=600,      # Pool de conexiones
        ssl_require=True       # Requiere SSL
    )
}

# SEGURIDAD
SECURE_SSL_REDIRECT = True                   # Redirigir HTTP → HTTPS
SESSION_COOKIE_SECURE = True                 # Cookies solo HTTPS
CSRF_COOKIE_SECURE = True                    # CSRF solo HTTPS
SECURE_BROWSER_XSS_FILTER = True             # Filtro XSS
SECURE_CONTENT_TYPE_NOSNIFF = True           # No sniffing
X_FRAME_OPTIONS = 'DENY'                     # No iframes

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000               # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True        # Incluir subdominios
SECURE_HSTS_PRELOAD = True                   # Preload list

# LOGGING AVANZADO
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': config('DJANGO_LOG_LEVEL', default='INFO'),
            'propagate': False,
        },
    },
}
```

**Características de seguridad:**
- DEBUG=False
- HTTPS obligatorio
- Cookies seguras
- HSTS activado
- PostgreSQL con SSL
- Hosts permitidos restringidos

---

## 2. DOCKER

### 2.1 Dockerfile (31 líneas)

**Propósito:** Imagen Docker de la aplicación

**Ubicación:** `/home/chapitec/Documents/chapitec/andre/T.A-Arquitectura-de-software/proyecto_untels/Dockerfile`

```dockerfile
FROM python:3.12-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Dependencias del sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Crear directorios
RUN mkdir -p /app/media /app/staticfiles

# Puerto
EXPOSE 8000

# Comando por defecto
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

**Optimizaciones:**
- Imagen slim (tamaño reducido)
- `--no-cache-dir` en pip
- Limpieza de apt cache
- Variables de entorno para Python

---

### 2.2 docker-compose.yml (29 líneas) - DESARROLLO

**Propósito:** Orquestación para desarrollo

**Ubicación:** `/home/chapitec/Documents/chapitec/andre/T.A-Arquitectura-de-software/proyecto_untels/docker-compose.yml`

```yaml
version: '3.9'

services:
  db:
    image: postgres:16
    container_name: postgres-db
    environment:
      POSTGRES_DB: untels_db
      POSTGRES_USER: untels_user
      POSTGRES_PASSWORD: untels_pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
      
  web:
    build: .
    container_name: django-app
    command: sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
    volumes:
      - .:/app           # Hot reload
    ports:
      - "8000:8000"
    env_file:
      - .env
    environment:
      - DATABASE_URL=postgresql://untels_user:untels_pass@db:5432/untels_db
    depends_on:
      - db

volumes:
  postgres_data:
```

**Características:**
- Runserver de Django (hot reload)
- Volumen montado (cambios en vivo)
- PostgreSQL 16
- Migraciones automáticas

**Uso:**
```bash
docker-compose up --build
```

---

### 2.3 docker-compose.prod.yml (58 líneas) - PRODUCCIÓN

**Propósito:** Orquestación para producción

**Ubicación:** `/home/chapitec/Documents/chapitec/andre/T.A-Arquitectura-de-software/proyecto_untels/docker-compose.prod.yml`

```yaml
version: '3.9'

services:
  db:
    image: postgres:16-alpine
    container_name: untels-postgres-prod
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-untels_db}
      POSTGRES_USER: ${POSTGRES_USER:-untels_user}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - untels-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U untels_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: untels-django-prod
    restart: unless-stopped
    command: >
      sh -c "python manage.py migrate --settings=config.settings.production &&
             python manage.py collectstatic --noinput --settings=config.settings.production &&
             gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4 --timeout 120"
    volumes:
      - ./media:/app/media
      - ./staticfiles:/app/staticfiles
    ports:
      - "8000:8000"
    env_file:
      - .env
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.production
      - DATABASE_URL=postgresql://${POSTGRES_USER:-untels_user}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB:-untels_db}
    depends_on:
      db:
        condition: service_healthy
    networks:
      - untels-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  postgres_data:

networks:
  untels-network:
    driver: bridge
```

**Características de producción:**
- Gunicorn con 4 workers
- Restart policy (unless-stopped)
- Health checks para db y web
- Red aislada (untels-network)
- Volúmenes separados para media y static
- collectstatic automático
- PostgreSQL Alpine (imagen pequeña)
- Timeout de 120s

**Uso:**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## 3. DEPENDENCIAS (requirements.txt)

**Ubicación:** `/home/chapitec/Documents/chapitec/andre/T.A-Arquitectura-de-software/proyecto_untels/requirements.txt`

```txt
Django==5.0.6
psycopg2-binary==2.9.9
python-docx==1.1.2
requests==2.32.3
dj-database-url==2.1.0
python-decouple==3.8
whitenoise==6.7.0
gunicorn==22.0.0
```

**8 dependencias:**

| Paquete | Versión | Propósito |
|---------|---------|-----------|
| Django | 5.0.6 | Framework web |
| psycopg2-binary | 2.9.9 | Driver PostgreSQL |
| python-docx | 1.1.2 | Leer archivos .docx |
| requests | 2.32.3 | Cliente HTTP (para IA) |
| dj-database-url | 2.1.0 | Parse DATABASE_URL |
| python-decouple | 3.8 | Variables de entorno |
| whitenoise | 6.7.0 | Servir archivos estáticos |
| gunicorn | 22.0.0 | Servidor WSGI |

---

## 4. VARIABLES DE ENTORNO

### 4.1 .env.example (15 líneas) - DESARROLLO

```env
# Django settings
DJANGO_SECRET_KEY=django-insecure-change-this-in-production
DJANGO_SETTINGS_MODULE=config.settings.development
DEBUG=True

# Database
DATABASE_URL=sqlite:////ruta/al/proyecto/database/db.sqlite3
# Para producción con PostgreSQL: postgresql://user:password@host:5432/dbname

# Hosts permitidos (separados por coma, solo para producción)
ALLOWED_HOSTS=localhost,127.0.0.1

# API Keys
GROQ_API_KEY=your_groq_api_key_here

# Logging (opcional)
DJANGO_LOG_LEVEL=INFO
```

---

### 4.2 .env.production.example (23 líneas) - PRODUCCIÓN

```env
# Django Production Settings
DJANGO_SECRET_KEY=CHANGE-THIS-TO-A-RANDOM-SECRET-KEY
DJANGO_SETTINGS_MODULE=config.settings.production
DEBUG=False

# Allowed hosts (comma-separated)
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (PostgreSQL)
DATABASE_URL=postgresql://user:password@db:5432/untels_db
POSTGRES_DB=untels_db
POSTGRES_USER=untels_user
POSTGRES_PASSWORD=CHANGE-THIS-PASSWORD

# API Keys
GROQ_API_KEY=your-groq-api-key-here

# Logging
DJANGO_LOG_LEVEL=INFO

# Email (opcional - para notificaciones)
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=your-email@gmail.com
# EMAIL_HOST_PASSWORD=your-app-password
```

---

## 5. ARCHIVOS ESTÁTICOS

### Configuración Whitenoise

```python
# config/settings/base.py
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Recopilar archivos estáticos

```bash
python manage.py collectstatic --noinput
```

**Resultado:** 126 archivos copiados a `staticfiles/`

### Estructura

```
staticfiles/
├── admin/          # Django admin
├── css/           # CSS personalizado (futuro)
├── js/            # JavaScript (futuro)
└── img/           # Imágenes (futuro)
```

---

## 6. WSGI (config/wsgi.py)

**Propósito:** Punto de entrada para servidores WSGI (Gunicorn)

```python
import os
from django.core.wsgi import get_wsgi_application
from decouple import config

# Usar producción por defecto en WSGI
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    config('DJANGO_SETTINGS_MODULE', default='config.settings.production')
)

application = get_wsgi_application()
```

---

## 7. SCRIPT DE AYUDA (run.sh)

**Propósito:** Menú interactivo para desarrollo

**Ubicación:** `/home/chapitec/Documents/chapitec/andre/T.A-Arquitectura-de-software/proyecto_untels/run.sh`

```bash
#!/bin/bash

# Activar entorno virtual
source venv/bin/activate

# Menú
echo "1) Iniciar servidor de desarrollo"
echo "2) Ejecutar tests"
echo "3) Ejecutar migraciones"
echo "4) Crear superusuario"
echo "5) Recopilar archivos estáticos"
echo "6) Abrir shell de Django"
echo "7) Limpiar base de datos y reiniciar"
echo "8) Salir"

read -p "Selecciona una opción: " option

case $option in
    1) python manage.py runserver ;;
    2) python manage.py test --verbosity=2 ;;
    3) python manage.py makemigrations && python manage.py migrate ;;
    4) python manage.py createsuperuser ;;
    5) python manage.py collectstatic --noinput ;;
    6) python manage.py shell ;;
    7) rm -f db.sqlite3 && python manage.py migrate ;;
    8) exit 0 ;;
esac
```

**Uso:**
```bash
chmod +x run.sh
./run.sh
```

---

## 8. DEPLOYMENT

### Desarrollo Local

```bash
# 1. Clonar repo
git clone <repo>
cd backend

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar .env
cp .env.example .env
# Editar .env con tu GROQ_API_KEY

# 5. Migrar
python manage.py migrate

# 6. Crear usuarios demo
python manage.py crear_usuarios_demo

# 7. Runserver
python manage.py runserver
```

---

### Docker Desarrollo

```bash
# 1. Configurar .env
cp .env.example .env

# 2. Build y run
docker-compose up --build

# Acceder a http://localhost:8000
```

---

### Docker Producción

```bash
# 1. Configurar .env para producción
cp .env.production.example .env
# Editar con valores reales

# 2. Build y run en background
docker-compose -f docker-compose.prod.yml up -d --build

# 3. Ver logs
docker-compose -f docker-compose.prod.yml logs -f

# 4. Verificar health
docker ps
```

---

## 9. COMANDOS DE GESTIÓN

### Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations
```

### Usuarios demo

```bash
python manage.py crear_usuarios_demo
```

**Crea:**
- 2021101234 / demo123 (Estudiante)
- 2022105678 / demo123 (Estudiante)
- 2019103456 / demo123 (Egresado)
- DOC001 / docente123 (Docente)

### Superusuario

```bash
python manage.py createsuperuser
```

Acceder a `/admin/` con credenciales

### Shell

```bash
python manage.py shell
```

```python
>>> from apps.usuarios.models import Usuario
>>> usuarios = Usuario.objects.all()
>>> print(usuarios)
```

### Tests

```bash
python manage.py test                    # Todos
python manage.py test apps.usuarios      # Solo usuarios
python manage.py test --verbosity=2      # Detallado
```

---

## 10. MONITOREO Y LOGS

### Ver logs de Docker

```bash
# Desarrollo
docker-compose logs -f web

# Producción
docker-compose -f docker-compose.prod.yml logs -f web
```

### Health checks

```bash
# Verificar estado de contenedores
docker ps

# Estado de health check
docker inspect --format='{{.State.Health.Status}}' untels-django-prod
```

---

## 11. BACKUP Y RESTORE

### Backup de PostgreSQL (producción)

```bash
docker exec untels-postgres-prod pg_dump -U untels_user untels_db > backup.sql
```

### Restore

```bash
docker exec -i untels-postgres-prod psql -U untels_user untels_db < backup.sql
```

### Backup de SQLite (desarrollo)

```bash
cp db.sqlite3 db.sqlite3.backup
```

---

## RESUMEN

| Componente | Archivo | Propósito |
|------------|---------|-----------|
| Settings Base | config/settings/base.py | Configuración común |
| Settings Dev | config/settings/development.py | DEBUG=True, SQLite |
| Settings Prod | config/settings/production.py | Seguridad, PostgreSQL |
| Docker Dev | docker-compose.yml | Desarrollo con hot reload |
| Docker Prod | docker-compose.prod.yml | Producción con Gunicorn |
| Dockerfile | Dockerfile | Imagen de la app |
| Dependencias | requirements.txt | 8 paquetes Python |
| Env Dev | .env.example | Variables de desarrollo |
| Env Prod | .env.production.example | Variables de producción |
| WSGI | config/wsgi.py | Punto de entrada WSGI |
| Script | run.sh | Menú interactivo |

---

**Esta es la CAPA DE INFRAESTRUCTURA completa.**

**Has completado el recorrido por las 4 capas del sistema.**

---

## ARQUITECTURA COMPLETA

```
┌─────────────────────────────────────────┐
│     CAPA PRESENTACIÓN (7 templates)     │
│         Bootstrap 5.3 + Django          │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│      CAPA NEGOCIO (7 vistas + 8 svc)    │
│    Views → Services → Models            │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│       CAPA DATOS (5 modelos)            │
│    PostgreSQL / SQLite                  │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│   CAPA INFRAESTRUCTURA (Docker)         │
│   Settings + Docker + Gunicorn          │
└─────────────────────────────────────────┘
```

**Sistema completo, bien separado en capas, listo para producción.**
