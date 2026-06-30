# Acceso al Panel de Administración - Guía Rápida

## Cómo Acceder al Panel Admin

### Opción 1: Desde el Panel Docente (Recomendado)

1. Inicia sesión como **docente**
2. Ve al Panel Docente: http://127.0.0.1:8000/panel-docente/
3. Clic en el botón **"⚙️ Panel Admin"** (botón amarillo en la esquina superior derecha)
4. Serás redirigido al Dashboard del panel admin

### Opción 2: Acceso Directo

1. Inicia sesión como **docente**
2. Accede directamente a: http://127.0.0.1:8000/admin/dashboard/

---

## URLs Principales del Panel Admin

```
Dashboard:                  http://127.0.0.1:8000/admin/dashboard/
Gestión de Usuarios:        http://127.0.0.1:8000/admin/usuarios/
Gestión de Reglamento:      http://127.0.0.1:8000/admin/reglamento/
Banco de Observaciones:     http://127.0.0.1:8000/admin/observaciones/
Reportes y Estadísticas:    http://127.0.0.1:8000/admin/reportes/
```

---

## Requisitos

- ✅ Estar autenticado en el sistema
- ✅ Tener tipo de usuario = **"docente"**
- ❌ Estudiantes y egresados NO pueden acceder

---

## Qué Puedes Hacer en Cada Sección

### 📊 Dashboard
- Ver estadísticas generales del sistema
- Ver informes recientes
- Ver secciones con más observaciones
- Accesos rápidos a todas las funcionalidades

### 👥 Gestión de Usuarios
- Ver lista completa de usuarios
- Filtrar por tipo (estudiante, egresado, docente)
- Buscar por código o nombre
- Ver detalle de cada usuario
- Ver historial de informes por usuario

### 📋 Gestión de Reglamento
- Crear nuevo reglamento
- Ver historial de reglamentos
- Ver contenido completo de cada versión
- El nuevo reglamento se activa automáticamente

### 📝 Banco de Observaciones
- Agregar nuevas observaciones
- Ver todas las observaciones por sección
- Eliminar observaciones
- Ver estadísticas de distribución

### 📈 Reportes y Estadísticas
- Informes por estado (enviado, en revisión, completado)
- Informes por tipo de usuario
- Top 10 usuarios más activos
- Top 10 observaciones más frecuentes
- Resumen general del sistema

---

## Iniciar el Servidor

```bash
# En la terminal, navega al directorio del proyecto
cd /home/chapitec/Documents/chapitec/andre/T.A-Arquitectura-de-software/proyecto_untels

# Activa el entorno virtual
source venv/bin/activate

# Inicia el servidor
python manage.py runserver

# Abre el navegador en:
# http://127.0.0.1:8000/
```

---

## Credenciales de Docente

Si necesitas crear un usuario docente:

```bash
# Desde la terminal con el entorno virtual activado
python manage.py shell
```

```python
from apps.usuarios.models import Usuario

# Crear docente
Usuario.objects.create(
    codigo='D001',
    nombre='Profesor Admin',
    tipo_usuario='docente',
    password='password123'  # Cambia esto por una contraseña segura
)
```

O usa el formulario de registro en: http://127.0.0.1:8000/registro/

---

## Navegación Rápida

Una vez dentro del panel admin, encontrarás:

**Barra de navegación superior:**
```
📊 Dashboard  |  👥 Usuarios  |  📋 Reglamento  |  📝 Banco de Observaciones  |  📈 Reportes
```

**Botones de acción:**
- **Ver Informes** → Te lleva al Panel Docente
- **Inicio** → Te lleva a la página de subir informes
- **Cerrar Sesión** → Cierra tu sesión

---

## Tareas Comunes

### Actualizar el Reglamento

1. Panel Admin → 📋 Reglamento
2. Llenar el formulario:
   - Nombre: "Reglamento 2024 - Versión 2.0"
   - Contenido: (pegar el contenido completo)
3. Clic en "💾 Actualizar Reglamento"

### Ver Detalle de un Usuario

1. Panel Admin → 👥 Usuarios
2. (Opcional) Filtrar por tipo o buscar
3. Clic en "Ver Detalle →" del usuario que deseas ver
4. Verás:
   - Información del usuario
   - Estadísticas personales
   - Historial completo de informes

### Agregar una Observación al Banco

1. Panel Admin → 📝 Banco de Observaciones
2. Seleccionar sección (ej: "Portada")
3. Escribir descripción (ej: "Falta el logo de UNTELS")
4. Clic en "➕ Agregar al Banco"

### Ver Estadísticas del Sistema

1. Panel Admin → 📈 Reportes
2. Revisar:
   - Distribución de informes por estado
   - Informes por tipo de usuario
   - Usuarios más activos
   - Observaciones más comunes

---

## Diferencias con Django Admin

**NO uses el Django Admin (`/admin/`)** - Usa el Panel Admin Personalizado (`/admin/dashboard/`)

| Django Admin | Panel Admin Personalizado |
|--------------|---------------------------|
| `/admin/` | `/admin/dashboard/` |
| Solo superusuarios | Docentes normales |
| Diseño genérico | Diseño UNTELS |
| Sin estadísticas | Dashboard completo |
| Limitado | Funcionalidad completa |

---

## Solución de Problemas

### "Acceso denegado"
- ✅ Verifica que iniciaste sesión como **docente**
- ✅ Verifica que tu sesión no haya expirado

### "Page not found"
- ✅ Verifica que el servidor esté corriendo
- ✅ Verifica que la URL sea correcta: `/admin/dashboard/`

### No se ven estadísticas
- ✅ Si es la primera vez, es normal no tener datos
- ✅ Sube algunos informes primero para ver estadísticas

---

## Contacto y Soporte

Si tienes problemas:
1. Verifica que el servidor esté corriendo
2. Verifica que estés autenticado como docente
3. Revisa la terminal por errores
4. Consulta `PANEL_ADMINISTRACION.md` para documentación completa

---

**¡Listo! Ya puedes gestionar todo el sistema desde el Panel de Administración.**
