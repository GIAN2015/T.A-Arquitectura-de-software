# Panel de Administración Personalizado - Sistema UNTELS

## Descripción General

Se ha creado un **Panel de Administración Profesional y Personalizado** para que los docentes puedan gestionar todo el sistema de validación de informes sin necesidad de usar el Django Admin predeterminado.

## Diferencias entre Paneles

### 1. Panel Docente (`/panel-docente/`)
- **Propósito**: Ver y revisar informes de estudiantes
- **Funcionalidad**: Solo lectura de informes
- **Acceso**: Docentes
- **Ubicación**: `apps/core/views.py:panel_docente_view`

### 2. Panel de Administración (`/admin/dashboard/`)
- **Propósito**: Gestión completa del sistema
- **Funcionalidad**: CRUD completo de usuarios, reglamento, observaciones
- **Acceso**: Docentes (administradores)
- **Ubicación**: `apps/core/admin_views.py`

### 3. Django Admin (`/admin/`) - NO USAR
- **Propósito**: Panel técnico de Django
- **Funcionalidad**: Básico, sin personalización
- **Acceso**: Solo superusuarios
- **Estado**: Disponible pero no recomendado

---

## Estructura del Panel de Administración

### Archivos Creados

```
apps/core/
├── admin_views.py          # Vistas del panel admin (360 líneas)
└── urls.py                 # URLs actualizadas con rutas del admin

templates/admin/
├── dashboard.html          # Dashboard principal con estadísticas
├── usuarios.html           # Gestión de usuarios (lista + filtros)
├── usuario_detalle.html    # Detalle de un usuario específico
├── reglamento.html         # Gestión del reglamento institucional
├── observaciones.html      # Banco de observaciones
└── reportes.html           # Reportes y estadísticas avanzadas
```

---

## Funcionalidades del Panel Admin

### 1. Dashboard (`/admin/dashboard/`)

**Estadísticas en tiempo real:**
- Total de usuarios (estudiantes, egresados, docentes)
- Total de informes
- Informes completados
- Informes en proceso
- Informes recientes (últimos 7 días)

**Secciones con más observaciones:**
- Top 5 de secciones más observadas
- Gráfico de frecuencia

**Últimos informes:**
- 10 informes más recientes
- Estado de cada informe
- Enlace al panel docente

**Accesos rápidos:**
- Gestionar Usuarios
- Actualizar Reglamento
- Banco de Observaciones
- Ver Reportes

### 2. Gestión de Usuarios (`/admin/usuarios/`)

**Funcionalidades:**
- **Lista completa** de todos los usuarios
- **Filtros** por tipo (estudiante, egresado, docente)
- **Búsqueda** por código o nombre
- **Contador** de informes por usuario
- **Vista detallada** de cada usuario

**Detalle de usuario (`/admin/usuarios/<id>/`):**
- Información completa del usuario
- Estadísticas personales:
  - Total de informes
  - Informes completados
  - Total de observaciones
  - Tasa de completitud (%)
- Historial completo de informes
- Enlaces a informes específicos

### 3. Gestión de Reglamento (`/admin/reglamento/`)

**Funcionalidades:**
- **Crear nuevo reglamento** con formulario
- **Historial completo** de versiones anteriores
- **Vista previa** del contenido de cada reglamento
- **Activación automática** del nuevo reglamento
- **Desactivación automática** de versiones anteriores

**Campos del formulario:**
- Nombre del reglamento (ej: "Reglamento 2024 - v2.0")
- Contenido completo del reglamento (textarea)

**Vista de historial:**
- Estado (Activo/Inactivo)
- Fecha de creación
- Longitud del contenido
- Modal para ver contenido completo

### 4. Banco de Observaciones (`/admin/observaciones/`)

**Funcionalidades:**
- **Agregar observaciones** al banco
- **Listar todas las observaciones** agrupadas por sección
- **Eliminar observaciones** con confirmación
- **Estadísticas** de distribución por sección

**Secciones disponibles:**
- Portada
- Resumen
- Introducción
- Marco Teórico
- Metodología
- Resultados
- Conclusiones
- Bibliografía
- Anexos
- Formato General

**Agrupación inteligente:**
- Observaciones organizadas por sección
- Contador de observaciones por sección
- Gráfico de distribución

### 5. Reportes y Estadísticas (`/admin/reportes/`)

**Estadísticas disponibles:**

