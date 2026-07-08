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

### 1. **Flujo Multi-Rol v2.1 Completo**

```
Estudiante → Secretaria → Presidente → Docente → IA → Docente → 
Presidente (3 decisiones) → Secretaria → Estudiante
```

#### Responsabilidades por Rol:

| Rol | Responsabilidades Principales | Estados que Gestiona |
|-----|------------------------------|----------------------|
| **🎓 Estudiante** | • Subir informe (PDF/DOCX)<br>• Ver estado en tiempo real<br>• Ver dictamen si es rechazado<br>• Reenviar versión corregida (solo última rechazada) | `enviado`, `rechazado_estudiante` |
| **📋 Secretaria** | • Derivar informes a escuelas<br>• Notificar aprobación final<br>• Notificar rechazo final<br>• Ver resultado de completados (aprobado/rechazado) | `pendiente_secretaria`, `aprobado_presidente`, `rechazado_presidente` |
| **👔 Presidente** | • Asignar docente revisor<br>• Revisar dictamen del docente<br>• **3 decisiones posibles:**<br>&nbsp;&nbsp;✅ Aprobar informe<br>&nbsp;&nbsp;❌ Rechazar informe<br>&nbsp;&nbsp;🔄 Devolver dictamen al docente | `pendiente_presidente`, `pendiente_aprobacion_presidente` |
| **👨‍🏫 Docente** | • Crear/gestionar bancos de observaciones<br>• Validar informe con IA<br>• Confirmar/descartar observaciones<br>• Generar dictamen estructurado<br>• Enviar dictamen al presidente | `pendiente_docente`, `validando_ia`, `revision_docente` |
| **🔧 Admin** | • Gestionar usuarios<br>• Gestionar escuelas<br>• Ver estadísticas globales | Todos los estados (lectura) |

#### Características Clave del Flujo:

- ✅ **11 estados** bien definidos con transiciones controladas por State Machine
- ✅ **Versionado automático**: Cada reenvío crea una nueva versión del informe (v1, v2, v3...)
- ✅ **Trazabilidad completa**: Cada transición registra fecha, hora y responsable
- ✅ **Notificaciones en tiempo real**: Cada actor recibe notificaciones de sus tareas pendientes
- ✅ **Validación con IA**: Integración con xAI Grok o Groq para generar observaciones automáticas
- ✅ **Banco personalizado**: Cada docente puede tener múltiples bancos y elegir cuál usar
- ✅ **3 decisiones del presidente**: Aprobar, rechazar o devolver al docente (novedad v2.1)

### 2. **Banco de Observaciones Personalizado (Novedad v2.1)**

#### Características del Sistema de Bancos:

Los docentes pueden:
- ✅ **Crear múltiples bancos** de observaciones (cada uno con criterios específicos)
- ✅ **Subir archivos** PDF/DOCX/TXT con criterios de evaluación
- ✅ **Activar/desactivar bancos** (solo uno activo a la vez)
- ✅ **Seleccionar banco específico** al momento de validar (o usar el activo)
- ✅ **Extracción automática de texto** del archivo subido
- ✅ **Contador de uso**: El sistema registra cuántas veces se usó cada banco
- ✅ **La IA usa el banco como "memoria"** contextual para generar observaciones coherentes

#### Ejemplo de Uso:

```
Docente crea:
  📁 Banco 1: "Criterios ISI 2024" (activo) - usado 15 veces
  📁 Banco 2: "Criterios estrictos" (inactivo) - usado 5 veces
  📁 Banco 3: "Criterios tesis" (inactivo) - usado 0 veces

Al validar un informe:
  → Modal pregunta: "¿Qué banco usar?"
  → Por defecto: "Criterios ISI 2024" (el activo)
  → Puede elegir: "Criterios estrictos" para casos especiales
```

#### Contenido Típico de un Banco:

```
El banco contiene:
  - Criterios de evaluación específicos
  - Errores comunes a detectar
  - Formato esperado de secciones
  - Estándares de citación
  - Reglamento de la escuela
  - Ejemplos de buenas prácticas
```

La IA lee el banco completo y lo usa como contexto para generar observaciones personalizadas según los criterios del docente.

### 3. **Validación Automática con IA**

#### APIs de IA Soportadas:

