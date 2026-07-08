# 📊 Diagramas de Arquitectura de Software - Sistema de Validación UNTELS

Este directorio contiene los **6 diagramas profesionales** que documentan la arquitectura completa del Sistema de Validación de Informes con IA para UNTELS.

---

## 📁 Contenido

### 01-arquitectura-3-capas.drawio
**Arquitectura de 3 Capas del Sistema**

Diagrama que muestra la separación del sistema en tres capas claramente definidas:
- **Capa de Presentación**: Frontend con Django Templates, Bootstrap 5, JavaScript
- **Capa de Lógica de Negocio**: Backend Django organizado en 3 subcapas (Presentación HTTP, Servicios, Repositorios)
- **Capa de Datos**: Base de datos SQLite/PostgreSQL con 6 tablas principales

**Tecnologías mostradas**: Django, Python, Bootstrap, JavaScript, PostgreSQL

---

### 02-flujo-sistema-completo.drawio
**Diagrama de Flujo de Estados (State Machine)**

Representa el flujo completo de un informe a través de **11 estados posibles**:
1. `enviado` - Estudiante sube el informe
2. `derivado` - Secretaria deriva a escuela
3. `asignado_presidente` - Asignado al presidente
4. `asignado_docente` - Presidente asigna docente revisor
5. `pendiente_docente` - Esperando validación
6. `validando_ia` - IA procesando el documento
7. `revision_docente` - Docente revisa observaciones IA
8. `dictamen_emitido` - Docente emite dictamen
9. `revision_presidente` - Presidente revisa dictamen
10. `aprobado_final` - Informe aprobado
11. `rechazado_final` - Informe rechazado con observaciones

**Actores involucrados**: Estudiante, Secretaria, Presidente, Docente, Sistema IA

---

### 03-diagrama-er-base-datos.drawio
**Diagrama Entidad-Relación (ER) de la Base de Datos**

Modelo de datos completo con **6 tablas principales**:

| Tabla | Descripción | Campos Clave |
|-------|-------------|--------------|
| `usuarios_usuario` | Almacena todos los usuarios (5 tipos) | tipo_usuario, email, nombre |
| `escuelas_escuela` | Escuelas profesionales | nombre, presidente_id |
| `informes_informe` | Núcleo del sistema (11 estados) | estado, archivo, usuario_id, version_anterior |
| `observaciones_observaciongenerada` | Observaciones de IA | severidad, estado_obs, informe_id |
| `observaciones_bancoobservacionesdocente` | Bancos personalizados por docente | nombre, criterios, activo |
| `notificaciones_notificacion` | Sistema de notificaciones | tipo, leida, usuario_id |

**Características especiales**:
- Auto-referencia en `Informe` para versionado
- Índices compuestos para optimización
- Relaciones 1:N y N:1 claramente definidas

---

### 04-estructura-backend.drawio
**Estructura Interna del Backend Django**

Muestra la organización del backend siguiendo **Clean Architecture**:

```
backend/
├── apps/
│   ├── presentacion/
│   │   └── web/              # Vistas HTTP (delgadas)
│   │       ├── estudiante_views.py
│   │       ├── docente_views.py
│   │       ├── presidente_views.py
│   │       └── secretaria_views.py
│   │
│   ├── negocio/
│   │   └── servicios/        # Lógica de negocio (gruesa)
│   │       ├── DocenteService
│   │       ├── PresidenteService
│   │       ├── SecretariaService
│   │       └── NotificacionService
│   │
│   └── datos/
│       └── repositorios/     # Acceso a datos (abstracción ORM)
│           ├── InformeRepository
│           ├── UsuarioRepository
│           └── ObservacionRepository
│
└── config/                   # Configuración Django
```

**Aplicaciones Django modulares**:
- `usuarios/` - Gestión de 5 tipos de usuarios
- `informes/` - Modelo Informe con State Machine
- `observaciones/` - IA y bancos de observaciones
- `escuelas/` - Escuelas profesionales
- `notificaciones/` - Observer Pattern
- `core/` - Decoradores, middleware, utils

---

### 05-patrones-diseño.drawio
**8 Patrones de Diseño Implementados**

Diagrama que documenta cada uno de los **8 patrones GoF y Enterprise** aplicados:

1. **Repository Pattern** → `apps/datos/repositorios/`
   - Abstrae el acceso a datos
   - Optimiza queries con `select_related` y `prefetch_related`

2. **Service Layer Pattern** → `apps/negocio/servicios/`
   - Encapsula toda la lógica de negocio
   - Retorna tupla `(success, data, error)`

3. **State Machine Pattern** → `informes/models.py`
   - Controla transiciones entre 11 estados
   - Valida transiciones permitidas

4. **Strategy Pattern** → `observaciones/services.py`
   - Selección dinámica de API IA (xAI/Groq/Fallback)
   - Cambio de algoritmo en runtime

5. **Observer Pattern** → `notificaciones/services.py`
   - Notificaciones automáticas en cambios de estado
   - Desacoplamiento entre emisor y receptores

6. **Decorator Pattern** → `core/decorators.py`
   - `@requiere_rol()` para autorización
   - Añade funcionalidad sin modificar clases