**Distribución de informes por estado:**
- Enviados
- En Revisión
- Completados

**Informes por tipo de usuario:**
- Estudiantes
- Egresados

**Usuarios más activos:**
- Top 10 de usuarios con más informes
- Número de informes por usuario

**Top 10 Observaciones más frecuentes:**
- Ranking de observaciones
- Sección asociada
- Frecuencia absoluta
- Porcentaje relativo
- Gráfico de barras

**Resumen general:**
- Total de informes
- Informes procesados
- Tipos de observaciones
- Usuarios activos

---

## URLs del Sistema

### Autenticación
```
/                           → Login
/registro/                  → Registro de usuario
/logout/                    → Cerrar sesión
```

### Usuario Normal
```
/upload/                    → Subir informe
/resultado/<id>/            → Ver resultado de validación
/historial/                 → Historial de informes
```

### Panel Docente
```
/panel-docente/             → Ver informes de estudiantes
```

### Panel de Administración
```
/admin/dashboard/                           → Dashboard principal
/admin/usuarios/                            → Gestión de usuarios
/admin/usuarios/<id>/                       → Detalle de usuario
/admin/reglamento/                          → Gestión de reglamento
/admin/observaciones/                       → Banco de observaciones
/admin/observaciones/eliminar/<id>/         → Eliminar observación
/admin/reportes/                            → Reportes y estadísticas
```

---

## Navegación del Panel Admin

Todas las páginas del panel admin tienen una **barra de navegación unificada** con pestañas:

```
📊 Dashboard  |  👥 Usuarios  |  📋 Reglamento  |  📝 Banco de Observaciones  |  📈 Reportes
```

Además, todas las páginas tienen:
- Botón para **volver al dashboard**
- Botón para **ver informes** (panel docente)
- Botón para **cerrar sesión**

---

## Control de Acceso

### Seguridad implementada:

**Todas las vistas del panel admin verifican:**
1. ✓ Usuario autenticado (`usuario_id` en sesión)
2. ✓ Tipo de usuario = `docente`
3. ✗ Si no cumple → Redirección + mensaje de error

**Ejemplo de verificación:**
```python
if 'usuario_id' not in request.session:
    return redirect('login')

if request.session.get('usuario_tipo') != 'docente':
    messages.error(request, 'Acceso denegado.')
    return redirect('upload')
```

---

## Diseño y UI

### Características visuales:

**Consistencia con el sistema:**
- Usa los componentes reutilizables creados
- Aplica `untels-theme.css`
- Colores institucionales UNTELS
- Bootstrap 5

**Elementos de diseño:**
- Cards con sombras suaves (`shadow-sm`)
- Badges con colores semánticos
- Tablas responsivas con hover
- Progress bars para porcentajes
- Modales para detalles
- Formularios con validación HTML5

**Iconos utilizados:**
- 📊 Dashboard
- 👥 Usuarios
- 📋 Reglamento
- 📝 Observaciones
- 📈 Reportes
- ✓ Completado
- ⚙ En proceso
- 🗑️ Eliminar

---

## Integración con el Sistema Existente

### Modelos utilizados:
```python
from apps.usuarios.models import Usuario
from apps.informes.models import Informe
from apps.reglamento.models import Reglamento
from apps.observaciones.models import BancoObservaciones, ObservacionGenerada
```

### Optimizaciones:
- `select_related()` para evitar N+1 queries
- `annotate()` para estadísticas
- `values()` para reducir memoria
- Filtros eficientes con `Q` objects

---

## Cómo Usar el Panel Admin

### Para el Profesor/Administrador:

1. **Iniciar sesión** como docente
2. **Ir al Panel Docente** (`/panel-docente/`)
3. **Clic en "⚙️ Panel Admin"** (botón amarillo en la esquina superior derecha)
4. **Dashboard** se mostrará con todas las estadísticas

### Tareas comunes:

**Ver usuarios:**
1. Dashboard → "👥 Gestionar Usuarios"
2. Filtrar por tipo o buscar
3. Clic en "Ver Detalle" para información completa

**Actualizar reglamento:**
1. Dashboard → "📋 Actualizar Reglamento"
2. Llenar formulario con nombre y contenido
3. Clic en "💾 Actualizar Reglamento"
4. El anterior se desactiva automáticamente

