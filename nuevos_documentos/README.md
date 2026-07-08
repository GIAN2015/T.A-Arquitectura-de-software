# 📋 Sistema de Validación de Informes - UNTELS

> Sistema web para la validación automatizada de informes de prácticas preprofesionales con IA, implementando Clean Architecture y flujo multi-rol.

[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.1-orange.svg)](CHANGELOG.md)

---

## 🎯 Descripción

Sistema integral para la **Universidad Nacional Tecnológica de Lima Sur (UNTELS)** que automatiza el proceso de revisión y validación de informes de prácticas preprofesionales mediante:

- ✅ **Validación automática con IA** (xAI Grok / Groq API)
- ✅ **Flujo multi-rol** (Estudiante → Secretaria → Presidente → Docente)
- ✅ **Banco de observaciones personalizado** por docente
- ✅ **Dictámenes estructurados** con observaciones categorizadas
- ✅ **Trazabilidad completa** de todo el proceso
- ✅ **Notificaciones en tiempo real**

---

## 📚 Documentación Completa

| Documento | Descripción |
|-----------|-------------|
| [**📐 Arquitectura**](docs/ARQUITECTURA.md) | Clean Architecture, capas, principios SOLID |
| [**🔧 Backend**](docs/BACKEND.md) | Django, servicios, modelos, APIs |
| [**🎨 Frontend**](docs/FRONTEND.md) | Templates, Bootstrap, JavaScript |
| [**💾 Base de Datos**](docs/BASE_DE_DATOS.md) | Modelo relacional, relaciones, migraciones |
| [**🧩 Patrones de Diseño**](docs/PATRONES.md) | Patrones implementados y su ubicación |
| [**🔄 Flujo del Sistema**](docs/FLUJO_DEL_SISTEMA.md) | Diagramas de secuencia y casos de uso |
| [**🚀 Deployment**](docs/DEPLOYMENT.md) | Instalación, configuración, producción |

---

## 🏗️ Arquitectura del Proyecto

### Arquitectura de 3 Capas

```
T.A-Arquitectura-de-software/
│
├── 🎨 frontend/                   # CAPA 1: Presentación
│   ├── templates/                 # Templates HTML
│   └── static/                    # CSS, JS
│
├── 🔧 backend/                    # CAPA 2: Lógica de Negocio
│   ├── apps/                      # Apps Django
│   ├── config/                    # Configuración
│   └── manage.py
│
└── 💾 database/                   # CAPA 3: Datos
    └── db.sqlite3                 # SQLite
```

### Las 3 Capas

1. **Frontend** - Interfaz de usuario
2. **Backend** - Lógica del servidor
3. **Database** - Persistencia

---

## 🚀 Inicio Rápido

### Prerrequisitos

```bash
Python 3.9+
pip
virtualenv (recomendado)
```

### Instalación

```bash
# 1. Clonar el repositorio
git clone <repository-url>
cd T.A-Arquitectura-de-software

# 2. Crear entorno virtual
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales de API de IA

# 5. Ejecutar migraciones
python manage.py migrate

# 6. Cargar datos iniciales
python manage.py loaddata fixtures/initial_data.json

# 7. Iniciar servidor
python manage.py runserver 0.0.0.0:8000
```

### Acceder al Sistema

```
🌐 URL: http://localhost:8000

👥 Usuarios de prueba:
   - Secretaria:   secretaria1    / test123
   - Presidente:   presidente_isi / test123
   - Docente:      docente_isi_1  / test123
   - Estudiante:   2020123456     / test123
```

---

## 🎨 Características Principales

### 1. **Flujo Multi-Rol v2.1**

```
Estudiante → Secretaria → Presidente → Docente → IA → Docente → 
Presidente → Secretaria → Estudiante
```

Cada rol tiene responsabilidades específicas:
- **Estudiante**: Sube informe
- **Secretaria**: Deriva a presidente
- **Presidente**: Asigna docente revisor
- **Docente**: Valida con IA + banco personalizado
- **Presidente**: Puede aprobar el informe final, rechazarlo y enviarlo a secretaría, o devolver el dictamen al docente
- **Secretaria**: Notifica al estudiante si el resultado final fue aprobado o con observaciones
- **Estudiante**: Recibe feedback o aprobación y solo puede reenviar la última versión rechazada