7. **Facade Pattern** → Simplificación de subsistemas complejos
   - Interfaz unificada para servicios IA

8. **Template Method Pattern** → Flujos de validación estandarizados
   - Define esqueleto de algoritmo

**Ubicación en código real**: Cada patrón referencia archivos específicos del proyecto

---

### 06-secuencia-validacion-ia.drawio
**Diagrama de Secuencia - Validación con IA**

Representa el **flujo completo de 23 pasos** de la validación automática con inteligencia artificial:

**Actores**:
- Docente (usuario)
- DocenteService (capa de negocio)
- InformeRepository (capa de datos)
- BancoObservacionesRepository (capa de datos)
- ValidarInformeIA (servicio IA)
- API Externa (xAI Grok / Groq LLaMA)
- ObservacionGenerada (modelo)

**Flujo principal**:
1. Docente solicita validación con IA
2. Servicio obtiene informe desde repositorio
3. Valida estado del informe (debe estar en `pendiente_docente` o `rechazado_presidente`)
4. Obtiene banco de observaciones activo del docente
5. Construye prompt con banco + contenido del informe
6. Intenta validación con xAI Grok
7. Si falla o sin créditos → Intenta con Groq LLaMA
8. Si falla → Fallback a validación local con regex
9. Parsea respuesta JSON de la IA
10. Crea observaciones en BD con severidad (crítica, mayor, menor, sugerencia)
11. Actualiza estado del informe a `validando_ia` → `revision_docente`
12. Registra banco utilizado
13. Retorna observaciones al docente

**Tiempo de ejecución**: < 30 segundos (vs 2-3 días manual)

---

## 🎨 Convenciones de Diseño

### Colores utilizados:
- **Azul oscuro (#003876)**: Elementos principales, títulos
- **Dorado (#FDB913)**: Destacados, acciones importantes
- **Verde (#4CAF50)**: Estados exitosos, aprobaciones
- **Rojo (#F44336)**: Errores, rechazos, validaciones fallidas
- **Gris (#757575)**: Información secundaria, notas

### Formas:
- **Rectángulos con bordes redondeados**: Componentes del sistema
- **Rombos**: Decisiones en flujos
- **Cilindros**: Base de datos / repositorios
- **Actores (stickman)**: Usuarios del sistema
- **Flechas direccionales**: Flujo de datos / control

---

## 🛠️ Cómo Editar los Diagramas

### Opción 1: Draw.io Online (Recomendado)
1. Ve a https://app.diagrams.net/
2. Click en "Open Existing Diagram"
3. Selecciona el archivo `.drawio` que quieras editar
4. Edita el diagrama
5. File → Save (guarda automáticamente)

### Opción 2: Draw.io Desktop
1. Descarga Draw.io Desktop: https://github.com/jgraph/drawio-desktop/releases
2. Abre el archivo `.drawio` deseado
3. Edita y guarda

### Opción 3: VS Code
1. Instala extensión "Draw.io Integration"
2. Abre cualquier `.drawio` en VS Code
3. Edita directamente en el editor

---

## 📤 Exportar Diagramas

### Para presentaciones o documentos:

**PNG (Alta resolución)**:
1. Abre el diagrama en Draw.io
2. File → Export as → PNG
3. Configuración recomendada:
   - Zoom: 200%
   - Border Width: 10
   - Transparent Background: No
   - Selection Only: No

**PDF (Documentos profesionales)**:
1. File → Export as → PDF
2. Configuración:
   - All Pages: Yes
   - Crop: No

**SVG (Vectorial escalable)**:
1. File → Export as → SVG
2. Ideal para web o impresiones de gran formato

---

## 📊 Estadísticas de los Diagramas

| Diagrama | Tamaño | Elementos | Complejidad |
|----------|--------|-----------|-------------|
| 01-arquitectura-3-capas | 12 KB | ~15 componentes | Media |
| 02-flujo-sistema-completo | 31 KB | 11 estados + transiciones | Alta |
| 03-diagrama-er-base-datos | 25 KB | 6 tablas + relaciones | Alta |
| 04-estructura-backend | 20 KB | 3 capas + apps | Media |
| 05-patrones-diseño | 34 KB | 8 patrones detallados | Muy Alta |
| 06-secuencia-validacion-ia | 24 KB | 23 pasos + 7 actores | Muy Alta |

**Total**: 146 KB de documentación visual profesional

---

## 🎓 Equipo del Proyecto

- **Díaz Sánchez, Leonardo**
- **Rodríguez Díaz, Enrique**
- **Salas Chaparín, Andre Alonso**
- **Sinarahua Cárdenas, Gian**

**Curso**: Arquitectura de Software  
**Universidad**: Universidad Nacional Tecnológica de Lima Sur (UNTELS)  
**Semestre**: 2026-I

---

## 📚 Referencias Técnicas

Los diagramas están basados en:
- Clean Architecture (Robert C. Martin)
- Design Patterns: Elements of Reusable OO Software (Gang of Four)
- Patterns of Enterprise Application Architecture (Martin Fowler)
- UML 2.0 Specification
- Django Documentation

---

**Última actualización**: Julio 2026
