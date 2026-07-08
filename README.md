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
| [**📐 Arquitectura**](nuevos_documentos/ARQUITECTURA.md) | Arquitectura de 3 Capas explicada |
| [**🔧 Backend**](nuevos_documentos/BACKEND.md) | Django, servicios, modelos, APIs |
| [**🎨 Frontend**](nuevos_documentos/FRONTEND.md) | Templates, Bootstrap, JavaScript |
| [**💾 Base de Datos**](nuevos_documentos/BASE_DE_DATOS.md) | Modelo relacional, relaciones, migraciones |
| [**🧩 Patrones de Diseño**](nuevos_documentos/PATRONES.md) | 8 patrones implementados con código |
| [**🔄 Flujo del Sistema**](nuevos_documentos/FLUJO_DEL_SISTEMA.md) | Diagramas de secuencia y casos de uso |
| [**🚀 Deployment**](nuevos_documentos/DEPLOYMENT.md) | Instalación, configuración, producción |
| [**📊 Resumen Ejecutivo**](nuevos_documentos/RESUMEN_EJECUTIVO.md) | Presentación del proyecto |
| [**📖 Índice**](nuevos_documentos/INDEX.md) | Navegación de documentación |

---

## 🏗️ Arquitectura del Proyecto

### Arquitectura de 3 Capas (Three-Tier Architecture)

```
T.A-Arquitectura-de-software/
│
├── 🎨 frontend/                   # CAPA 1: PRESENTACIÓN
│   ├── templates/                 # Templates HTML por rol
│   │   ├── estudiante/
│   │   ├── docente/
│   │   ├── presidente/
│   │   └── secretaria/
│   └── static/                    # CSS, JS, imágenes
│
├── 🔧 backend/                    # CAPA 2: LÓGICA DE NEGOCIO
│   ├── apps/                      # Apps Django organizadas:
│   │   ├── presentacion/          #   Vistas HTTP por rol
│   │   ├── negocio/               #   Servicios con lógica
│   │   ├── datos/                 #   Repositorios (acceso a BD)
│   │   ├── usuarios/              #   Gestión de usuarios
│   │   ├── informes/              #   Gestión de informes + Estados
│   │   ├── observaciones/         #   IA + Banco de observaciones
│   │   ├── escuelas/              #   Escuelas profesionales
│   │   ├── notificaciones/        #   Sistema de notificaciones
│   │   └── core/                  #   Utilidades compartidas
│   ├── config/                    # Configuración Django
│   └── manage.py                  # CLI Django
│
└── 💾 database/                   # CAPA 3: DATOS
    └── db.sqlite3                 # Base de datos SQLite
```

### Las 3 Capas

1. **🎨 Frontend** - Interfaz de usuario (Templates, Bootstrap, JS)
2. **🔧 Backend** - Lógica del servidor (Django, Python)
3. **💾 Database** - Persistencia de datos (SQLite/PostgreSQL)

**Ver documentación completa**: [ARQUITECTURA.md](nuevos_documentos/ARQUITECTURA.md)

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
- **Presidente**: Aprueba/rechaza dictamen
- **Secretaria**: Notifica resultado final
- **Estudiante**: Recibe feedback o aprobación

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
| **Repository** | `backend/apps/datos/repositorios/` | Abstracción de acceso a datos |
| **Service Layer** | `backend/apps/negocio/servicios/` | Lógica de negocio centralizada |
| **State Machine** | `backend/apps/informes/state.py` | Gestión de 11 estados del informe |
| **Strategy** | `backend/apps/observaciones/services.py` | Selección de API de IA |
| **Template Method** | `backend/apps/core/templatetags/` | Formateo de dictámenes |
| **Facade** | Servicios de negocio | Simplificación de operaciones |
| **Observer** | `backend/apps/notificaciones/` | Sistema de eventos |
| **Decorator** | `backend/apps/core/decorators.py` | Autorización por rol |

**Total**: 8 patrones de diseño profesionales

Ver detalles completos en [**PATRONES.md**](nuevos_documentos/PATRONES.md)

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

- [📐 Arquitectura del Sistema](nuevos_documentos/ARQUITECTURA.md) - Clean Architecture explicada
- [🎯 Capa de Dominio](nuevos_documentos/CAPA_DOMINIO.md) - Entidades y State Machine
- [🧩 Patrones de Diseño](nuevos_documentos/PATRONES.md) - 8 patrones con código
- [🔄 Flujo del Sistema](nuevos_documentos/FLUJO_DEL_SISTEMA.md) - Diagramas y casos de uso
- [🚀 Guía de Deployment](nuevos_documentos/DEPLOYMENT.md) - Instalación paso a paso
- [📖 Índice Completo](nuevos_documentos/INDEX.md) - Navegación de toda la documentación

---

## 📞 Soporte

Para preguntas o problemas:
1. Revisar la [documentación completa](docs/)
2. Ver los [patrones implementados](docs/PATRONES.md)
3. Consultar el [flujo del sistema](docs/FLUJO_DEL_SISTEMA.md)

---

**© 2026 Universidad Nacional Tecnológica de Lima Sur**  
*Sistema de Validación de Informes v2.1 - Arquitectura de Software*
