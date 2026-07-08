# 📐 Arquitectura del Sistema - UNTELS

> Sistema de Validación de Informes con Arquitectura de 3 Capas

---

## 📋 Tabla de Contenidos

1. [Definición de la Arquitectura](#definición-de-la-arquitectura)
2. [Las 3 Capas del Sistema](#las-3-capas-del-sistema)
3. [Organización Interna del Backend](#organización-interna-del-backend)
4. [Principios SOLID](#principios-solid)
5. [Flujo de Datos](#flujo-de-datos)

---

## 🎯 Definición de la Arquitectura

### Tipo de Arquitectura

**Arquitectura de 3 Capas (Three-Tier Architecture)**

Esta es una arquitectura clásica y probada que separa el sistema en 3 capas independientes:

1. **Capa de Presentación** (Frontend)
2. **Capa de Lógica de Negocio** (Backend)  
3. **Capa de Datos** (Database)

### ¿Por qué 3 Capas?

✅ **Separación clara de responsabilidades**  
✅ **Fácil de mantener y escalar**  
✅ **Cada capa puede desarrollarse independientemente**  
✅ **Estándar de la industria**  
✅ **Fácil de entender**

---

## 🏗️ Las 3 Capas del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    🌐 USUARIO FINAL                         │
└─────────────────────┬───────────────────────────────────────┘
                      │ Interactúa
                      ▼
╔═════════════════════════════════════════════════════════════╗
║  🎨 CAPA 1: PRESENTACIÓN (Frontend)                        ║
║  Carpeta: frontend/                                         ║
║                                                              ║
║  Responsabilidad:                                            ║
║  • Mostrar la interfaz de usuario                            ║
║  • Capturar interacciones del usuario                        ║
║  • Enviar peticiones al backend                              ║
║  • Renderizar respuestas                                     ║
║                                                              ║
║  Tecnologías:                                                ║
║  - Templates Django (HTML)                                   ║
║  - Bootstrap 5.3 (CSS)                                       ║
║  - JavaScript Vanilla                                        ║
║  - Bootstrap Icons                                           ║
║                                                              ║
║  Contenido:                                                  ║
║  frontend/                                                   ║
║  ├── templates/                                              ║
║  │   ├── estudiante/     # UI para estudiantes               ║
║  │   ├── docente/        # UI para docentes                  ║
║  │   ├── presidente/     # UI para presidentes               ║
║  │   └── secretaria/     # UI para secretarias               ║
║  └── static/                                                 ║
║      ├── css/            # Estilos personalizados            ║
║      ├── js/             # JavaScript                        ║
║      └── images/         # Imágenes                          ║
╚═════════════════════════════════════════════════════════════╝
                      │ HTTP Request
                      ▼
╔═════════════════════════════════════════════════════════════╗
║  🔧 CAPA 2: LÓGICA DE NEGOCIO (Backend)                    ║
║  Carpeta: backend/                                          ║
║                                                              ║
║  Responsabilidad:                                            ║
║  • Procesar la lógica del negocio                            ║
║  • Validar datos                                             ║
║  • Implementar reglas de negocio                             ║
║  • Coordinar entre frontend y database                       ║
║  • Gestionar autenticación y autorización                    ║
║                                                              ║
║  Tecnologías:                                                ║
║  - Django 4.2 (Framework web)                                ║
║  - Python 3.9+                                               ║
║  - Django ORM                                                ║
║                                                              ║
║  Organización Interna (apps Django):                         ║
║  backend/apps/                                               ║
║  ├── presentacion/       # Vistas HTTP por rol               ║
║  ├── negocio/            # Servicios con lógica              ║
║  ├── datos/              # Repositorios (acceso a BD)        ║
║  ├── usuarios/           # Gestión de usuarios               ║
║  ├── informes/           # Gestión de informes + Estados     ║
║  ├── observaciones/      # IA + Banco de observaciones       ║
║  ├── escuelas/           # Escuelas profesionales            ║
║  ├── notificaciones/     # Sistema de notificaciones         ║
║  └── core/               # Utilidades compartidas            ║
╚═════════════════════════════════════════════════════════════╝
                      │ Query/Insert/Update
                      ▼
╔═════════════════════════════════════════════════════════════╗
║  💾 CAPA 3: DATOS (Database)                               ║
║  Carpeta: database/                                         ║
║                                                              ║
║  Responsabilidad:                                            ║
║  • Almacenar datos de forma persistente                      ║
║  • Garantizar integridad de datos                            ║
║  • Gestionar transacciones                                   ║
║  • Optimizar consultas                                       ║
║                                                              ║
║  Tecnologías:                                                ║
║  - SQLite (Desarrollo)                                       ║
║  - PostgreSQL (Producción - recomendado)                     ║
║                                                              ║
║  Contenido:                                                  ║
║  database/                                                   ║
║  └── db.sqlite3          # Base de datos                     ║
║                                                              ║
║  Tablas Principales:                                         ║
║  - usuarios_usuario      # Usuarios del sistema              ║
║  - informes_informe      # Informes de prácticas             ║
║  - observaciones_*       # Observaciones e IA                ║
║  - escuelas_escuela      # Escuelas profesionales            ║
║  - notificaciones_*      # Notificaciones                    ║
╚═════════════════════════════════════════════════════════════╝
```

---

## 🎨 Capa 1: Presentación (Frontend)

### Ubicación

```
frontend/
├── templates/
│   ├── base.html                    # Template base legacy
│   ├── base_v2.html                 # Template moderno con sidebar mejorado
│   ├── login.html                   # Página de inicio de sesión
│   │
│   ├── estudiante/                  # UI para Estudiantes
│   │   ├── base_estudiante.html    # Base con navbar específico
│   │   ├── dashboard.html          # Dashboard principal
│   │   ├── enviar_informe.html     # Formulario de envío
│   │   ├── historial.html          # Historial de informes (con versionado)
│   │   └── detalle_informe.html    # Ver estado y dictamen
│   │
│   ├── docente/                     # UI para Docentes
│   │   ├── base_docente.html       # Base con navbar específico
│   │   ├── dashboard.html          # Informes asignados + revisados
│   │   ├── revisar.html            # Validación con IA + confirmar obs
│   │   ├── banco.html              # Gestión de bancos de observaciones
│   │   ├── detalle_banco.html      # Ver contenido del banco
│   │   └── estadisticas.html       # Métricas del docente
│   │
│   ├── presidente/                  # UI para Presidentes
│   │   ├── base_presidente.html    # Base con navbar específico
│   │   ├── dashboard.html          # Informes pendientes de asignar/revisar
│   │   ├── asignar.html            # Asignar docente revisor
│   │   ├── revisar.html            # Revisar dictamen (3 decisiones)
│   │   └── estadisticas.html       # Métricas de la escuela
│   │
│   ├── secretaria/                  # UI para Secretarias
│   │   ├── base_secretaria.html    # Base con navbar específico
│   │   ├── dashboard.html          # Nuevos + completados (aprobado/rechazado)
│   │   ├── derivar.html            # Derivar a escuela profesional
│   │   ├── notificar.html          # Notificar aprobación/rechazo final
│   │   └── historial.html          # Historial completo
│   │
│   ├── admin/                       # UI para Administradores
│   │   ├── base_admin.html         # Base con panel administrativo
│   │   ├── dashboard.html          # Estadísticas globales
│   │   ├── usuarios.html           # Gestión de usuarios
│   │   ├── escuelas.html           # Gestión de escuelas
│   │   └── reportes.html           # Reportes y analytics
│   │
│   └── components/                  # Componentes reutilizables
│       ├── notificaciones.html     # Widget de notificaciones
│       ├── tabla_informes.html     # Tabla con filtros
│       └── modal_confirmacion.html # Modal genérico
│
└── static/
    ├── css/
    │   ├── untels-theme.css        # Paleta de colores UNTELS
    │   ├── custom.css              # Estilos personalizados
    │   └── responsive.css          # Media queries
    │
    ├── js/
    │   ├── multi-tab-sessions.js   # Gestión de sesiones en múltiples tabs
    │   ├── validacion-ia.js        # Barra de progreso de IA
    │   ├── notificaciones.js       # Actualización de notificaciones
    │   ├── confirmar-observaciones.js  # UI para confirmar/descartar obs
    │   └── utils.js                # Utilidades comunes
    │
    └── images/
        ├── logo-untels.png         # Logo oficial
        ├── favicon.ico             # Favicon
        └── placeholders/           # Imágenes de placeholder
```

### Responsabilidad

- ✅ **Renderizar HTML** para cada rol de usuario con interfaces diferenciadas
- ✅ **Capturar eventos** (clicks, formularios, drag & drop)
- ✅ **Enviar peticiones HTTP** al backend vía AJAX y formularios
- ✅ **Mostrar respuestas** al usuario (toasts, modales, actualizaciones dinámicas)
- ✅ **Experiencia de usuario (UX)** optimizada por rol
- ✅ **Validación en cliente** antes de enviar al servidor
- ✅ **Progreso visual** para operaciones largas (validación IA)

### Características

- **Responsive Design**: Se adapta a móvil, tablet, desktop con breakpoints personalizados
- **Por Rol**: Cada usuario ve su interfaz específica con navegación contextual
- **Bootstrap 5.3**: Framework CSS moderno con componentes interactivos
- **Paleta UNTELS**: Azul #1a3a6b oficial en toda la aplicación
- **Accesibilidad**: Cumple con WCAG 2.1 (contraste, navegación por teclado)
- **Carga rápida**: Lazy loading de imágenes, CSS/JS minificados
- **Notificaciones en tiempo real**: Badge con contador de no leídas
- **Multi-tab support**: Sesiones sincronizadas entre pestañas del navegador

---

## 🔧 Capa 2: Lógica de Negocio (Backend)

### Ubicación

```
backend/
├── apps/                               # Aplicaciones Django
│   │
│   ├── presentacion/                   # ⭐ CAPA DE PRESENTACIÓN (Vistas HTTP)
│   │   └── web/
│   │       ├── auth_views.py          # Login, logout, registro
│   │       ├── estudiante_views.py    # Vistas de estudiantes
│   │       ├── docente_views.py       # Vistas de docentes
│   │       ├── presidente_views.py    # Vistas de presidentes (3 decisiones)
│   │       ├── secretaria_views.py    # Vistas de secretarias
│   │       └── admin_views.py         # Panel administrativo
│   │
│   ├── negocio/                        # ⭐ CAPA DE NEGOCIO (Servicios)
│   │   └── servicios/
│   │       ├── estudiante.py          # EstudianteService (futuro)
│   │       ├── docente.py             # DocenteService
│   │       │   ├── obtener_informes_asignados()
│   │       │   ├── obtener_informes_revisados()
│   │       │   ├── obtener_banco_activo()
│   │       │   ├── crear_banco_observaciones()
│   │       │   ├── validar_informe_con_ia()
│   │       │   ├── confirmar_observacion()
│   │       │   ├── descartar_observacion()
│   │       │   ├── enviar_dictamen_a_presidente()
│   │       │   └── obtener_estadisticas()
│   │       │
│   │       ├── presidente.py          # PresidenteService
│   │       │   ├── obtener_informes_pendientes()
│   │       │   ├── obtener_informes_para_dictamen()
│   │       │   ├── obtener_docentes_disponibles()
│   │       │   ├── asignar_docente()
│   │       │   ├── aprobar_dictamen_docente() (3 acciones)
│   │       │   ├── rechazar_dictamen_docente()
│   │       │   └── obtener_estadisticas()
│   │       │
│   │       └── secretaria.py          # SecretariaService
│   │           ├── obtener_informes_pendientes()
│   │           ├── obtener_informes_completados()
│   │           ├── derivar_a_presidente()
│   │           ├── notificar_estudiante_aprobado()
│   │           ├── notificar_estudiante_rechazado()
│   │           └── obtener_estadisticas()
│   │
│   ├── datos/                          # ⭐ CAPA DE DATOS (Repositorios)
│   │   └── repositorios/
│   │       ├── informes.py            # InformeRepository
│   │       │   ├── obtener_por_id()
│   │       │   ├── obtener_con_observaciones()
│   │       │   ├── obtener_por_estado_y_docente()
│   │       │   └── obtener_ultimas_versiones()
│   │       │
│   │       ├── usuarios.py            # UsuarioRepository
│   │       │   ├── obtener_por_codigo()
│   │       │   ├── obtener_docentes_por_escuela()
│   │       │   └── validar_credenciales()
│   │       │
│   │       └── observaciones.py       # ObservacionRepository
│   │           ├── obtener_por_informe()
│   │           ├── obtener_confirmadas()
│   │           └── obtener_descartadas()
│   │
│   ├── usuarios/                       # App de Usuarios
│   │   ├── models.py                  # Modelo Usuario (5 tipos)
│   │   ├── managers.py                # Custom managers
│   │   └── migrations/
│   │
│   ├── informes/                       # App de Informes
│   │   ├── models.py                  # Modelo Informe (con versionado)
│   │   ├── state.py                   # State Machine (11 estados)
│   │   ├── utils.py                   # Extracción de texto (PDF/DOCX)
│   │   └── migrations/
│   │
│   ├── observaciones/                  # App de Observaciones e IA
│   │   ├── models.py                  # ObservacionGenerada, BancoObservaciones
│   │   ├── services.py                # Integración con APIs de IA
│   │   │   ├── validar_con_groq()     # Strategy pattern
│   │   │   ├── _validar_con_xai()     # xAI Grok API
│   │   │   ├── _validar_con_groq_api() # Groq API
│   │   │   └── _validacion_local()    # Fallback
│   │   └── migrations/
│   │
│   ├── escuelas/                       # App de Escuelas Profesionales
│   │   ├── models.py                  # Modelo Escuela
│   │   ├── services.py                # EscuelaService
│   │   └── migrations/
│   │
│   ├── notificaciones/                 # App de Notificaciones
│   │   ├── models.py                  # Modelo Notificacion
│   │   ├── services.py                # NotificacionService (Observer)
│   │   │   ├── crear_notificacion()
│   │   │   ├── notificar_informe_nuevo()
│   │   │   ├── notificar_informe_derivado()
│   │   │   ├── notificar_informe_asignado()
│   │   │   ├── notificar_dictamen_enviado()
│   │   │   ├── notificar_aprobacion_presidente()
│   │   │   ├── notificar_rechazo_presidente()
│   │   │   └── marcar_como_leida()
│   │   └── migrations/
│   │
│   └── core/                           # Utilidades Compartidas
│       ├── decorators.py              # @requiere_rol (Decorator pattern)
│       ├── middleware.py              # Middleware personalizado
│       ├── admin_views.py             # Vistas admin
│       ├── templatetags/              # Filtros personalizados
│       │   └── dictamen_filters.py    # @formatear_dictamen
│       └── utils.py                   # Funciones auxiliares
│
├── config/                             # Configuración Django
│   ├── settings/
│   │   ├── base.py                    # Configuración base
│   │   ├── development.py             # Desarrollo (DEBUG=True)
│   │   └── production.py              # Producción (DEBUG=False)
│   ├── urls.py                        # URLs principales
│   ├── wsgi.py                        # WSGI application
│   └── asgi.py                        # ASGI application (futuro WebSockets)
│
├── media/                              # Archivos subidos por usuarios
│   ├── informes/                      # PDFs de informes
│   └── bancos/                        # Bancos de observaciones
│
├── staticfiles/                        # Archivos estáticos compilados
├── venv/                               # Entorno virtual Python
├── manage.py                           # CLI de Django
├── requirements.txt                    # Dependencias Python
├── .env                                # Variables de entorno (no versionado)
└── .gitignore
```

### Responsabilidad

- ✅ **Implementar todas las reglas de negocio** en la capa de servicios
- ✅ **Validar datos de entrada** antes de persistir
- ✅ **Procesar lógica compleja** (validación IA, dictámenes, versionado)
- ✅ **Autenticación y autorización** personalizada sin django.contrib.auth
- ✅ **Integración con APIs externas** (xAI Grok, Groq) con fallback automático
- ✅ **Gestionar el flujo multi-rol** con State Machine de 11 estados
- ✅ **Trazabilidad completa** con fechas en cada transición
- ✅ **Sistema de notificaciones** basado en eventos (Observer pattern)
- ✅ **Extracción de texto** de PDF/DOCX para procesamiento IA

### Organización Interna

El backend está organizado en **apps Django** que siguen principios de **Clean Architecture**:

| App | Propósito | Patrones Aplicados |
|-----|-----------|-------------------|
| **presentacion/web/** | Vistas HTTP (controladores) | Decorator (@requiere_rol) |
| **negocio/servicios/** | Servicios con lógica de negocio | Service Layer, Facade |
| **datos/repositorios/** | Repositorios (acceso a BD) | Repository Pattern |
| **usuarios/** | Modelo Usuario + gestión | Active Record |
| **informes/** | Modelo Informe + State Machine | State Machine (11 estados) |
| **observaciones/** | Modelo Observación + IA | Strategy (selección de API) |
| **escuelas/** | Modelo Escuela profesional | - |
| **notificaciones/** | Modelo Notificación + eventos | Observer Pattern |
| **core/** | Decoradores, middleware, utils | Decorator, Template Method |

---

## 💾 Capa 3: Datos (Database)

### Ubicación

```
database/
└── db.sqlite3
```

### Responsabilidad

- ✅ Persistir todos los datos del sistema
- ✅ Garantizar integridad referencial
- ✅ Gestionar transacciones ACID
- ✅ Indexar para optimizar consultas
- ✅ Respaldar información

### Modelo de Datos

El sistema tiene **8 tablas principales**:

1. **usuarios_usuario** - Usuarios (estudiantes, docentes, etc.)
2. **informes_informe** - Informes de prácticas
3. **observaciones_observaciongenerada** - Observaciones de IA
4. **observaciones_bancoobservacionesdocente** - Bancos personalizados
5. **escuelas_escuela** - Escuelas profesionales
6. **notificaciones_notificacion** - Notificaciones
7. **reglamento_reglamento** - Reglamentos (opcional)
8. **core_* ** - Tablas auxiliares

Ver más detalles en [BASE_DE_DATOS.md](BASE_DE_DATOS.md)

---

## 🔀 Flujo de Datos

### Ejemplo: Estudiante Sube Informe

```
1. 🌐 Usuario: Hace clic en "Subir Informe"
   ↓
2. 🎨 CAPA 1 (Frontend):
   - frontend/templates/estudiante/enviar_informe.html
   - Captura archivo y datos
   - Envía POST /estudiante/enviar/
   ↓
3. 🔧 CAPA 2 (Backend):
   - backend/apps/presentacion/web/estudiante_views.py
   - Recibe request HTTP
   - Valida datos
   - Extrae texto del PDF/DOCX
   - Crea objeto Informe
   - Llama al ORM para guardar
   ↓
4. 💾 CAPA 3 (Database):
   - database/db.sqlite3
   - INSERT INTO informes_informe ...
   - Retorna ID del nuevo registro
   ↓
5. 🔧 CAPA 2 (Backend):
   - Crea notificación para secretaria
   - Retorna HTTP 200 + mensaje de éxito
   ↓
6. 🎨 CAPA 1 (Frontend):
   - Muestra mensaje "Informe enviado correctamente"
   - Redirige al dashboard
```

### Flujo Completo del Sistema

```
Estudiante (sube) → Backend (valida) → Database (guarda)
     ↓
Secretaria (deriva) → Backend (asigna) → Database (actualiza)
     ↓
Presidente (asigna docente) → Backend (notifica) → Database
     ↓
Docente (valida con IA) → Backend (llama API) → Database (guarda obs)
     ↓
Docente (envía dictamen) → Backend (procesa) → Database
     ↓
Presidente (aprueba, rechaza o devuelve dictamen) → Backend → Database
     ↓
Secretaria (notifica) → Backend → Database
     ↓
Estudiante (recibe resultado)
```

---

## 🔷 Principios SOLID

Aunque el sistema tiene 3 capas, dentro del backend aplicamos principios SOLID:

### S - Single Responsibility

Cada módulo tiene una responsabilidad:

```python
# ✅ CORRECTO
class DocenteService:
    """Solo operaciones de docentes"""
    pass

class InformeService:
    """Solo operaciones de informes"""
    pass
```

### O - Open/Closed

Abierto para extensión, cerrado para modificación:

```python
# Fácil agregar nueva API de IA sin modificar código existente
def validar_con_api(contenido, banco):
    if api_key.startswith('xai-'):
        return validar_con_xai()
    elif api_key.startswith('gsk_'):
        return validar_con_groq()
    # Agregar nueva API aquí
```

### L - Liskov Substitution

Las subclases deben ser reemplazables:

```python
class BaseInformeState:
    def transition(self, informe, next_state):
        # Implementación base

class EnviadoState(BaseInformeState):
    # Puede reemplazar a la base
    pass
```

### I - Interface Segregation

Interfaces específicas:

```python
# Servicios específicos por dominio
class DocenteService:
    obtener_informes_asignados()
    validar_informe_con_ia()

class PresidenteService:
    asignar_docente()
    aprobar_dictamen_docente()
    rechazar_dictamen_docente()
```

### D - Dependency Inversion

Depender de abstracciones:

```python
# ✅ Vista depende del servicio (abstracción)
informes = DocenteService.obtener_informes_asignados(docente)

# ❌ NO depende del ORM directamente
informes = Informe.objects.filter(...)  # Evitar en vistas
```

---

## 📊 Ventajas de las 3 Capas

### 1. Separación de Responsabilidades

- **Frontend**: Solo se preocupa de la UI
- **Backend**: Solo se preocupa de la lógica
- **Database**: Solo se preocupa de los datos

### 2. Desarrollo Paralelo

- ✅ Equipo de frontend puede trabajar independientemente
- ✅ Equipo de backend puede trabajar independientemente
- ✅ DBA puede optimizar la BD independientemente

### 3. Escalabilidad

- ✅ Cada capa puede escalarse por separado
- ✅ Frontend: CDN, múltiples instancias
- ✅ Backend: Load balancer, microservicios
- ✅ Database: Replicación, sharding

### 4. Mantenibilidad

- ✅ Cambios en UI no afectan la lógica
- ✅ Cambios en lógica no afectan la UI
- ✅ Cambios en BD (SQLite → PostgreSQL) transparentes

### 5. Testabilidad

```python
# Test de lógica de negocio sin DB ni UI
def test_validar_informe():
    service = DocenteService()
    result = service.validar_informe_con_ia(...)
    assert result == expected
```

---

## 🎓 Resumen

### Arquitectura: 3 Capas

1. **🎨 Frontend** (`frontend/`) - Presentación e interfaz
2. **🔧 Backend** (`backend/`) - Lógica de negocio
3. **💾 Database** (`database/`) - Persistencia de datos

### Tecnologías

| Capa | Tecnologías |
|------|-------------|
| Frontend | Django Templates, Bootstrap 5, JavaScript |
| Backend | Django 4.2, Python 3.9+, Django ORM |
| Database | SQLite (dev), PostgreSQL (prod) |

### Conclusión

**"Arquitectura de 3 Capas clásica y probada, con organización interna del backend siguiendo principios de Clean Code y SOLID"**

- ✅ Clara y fácil de entender
- ✅ Estándar de la industria
- ✅ Escalable y mantenible
- ✅ Testeable
- ✅ Profesional

---

**Ver también**: [Backend](BACKEND.md) | [Frontend](FRONTEND.md) | [Base de Datos](BASE_DE_DATOS.md) | [Patrones](PATRONES.md)
