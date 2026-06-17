# Sistema de Validación de Informes de Prácticas - UNTELS

Sistema web para la validación automática de informes de prácticas preprofesionales de la Universidad Nacional Tecnológica de Lima Sur (UNTELS), utilizando inteligencia artificial.

## Características

- **Autenticación segura** con contraseñas encriptadas
- **Validación automática** de informes .docx usando IA (Groq API - LLaMA 3.3 70B)
- **Flujo de estados**: Enviado → En Revisión → Completado
- **Panel de estudiantes** para subir informes y ver historial
- **Panel de docentes** para revisar todos los informes
- **Sistema de observaciones** automáticas basadas en reglamento
- **Arquitectura modular** con Django

## Tecnologías

- **Backend**: Django 5.0.6
- **Base de datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **IA**: Groq API (LLaMA 3.3 70B - gratuito)
- **Frontend**: Bootstrap 5.3
- **Procesamiento de documentos**: python-docx
- **Servidor**: Gunicorn + Whitenoise
- **Contenedores**: Docker & Docker Compose

## Estructura del Proyecto

```
proyecto_untels/
├── apps/
│   ├── core/           # Vistas principales y URLs
│   ├── usuarios/       # Modelo de usuarios y autenticación
│   ├── informes/       # Modelo de informes y procesamiento
│   ├── reglamento/     # Gestión del reglamento
│   └── observaciones/  # IA y generación de observaciones
├── config/
│   ├── settings/
│   │   ├── base.py         # Configuración base
│   │   ├── development.py  # Configuración de desarrollo
│   │   └── production.py   # Configuración de producción
│   ├── urls.py
│   └── wsgi.py
├── templates/          # Templates HTML
├── static/            # Archivos estáticos
├── manage.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## Instalación y Configuración

### Opción 1: Local (sin Docker)

#### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd T.A-Arquitectura-de-software/proyecto_untels
```

#### 2. Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

#### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

#### 4. Configurar variables de entorno

```bash
cp .env.example .env
```

Editar `.env` y configurar:

```env
DJANGO_SECRET_KEY=tu-clave-secreta-aqui
DJANGO_SETTINGS_MODULE=config.settings.development
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
GROQ_API_KEY=tu-api-key-de-groq
```

Para obtener una API key de Groq gratuita: https://console.groq.com/

#### 5. Aplicar migraciones

```bash
python manage.py migrate
```

#### 6. Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

#### 7. Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

Acceder a: http://localhost:8000

### Opción 2: Docker

#### 1. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus valores
```

#### 2. Construir y ejecutar contenedores

```bash
docker-compose up --build
```

Acceder a: http://localhost:8000

## Usuarios de Demostración

Para facilitar las pruebas, puedes crear usuarios de demostración ejecutando:

```bash
python manage.py crear_usuarios_demo
```

Esto creará los siguientes usuarios:

| Código | Nombre | Tipo | Contraseña |
|--------|--------|------|------------|
| 2021101234 | Juan Carlos Pérez García | Estudiante | demo123 |
| 2022105678 | María Elena Rodríguez López | Estudiante | demo123 |
| 2019103456 | Pedro Antonio Sánchez Díaz | Egresado | demo123 |
| DOC001 | Prof. Roberto García Martínez | Docente | docente123 |

## Uso

### Registro de Usuario

1. Ir a `/registro/`
2. Llenar el formulario:
   - Código universitario (ej: 2021101234)
   - Nombre completo
   - Contraseña (mínimo 6 caracteres)
   - Tipo de usuario: Estudiante / Egresado / Docente
3. Hacer clic en "Registrarse"

### Login

1. Ir a `/` (página principal)
2. Ingresar código y contraseña
3. Hacer clic en "Iniciar Sesión"

**Nota**: El sistema soporta modo legacy (sin contraseña) para usuarios existentes.

### Subir Informe (Estudiante/Egresado)

1. Después de login, se redirige a `/upload/`
2. Seleccionar archivo .docx
3. Hacer clic en "Validar Informe"
4. El sistema procesará el informe automáticamente
5. Se mostrará la página de resultados con las observaciones

### Ver Historial

1. Ir a `/historial/`
2. Ver todos tus informes enviados con:
   - Nombre del archivo
   - Fecha de envío
   - Estado actual
   - Número de observaciones
3. Hacer clic en "Ver Resultado" para ver detalles

### Panel Docente

1. Iniciar sesión como docente
2. Ir a `/panel-docente/`
3. Ver todos los informes de todos los estudiantes
4. Revisar observaciones y estados

## Testing

### Ejecutar todos los tests

```bash
python manage.py test
```

### Ejecutar tests de una app específica

```bash
python manage.py test apps.usuarios
python manage.py test apps.informes
python manage.py test apps.core
```

### Tests con cobertura

```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Genera reporte HTML
```

## Despliegue en Producción

### 1. Configurar variables de entorno para producción

```env
DJANGO_SECRET_KEY=clave-secreta-muy-fuerte
DJANGO_SETTINGS_MODULE=config.settings.production
DEBUG=False
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
DATABASE_URL=postgresql://user:password@host:5432/dbname
GROQ_API_KEY=tu-api-key-de-groq
```

### 2. Aplicar migraciones

```bash
python manage.py migrate --settings=config.settings.production
```

### 3. Recopilar archivos estáticos

```bash
python manage.py collectstatic --noinput --settings=config.settings.production
```

### 4. Ejecutar con Gunicorn

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Despliegue con Docker

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## API de IA (Groq)

El sistema utiliza Groq API con el modelo **LLaMA 3.3 70B** (gratuito) para:

- Analizar el contenido del informe
- Comparar con el reglamento de prácticas
- Generar observaciones específicas por sección
- Identificar ubicación de errores

Ver `apps/observaciones/services.py:validar_informe()` para más detalles.

## Estructura de la Base de Datos

### Usuario
- codigo (único)
- nombre
- tipo_usuario (estudiante/egresado/docente)
- password (encriptado)

### Informe
- usuario (FK)
- nombre_archivo
- contenido (texto extraído del .docx)
- fecha_registro
- estado (enviado/en_revision/completado)

### ObservacionGenerada
- informe (FK)
- seccion
- observacion
- ubicacion_error

### Reglamento
- contenido (texto del reglamento)

## Seguridad

- Contraseñas encriptadas con Django's password hashers
- CSRF protection habilitado
- SQL injection protection (Django ORM)
- XSS protection
- Configuración de seguridad para producción (HTTPS, HSTS, etc.)

## Contribuir

1. Fork el proyecto
2. Crear una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Licencia

Este proyecto es parte de un trabajo académico para UNTELS.

## Soporte

Para soporte o preguntas, contactar al equipo de desarrollo.

---

Desarrollado para la Universidad Nacional Tecnológica de Lima Sur (UNTELS)