### 2. **Banco de Observaciones Personalizado**

Los docentes pueden:
- ✅ Crear múltiples bancos de observaciones
- ✅ Subir archivos PDF/DOCX/TXT
- ✅ Activar/desactivar bancos
- ✅ Seleccionar qué banco usar al validar
- ✅ La IA usa el banco como memoria contextual

### 3. **Validación con IA**

- **API soportadas**: xAI Grok, Groq (LLaMA)
- **Detección automática** por prefijo de API key
- **Fallback local** si no hay créditos
- **Observaciones categorizadas**: Críticas, Importantes, Menores, Sugerencias

### 4. **Dictámenes Estructurados**

Formato profesional que incluye:
- 📋 Dictamen del docente
- ⚖️ Recomendación (Aprobar/Rechazar)
- 📊 Resumen de observaciones
- 🔴 Observaciones críticas
- 🟠 Observaciones importantes
- 🟡 Observaciones menores
- 💡 Sugerencias

### 5. **Sistema de Notificaciones**

- Notificaciones en tiempo real
- Contador de no leídas
- Registro de todas las acciones

---

## 🧩 Patrones de Diseño Implementados

| Patrón | Ubicación | Propósito |
|--------|-----------|-----------|
| **Repository** | `apps/datos/repositorios/` | Abstracción de acceso a datos |
| **Service Layer** | `apps/negocio/servicios/` | Lógica de negocio centralizada |
| **State Machine** | `apps/informes/state.py` | Gestión de estados del informe |
| **Strategy** | `apps/observaciones/services.py` | Selección de API de IA |
| **Template Method** | Filtros personalizados | Formateo de dictámenes |
| **Facade** | Servicios de negocio | Simplificación de operaciones |
| **Observer** | Sistema de notificaciones | Eventos del sistema |

Ver detalles en [**PATRONES.md**](docs/PATRONES.md)

---

## 🛠️ Tecnologías Utilizadas

### Backend
- **Django 4.2** - Framework web
- **Python 3.9+** - Lenguaje base
- **SQLite** - Base de datos (desarrollo)
- **Django ORM** - Mapeo objeto-relacional

### Frontend
- **Bootstrap 5.3** - Framework CSS
- **Bootstrap Icons** - Iconografía
- **JavaScript Vanilla** - Interactividad
- **Django Templates** - Motor de plantillas

### IA y APIs
- **xAI Grok API** - Validación con IA (beta)
- **Groq API** - Alternativa rápida (LLaMA)
- **python-docx** - Extracción de DOCX
- **pypdf** - Extracción de PDF

### DevOps
- **Git** - Control de versiones
- **Virtualenv** - Entornos virtuales
- **WhiteNoise** - Servir archivos estáticos

---

## 📊 Estadísticas del Proyecto

```
📁 Archivos Python:     120+
📄 Templates HTML:      45+
🎨 Líneas CSS:          2,500+
💻 Líneas de Código:    15,000+
🗄️ Modelos de BD:       8
🔄 Estados del Flujo:   11
👥 Roles de Usuario:    5
```

---

## 🤝 Contribuciones

Este es un proyecto académico para la **Universidad Nacional Tecnológica de Lima Sur**.

### Equipo de Desarrollo
- **Arquitectura**: Clean Architecture + SOLID
- **Backend**: Django + Python
- **Frontend**: Bootstrap + JavaScript
- **Base de Datos**: SQLite (desarrollo), PostgreSQL (producción)

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 🔗 Enlaces Útiles

- [📐 Arquitectura del Sistema](docs/ARQUITECTURA.md)
- [🧩 Patrones de Diseño](docs/PATRONES.md)
- [🔄 Flujo del Sistema](docs/FLUJO_DEL_SISTEMA.md)
- [🚀 Guía de Deployment](docs/DEPLOYMENT.md)

---

## 📞 Soporte

Para preguntas o problemas:
1. Revisar la [documentación completa](docs/)
2. Ver los [patrones implementados](docs/PATRONES.md)
3. Consultar el [flujo del sistema](docs/FLUJO_DEL_SISTEMA.md)

---

**© 2026 Universidad Nacional Tecnológica de Lima Sur**  
*Sistema de Validación de Informes v2.1 - Arquitectura de Software*