| API | Modelo | Velocidad | Costo | Detección |
|-----|--------|-----------|-------|-----------|
| **xAI Grok** | `grok-beta` | Rápido | Pago | API key empieza con `xai-` |
| **Groq** | `llama-3.3-70b-versatile` | Muy rápido | Gratis ⭐ | API key empieza con `gsk_` |
| **Fallback Local** | Regex básico | Instantáneo | Gratis | Si no hay API key válida |

#### Proceso de Validación:

1. **Docente hace clic** en "Validar con IA"
2. **Sistema extrae texto** del PDF/DOCX del informe
3. **Construye prompt** combinando:
   - Contenido del banco de observaciones
   - Contenido del informe del estudiante
   - Instrucciones para la IA
4. **Llama API de IA** (xAI Grok o Groq según API key)
5. **IA retorna JSON** con observaciones categorizadas:
   ```json
   {
     "observaciones": [
       {
         "seccion": "Introducción",
         "observacion": "No se plantea claramente el problema",
         "severidad": "critica",
         "ubicacion": "Página 2, párrafo 1"
       },
       ...
     ]
   }
   ```
6. **Sistema crea registros** de `ObservacionGenerada` en BD
7. **Docente revisa** cada observación:
   - ✅ **Confirmar**: La observación es válida
   - ❌ **Descartar**: La observación no aplica
   - ✏️ **Agregar comentario**: Comentario adicional del docente

#### Observaciones Categorizadas por Severidad:

| Severidad | Emoji | Color | Significado |
|-----------|-------|-------|-------------|
| **Crítica** | 🔴 | Rojo | Error grave que impide aprobación |
| **Importante** | 🟠 | Naranja | Error significativo a corregir |
| **Menor** | 🟡 | Amarillo | Detalle a mejorar |
| **Sugerencia** | 💡 | Azul | Recomendación opcional |

#### Características de la Validación:

- ✅ **Detección automática de API**: El sistema detecta qué API usar según el prefijo de la key
- ✅ **Fallback automático**: Si la API falla (sin créditos, timeout), usa validación local
- ✅ **Progreso visual**: Barra de progreso animada con mensajes ("Conectando...", "Analizando...")
- ✅ **Timeout de 60 segundos**: Si la IA no responde, activa fallback
- ✅ **Manejo de errores**: Captura errores de API y muestra mensaje al usuario
- ✅ **Cache opcional**: Puede guardar respuestas de IA para evitar validaciones repetidas (futuro)

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

## 📊 Estadísticas del Proyecto v2.1

### Código

```
📁 Archivos Python:     150+
📄 Templates HTML:      60+
🎨 Líneas CSS:          3,500+
⚡ Archivos JavaScript: 10+
💻 Líneas de Código:    ~20,000
📝 Líneas de Comentarios: ~5,000
```

### Arquitectura

```
🗄️ Modelos de BD:       8 principales
   - Usuario (5 tipos)
   - Informe (con versionado)
   - ObservacionGenerada
   - BancoObservacionesDocente
   - Escuela
   - Notificacion
   - Reglamento
   - Archivos de sesión

🔄 Estados del Flujo:   11 estados
   - enviado
   - pendiente_secretaria
   - pendiente_presidente
   - pendiente_docente
   - validando_ia
   - revision_docente
   - pendiente_aprobacion_presidente
   - aprobado_presidente
   - rechazado_presidente
   - aprobado_final ✅
   - rechazado_estudiante ❌

👥 Roles de Usuario:    5 roles
   - Estudiante
   - Docente
   - Presidente de Escuela
   - Secretaria Académica
   - Administrador

🧩 Patrones de Diseño:  8 patrones implementados
   1. Repository Pattern
   2. Service Layer Pattern
   3. State Machine Pattern
   4. Strategy Pattern
   5. Template Method Pattern
   6. Facade Pattern
   7. Observer Pattern
   8. Decorator Pattern
```

### Funcionalidades

```
📋 Vistas por Rol:      20+ vistas
🔔 Tipos de Notificación: 8 tipos
📊 Dashboards:          5 dashboards (uno por rol)
📁 Upload de Archivos:  PDF, DOCX, TXT
🤖 APIs de IA:          2 (xAI Grok, Groq) + fallback local
🌐 Endpoints HTTP:      40+ endpoints
🔐 Sistema de Sesiones: Custom (sin django.contrib.auth)
```

### Testing

```
✅ Tests Unitarios:     Implementados
✅ Tests de Integración: Implementados
✅ Coverage:            >80%
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
