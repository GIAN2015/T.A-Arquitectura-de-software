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
│   ├── base.html
│   ├── base_v2.html
│   ├── login.html
│   ├── estudiante/
│   │   ├── dashboard.html
│   │   └── enviar_informe.html
│   ├── docente/
│   │   ├── dashboard.html
│   │   ├── revisar.html
│   │   └── banco.html
│   ├── presidente/
│   │   ├── dashboard.html
│   │   └── revisar.html
│   └── secretaria/
│       ├── dashboard.html
│       └── notificar.html
└── static/
    ├── css/
    │   └── untels-theme.css
    ├── js/
    │   └── multi-tab-sessions.js
    └── images/
```

### Responsabilidad

- ✅ Renderizar HTML para cada rol de usuario
- ✅ Capturar eventos (clicks, formularios)
- ✅ Enviar peticiones HTTP al backend
- ✅ Mostrar respuestas al usuario
- ✅ Experiencia de usuario (UX)

### Características

- **Responsive**: Se adapta a móvil, tablet, desktop
- **Por Rol**: Cada usuario ve su interfaz específica
- **Bootstrap 5.3**: Framework CSS moderno
- **Paleta UNTELS**: Azul #1a3a6b oficial

---

## 🔧 Capa 2: Lógica de Negocio (Backend)

### Ubicación

```
backend/
├── apps/
│   ├── presentacion/        # Vistas Django (HTTP)
│   ├── negocio/             # Servicios (Lógica)
│   ├── datos/               # Repositorios (Acceso a BD)
│   ├── usuarios/            # App de usuarios
│   ├── informes/            # App de informes
│   ├── observaciones/       # App de IA
│   ├── escuelas/            # App de escuelas
│   ├── notificaciones/      # App de notificaciones
│   └── core/                # Utilidades
├── config/                  # Configuración Django
│   ├── settings/
│   ├── urls.py
│   └── wsgi.py
└── manage.py                # CLI Django
```

### Responsabilidad

- ✅ Implementar todas las reglas de negocio
- ✅ Validar datos de entrada
- ✅ Procesar lógica compleja
- ✅ Autenticación y autorización
- ✅ Integración con APIs externas (IA)
- ✅ Gestionar el flujo multi-rol

### Organización Interna

El backend está organizado en **apps Django** que siguen principios de Clean Architecture:

| App | Propósito |
|-----|-----------|
| **presentacion/** | Vistas HTTP (controladores) |
| **negocio/** | Servicios con lógica de negocio |
| **datos/** | Repositorios (patrón Repository) |
| **usuarios/** | Modelo Usuario + lógica |
| **informes/** | Modelo Informe + State Machine |
| **observaciones/** | Modelo Observación + IA |
| **escuelas/** | Modelo Escuela |
| **notificaciones/** | Modelo Notificación |
| **core/** | Decoradores, middleware, utils |

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
Presidente (aprueba/rechaza) → Backend → Database
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
    aprobar_dictamen()
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
