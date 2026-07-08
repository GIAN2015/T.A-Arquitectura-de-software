# 🚀 Deployment - Sistema de Validación UNTELS

> Guía completa de instalación, configuración y despliegue

---

## 📋 Tabla de Contenidos

1. [Requisitos del Sistema](#requisitos-del-sistema)
2. [Instalación Local](#instalación-local)
3. [Configuración](#configuración)
4. [Deployment en Producción](#deployment-en-producción)
5. [Mantenimiento](#mantenimiento)
6. [Troubleshooting](#troubleshooting)

---

## 💻 Requisitos del Sistema

### Desarrollo

```
✅ Python 3.9 o superior
✅ pip (gestor de paquetes Python)
✅ virtualenv (recomendado)
✅ Git (control de versiones)
✅ 500 MB espacio en disco
✅ 2 GB RAM mínimo
```

### Producción

```
✅ Python 3.9+
✅ PostgreSQL 12+ (recomendado)
✅ Nginx (servidor web)
✅ Gunicorn (WSGI server)
✅ Systemd (gestor de servicios)
✅ 2 GB RAM mínimo
✅ 5 GB espacio en disco
✅ SSL/TLS certificado
```

---

## 🔧 Instalación Local

### Paso 1: Clonar Repositorio

```bash
# Clonar el proyecto
git clone https://github.com/tu-usuario/T.A-Arquitectura-de-software.git
cd T.A-Arquitectura-de-software
```

### Paso 2: Crear Entorno Virtual

```bash
# Ir al directorio backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En macOS/Linux:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

### Paso 3: Instalar Dependencias

```bash
# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt
```

**Archivo `requirements.txt`**:
```
Django==4.2.11
python-dotenv==1.0.0
python-docx==1.1.0
pypdf==4.0.1
requests==2.31.0
whitenoise==6.6.0
Pillow==10.2.0
```

### Paso 4: Configurar Variables de Entorno

```bash
# Crear archivo .env
cp .env.example .env

# Editar .env con tus credenciales
nano .env
```

**Archivo `.env`**:
```bash
# Django
SECRET_KEY=tu-clave-secreta-aqui-cambiar-en-produccion
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de Datos
DATABASE_PATH=../database/db.sqlite3

# API de IA (elegir una)
# Opción 1: xAI Grok (recomendado)
GROQ_API_KEY=xai-tu-api-key-aqui

# Opción 2: Groq (gratis, rápido)
# GROQ_API_KEY=gsk_tu-api-key-aqui

# Media
MEDIA_ROOT=media/
MEDIA_URL=/media/

# Email (opcional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Paso 5: Crear Base de Datos

```bash
# Crear directorio para BD
mkdir -p ../database

# Ejecutar migraciones
python manage.py makemigrations
python manage.py migrate
```

### Paso 6: Cargar Datos Iniciales

```bash
# Cargar usuarios, escuelas, datos de prueba
python manage.py loaddata fixtures/initial_data.json
```

**Usuarios de prueba**:
```
Secretaria:   secretaria1    / test123
Presidente:   presidente_isi / test123
Docente:      docente_isi_1  / test123
Estudiante:   2020123456     / test123
Admin:        admin          / test123
```

### Paso 7: Iniciar Servidor de Desarrollo

```bash
# Ejecutar servidor
python manage.py runserver 0.0.0.0:8000

# Abrir navegador
# http://localhost:8000
```

---

## ⚙️ Configuración

### Estructura de Configuración

```
config/
├── settings/
│   ├── base.py          # Configuración base
│   ├── development.py   # Desarrollo (DEBUG=True)
│   └── production.py    # Producción (DEBUG=False)
├── urls.py
└── wsgi.py
```

### Configuración Base (`config/settings/base.py`)

```python
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'changeme')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Apps del proyecto
    'apps.core',
    'apps.usuarios',
    'apps.informes',
    'apps.observaciones',
    'apps.escuelas',
    'apps.notificaciones',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Servir estáticos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR.parent / 'database' / 'db.sqlite3',
    }
}

# Archivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR.parent / 'frontend' / 'static']

# WhiteNoise para servir estáticos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.parent / 'frontend' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Sesiones
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400  # 24 horas
SESSION_SAVE_EVERY_REQUEST = True
```

### Configuración de Producción (`config/settings/production.py`)

```python
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['tu-dominio.com', 'www.tu-dominio.com']

# PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'untels_informes'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Seguridad
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

---

## 🌐 Deployment en Producción

### Opción 1: VPS con Nginx + Gunicorn

#### 1. Preparar Servidor

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install python3-pip python3-venv nginx postgresql -y

# Instalar Gunicorn
pip install gunicorn
```

#### 2. Configurar PostgreSQL

```bash
# Entrar a PostgreSQL
sudo -u postgres psql

# Crear base de datos y usuario
CREATE DATABASE untels_informes;
CREATE USER untels_user WITH PASSWORD 'password-seguro';
ALTER ROLE untels_user SET client_encoding TO 'utf8';
ALTER ROLE untels_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE untels_user SET timezone TO 'America/Lima';
GRANT ALL PRIVILEGES ON DATABASE untels_informes TO untels_user;
\q
```

#### 3. Configurar Gunicorn

**Archivo**: `/etc/systemd/system/untels.service`

```ini
[Unit]
Description=UNTELS Informes Gunicorn Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/T.A-Arquitectura-de-software/backend
Environment="PATH=/var/www/T.A-Arquitectura-de-software/backend/venv/bin"
ExecStart=/var/www/T.A-Arquitectura-de-software/backend/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/var/www/T.A-Arquitectura-de-software/backend/untels.sock \
    config.wsgi:application

[Install]
WantedBy=multi-user.target
```

#### 4. Configurar Nginx

**Archivo**: `/etc/nginx/sites-available/untels`

```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /var/www/T.A-Arquitectura-de-software/backend/staticfiles/;
    }
    
    location /media/ {
        alias /var/www/T.A-Arquitectura-de-software/backend/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/T.A-Arquitectura-de-software/backend/untels.sock;
    }
}
```

#### 5. Habilitar Servicios

```bash
# Habilitar sitio Nginx
sudo ln -s /etc/nginx/sites-available/untels /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx

# Habilitar Gunicorn
sudo systemctl start untels
sudo systemctl enable untels

# Ver logs
sudo journalctl -u untels -f
```

#### 6. Configurar SSL (Let's Encrypt)

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtener certificado
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com

# Auto-renovación
sudo systemctl enable certbot.timer
```

### Opción 2: Docker

**Archivo**: `Dockerfile`

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar proyecto
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY database/ ./database/

WORKDIR /app/backend

# Collectstatic
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
```

**Archivo**: `docker-compose.yml`

```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: untels_informes
      POSTGRES_USER: untels_user
      POSTGRES_PASSWORD: password-seguro
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - ./backend:/app/backend
      - ./media:/app/backend/media
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DEBUG=False
      - DATABASE_URL=postgresql://untels_user:password-seguro@db:5432/untels_informes

volumes:
  postgres_data:
```

**Ejecutar**:
```bash
docker-compose up -d
```

---

## 🔧 Mantenimiento

### Backups de Base de Datos

```bash
# SQLite
cp database/db.sqlite3 "backups/db_$(date +%Y%m%d_%H%M%S).sqlite3"

# PostgreSQL
pg_dump -U untels_user untels_informes > "backup_$(date +%Y%m%d).sql"
```

### Actualizar Código

```bash
# En el servidor
cd /var/www/T.A-Arquitectura-de-software
git pull origin main

# Activar entorno
source backend/venv/bin/activate

# Instalar nuevas dependencias
pip install -r backend/requirements.txt

# Migrar BD
python backend/manage.py migrate

# Collectstatic
python backend/manage.py collectstatic --noinput

# Reiniciar servicio
sudo systemctl restart untels
```

### Logs

```bash
# Logs de Gunicorn
sudo journalctl -u untels -n 100 -f

# Logs de Nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Logs de Django (si está configurado)
tail -f backend/logs/django.log
```

---

## 🔍 Troubleshooting

### Problema: Error 502 Bad Gateway

**Causa**: Gunicorn no está corriendo

**Solución**:
```bash
sudo systemctl status untels
sudo systemctl restart untels
sudo journalctl -u untels -n 50
```

### Problema: Static files no se cargan

**Causa**: No se ejecutó collectstatic

**Solución**:
```bash
python manage.py collectstatic --noinput
sudo systemctl restart nginx
```

### Problema: IA no funciona (400 error)

**Causa**: API key inválida o sin créditos

**Solución**:
```bash
# Verificar .env
cat backend/.env | grep GROQ_API_KEY

# Probar API
curl -X POST https://api.x.ai/v1/chat/completions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"grok-beta","messages":[{"role":"user","content":"test"}]}'
```

**Fallback**: Sistema usa validación local automáticamente

### Problema: Permisos de archivos

**Solución**:
```bash
# Dar permisos correctos
sudo chown -R www-data:www-data /var/www/T.A-Arquitectura-de-software
sudo chmod -R 755 /var/www/T.A-Arquitectura-de-software
sudo chmod -R 775 /var/www/T.A-Arquitectura-de-software/backend/media
```

---

## 📊 Checklist de Deployment

### Antes de Producción

- [ ] Cambiar `SECRET_KEY` en `.env`
- [ ] Configurar `DEBUG=False`
- [ ] Configurar `ALLOWED_HOSTS`
- [ ] Migrar a PostgreSQL
- [ ] Configurar SSL/TLS
- [ ] Configurar backups automáticos
- [ ] Probar todas las funcionalidades
- [ ] Configurar monitoreo
- [ ] Documentar credenciales
- [ ] Configurar firewall

### Post-Deployment

- [ ] Verificar SSL funciona
- [ ] Probar login de todos los roles
- [ ] Probar subida de archivos
- [ ] Probar validación con IA
- [ ] Verificar notificaciones
- [ ] Probar flujo completo
- [ ] Verificar logs
- [ ] Configurar monitoreo de errores

---

## ✅ Conclusión

El sistema puede desplegarse en:
- ✅ **Desarrollo**: SQLite + runserver
- ✅ **Producción VPS**: PostgreSQL + Nginx + Gunicorn
- ✅ **Producción Docker**: Docker Compose
- ✅ **Cloud**: AWS, Google Cloud, Azure, DigitalOcean

**Recomendado para UNTELS**:
- VPS con Ubuntu 22.04
- PostgreSQL
- Nginx + Gunicorn
- Let's Encrypt SSL
- Backups diarios

---

**Ver también**: [README](../README.md), [Backend](BACKEND.md), [Arquitectura](ARQUITECTURA.md)
