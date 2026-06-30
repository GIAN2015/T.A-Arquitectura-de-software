# Changelog

Registro de cambios del Sistema de Validación de Informes - UNTELS

## [2.0.0] - 2026-06-16

### Añadido

#### Autenticación y Usuarios
- Sistema de autenticación con contraseñas encriptadas
- Modelo de Usuario mejorado con soporte para contraseñas
- Vista de registro de usuarios
- Vista de login con soporte para contraseñas
- Vista de logout
- Servicio de autenticación con hash de contraseñas
- Compatibilidad con modo legacy (sin contraseña)
- Comando de gestión para crear usuarios de demostración
- Tipo de usuario "docente" agregado

#### Gestión de Informes
- Vista de historial de informes para estudiantes
- Panel de docentes para revisar todos los informes
- Indicadores de estado visual en las vistas
- Contador de observaciones por informe
- Enlaces de navegación mejorados entre vistas

#### Configuración y Deployment
- Separación de configuraciones: base, development, production
- Configuración de seguridad para producción (SSL, HSTS, etc.)
- Configuración completa de Whitenoise para archivos estáticos
- Docker Compose para producción (docker-compose.prod.yml)
- Dockerfile optimizado con health checks
- Script de ayuda (run.sh) para desarrollo
- Variables de entorno organizadas (.env.example, .env.production.example)
- .gitignore actualizado y completo

#### Testing
- Tests unitarios para modelo Usuario
- Tests unitarios para modelo Informe
- Tests de integración para vistas (login, registro, upload, etc.)
- Tests para servicios de autenticación
- 18 tests con 100% de éxito

#### Documentación
- README.md completo con:
  - Instrucciones de instalación (local y Docker)
  - Guía de uso completa
  - Documentación de API
  - Estructura del proyecto
  - Guía de deployment
  - Usuarios de demostración
- CHANGELOG.md con registro de cambios
- Documentación de seguridad
- Ejemplos de configuración

### Mejorado

- Base de datos: campo `codigo` ahora es único
- Seguridad: contraseñas encriptadas con Django's hashers
- UX: navegación mejorada con enlaces entre vistas
- Templates: diseño mejorado con badges de estado
- Error handling: mensajes de error más descriptivos
- Performance: queries optimizadas con select_related
- Docker: configuración mejorada con health checks

### Migrado

- Migración 0002 para usuarios: campo password y código único
- Configuración de settings modularizada

### Características Técnicas

- Django 5.0.6
- Python 3.12
- Bootstrap 5.3
- PostgreSQL support (producción)
- SQLite (desarrollo)
- Groq API con LLaMA 3.3 70B
- Gunicorn para WSGI
- Whitenoise para archivos estáticos
- Docker & Docker Compose

## [1.0.0] - 2024-XX-XX

### Inicial

- MVP básico con validación de informes
- Integración con IA (Ollama → Gemini → Groq)
- Flujo de 3 estados (enviado → en_revision → completado)
- Modelos básicos: Usuario, Informe, Reglamento, Observación
- Templates básicos de login y upload
- Docker compose con PostgreSQL