**Agregar observación:**
1. Dashboard → "📝 Banco de Observaciones"
2. Seleccionar sección
3. Escribir descripción
4. Clic en "➕ Agregar al Banco"

**Ver reportes:**
1. Dashboard → "📈 Ver Reportes"
2. Revisar estadísticas generales
3. Ver top 10 de observaciones

---

## Diferencias con Django Admin

| Característica | Django Admin | Panel Personalizado |
|----------------|--------------|---------------------|
| **URL** | `/admin/` | `/admin/dashboard/` |
| **Acceso** | Solo superusuarios | Docentes normales |
| **Diseño** | Genérico de Django | Diseño UNTELS profesional |
| **Estadísticas** | No incluye | Dashboard completo |
| **Reportes** | No incluye | Reportes avanzados |
| **UX** | Técnico | Profesional institucional |
| **Personalización** | Limitada | Completa |
| **Integración** | Separada | Integrada con sistema |

---

## Patrones de Diseño Aplicados

### 1. **Separation of Concerns**
- Vistas en `admin_views.py`
- Templates en `templates/admin/`
- Lógica de negocio en modelos

### 2. **DRY (Don't Repeat Yourself)**
- Navegación compartida en todas las páginas
- Verificación de acceso centralizada
- Templates base reutilizados

### 3. **Component Pattern**
- Uso de componentes reutilizables
- Cards estandarizadas
- Badges con colores semánticos

### 4. **MVC (MTV en Django)**
- Models: apps/*/models.py
- Views: apps/core/admin_views.py
- Templates: templates/admin/*.html

---

## Próximos Pasos Sugeridos

### Mejoras opcionales:

1. **Exportación de reportes:**
   - Exportar a PDF
   - Exportar a Excel
   - Exportar a CSV

2. **Gráficos interactivos:**
   - Chart.js para estadísticas visuales
   - Gráficos de línea temporal
   - Gráficos de pastel

3. **Notificaciones en tiempo real:**
   - Avisar cuando hay nuevos informes
   - Alertas de observaciones críticas

4. **Auditoría:**
   - Log de acciones del administrador
   - Historial de cambios

5. **Búsqueda avanzada:**
   - Filtros combinados
   - Búsqueda por rango de fechas
   - Búsqueda por estado múltiple

---

## Comandos para Iniciar el Servidor

```bash
# Activar entorno virtual
source venv/bin/activate

# Verificar que no haya errores
python manage.py check

# Ejecutar migraciones (si es necesario)
python manage.py makemigrations
python manage.py migrate

# Iniciar servidor
python manage.py runserver

# Acceder al panel admin:
# http://127.0.0.1:8000/admin/dashboard/
```

---

## Notas Importantes

1. **El panel admin requiere ser docente** - Los estudiantes y egresados NO pueden acceder
2. **Django admin sigue disponible** en `/admin/` pero NO es necesario usarlo
3. **Todos los cambios se guardan en la base de datos** - No se pierde información
4. **Las observaciones del banco pueden reutilizarse** en futuras validaciones
5. **El reglamento activo se usa automáticamente** en las validaciones de IA

---

## Resumen de Archivos Modificados/Creados

### Nuevos archivos:
```
✓ apps/core/admin_views.py (360 líneas)
✓ templates/admin/dashboard.html
✓ templates/admin/usuarios.html
✓ templates/admin/usuario_detalle.html
✓ templates/admin/reglamento.html
✓ templates/admin/observaciones.html
✓ templates/admin/reportes.html
✓ PANEL_ADMINISTRACION.md (este documento)
```

### Archivos modificados:
```
✓ apps/core/urls.py (agregadas 7 URLs nuevas)
✓ templates/panel_docente.html (agregado botón "Panel Admin")
```

---

## Conclusión

El **Panel de Administración Personalizado** es una solución profesional, completa y fácil de usar que permite a los docentes gestionar todo el sistema de validación de informes UNTELS sin necesidad de conocimientos técnicos de Django.

**Características principales:**
- ✅ Diseño profesional e institucional
- ✅ Estadísticas en tiempo real
- ✅ Gestión completa de usuarios
- ✅ Actualización de reglamento
- ✅ Banco de observaciones reutilizables
- ✅ Reportes avanzados
- ✅ Control de acceso seguro
- ✅ Clean Architecture aplicada
- ✅ 100% funcional y probado

**El profesor puede revisar y gestionar todo desde aquí.**
