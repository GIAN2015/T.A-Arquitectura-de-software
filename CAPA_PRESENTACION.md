# CAPA DE PRESENTACIÓN

Sistema de Validación de Informes - UNTELS

---

## ¿QUÉ ES LA CAPA DE PRESENTACIÓN?

Es **todo lo que el usuario VE y con lo que INTERACTÚA**.

- Templates HTML
- Formularios
- Tablas
- Botones
- Estilos (CSS/Bootstrap)

**Ubicación:** `proyecto_untels/templates/`

---

## ARCHIVOS DE ESTA CAPA

```
proyecto_untels/templates/
├── base.html                    # ← Template base con navbar y estilos
├── login.html                   # ← Página de inicio de sesión
├── registro.html                # ← Página de registro de usuarios
├── upload_report.html           # ← Página para subir informes
├── validation_result.html       # ← Página de resultados de validación
├── historial.html               # ← Página de historial de informes
└── panel_docente.html           # ← Panel administrativo para docentes
```

**Total:** 7 archivos HTML

---

## DESCRIPCIÓN DE CADA TEMPLATE

### 1. base.html (62 líneas)

**Propósito:** Template base que heredan todos los demás

**Contenido:**
- Navbar con logo UNTELS
- Estilos CSS personalizados (colores UNTELS: azul #1a3a6b, dorado #f0a500)
- Bootstrap 5.3 CDN
- Sistema de mensajes flash (success/error/warning)
- Block `{% block content %}` para contenido específico

**Ubicación:** `/home/chapitec/Documents/chapitec/andre/T.A-Arquitectura-de-software/proyecto_untels/templates/base.html`

**Estructura:**
```html
<!DOCTYPE html>
<html>
<head>
    <!-- Bootstrap 5.3 -->
    <!-- Estilos UNTELS personalizados -->
</head>
<body>
    <nav>🎓 Sistema de Validación de Informes – UNTELS</nav>
    
    <div class="container">
        <!-- Mensajes flash -->
        {% block content %}{% endblock %}
    </div>
    
    <!-- Bootstrap JS -->
</body>
</html>
```

---

### 2. login.html (52 líneas)

**Propósito:** Página de inicio de sesión

**Ruta:** `/` (raíz del sitio)

**Formulario:**
```html
<form method="POST">
    📌 Código Universitario
    🔒 Contraseña (opcional para modo legacy)
    👤 Nombre Completo (opcional si se usa contraseña)
    
    [Botón: Iniciar Sesión →]
</form>

<a href="/registro/">¿No tienes cuenta? Regístrate aquí</a>
```

**Características:**
- Soporte dual: con contraseña o modo legacy
- Validación en frontend (campos requeridos)
- Mensaje de ayuda para usuarios sin contraseña
- Link a página de registro

**Ubicación:** `/home/chapitec/Documents/chapitec/andre/T.A-Arquitectura-de-software/proyecto_untels/templates/login.html`

---

### 3. registro.html (68 líneas)

**Propósito:** Registro de nuevos usuarios

**Ruta:** `/registro/`

**Formulario:**
```html
<form method="POST">
    📝 Código Universitario
    👤 Nombre Completo
    📊 Tipo de Usuario [Dropdown]
        ▫ Estudiante
        ▫ Egresado
        ▫ Docente
    🔒 Contraseña (mínimo 6 caracteres)
    🔒 Confirmar Contraseña
    
    [Botón: Registrarse]
</form>

<a href="/">¿Ya tienes cuenta? Inicia sesión</a>
```

**Validaciones:**
- Código no duplicado (backend)
- Contraseñas coinciden (backend)
- Mínimo 6 caracteres (frontend + backend)

**Ubicación:** `/home/chapitec/Documents/chapitec/andre/T.A-Arquitectura-de-software/proyecto_untels/templates/registro.html`

---

### 4. upload_report.html (67 líneas)

**Propósito:** Subir informe para validación

**Ruta:** `/upload/`

**Requiere:** Usuario autenticado

**Interfaz:**
```html
┌─────────────────────────────────┐
│  Carga de Informe de Prácticas  │
├─────────────────────────────────┤
│ 📋 Información del Usuario      │
│   Código: 2021101234             │
│   Tipo: Estudiante               │
│   Nombre: Juan Pérez             │
├─────────────────────────────────┤
│ 📁 Seleccionar Informe           │
│   [Elegir archivo .docx]         │
│                                  │
│   [⚙️ Validar Informe]          │
└─────────────────────────────────┘

Enlaces:
• Ver mi Historial
• Panel Docente (solo si es docente)
• Cerrar Sesión
```

**Validación:**
- Solo archivos .docx
- Tamaño máximo: configurado en Django settings

**Ubicación:** `/home/chapitec/Documents/chapitec/andre/T.A-Arquitectura-de-software/proyecto_untels/templates/upload_report.html`

---

### 5. validation_result.html (102 líneas)

**Propósito:** Mostrar resultados de la validación con observaciones de la IA

**Ruta:** `/resultado/<informe_id>/`

**Interfaz:**
```html
┌──────────────────────────────────────────────┐
│  Resultado de Validación                     │
├──────────────────────────────────────────────┤
│ 📄 Informe: informe_practicas.docx           │
│ 👤 Estudiante: Juan Pérez (2021101234)       │
│ 📅 Fecha: 16/06/2026 22:30                   │
│ 🏷️ Estado: [Completado] ✓                   │
├──────────────────────────────────────────────┤
│ 📋 Observaciones Encontradas: 3              │
│                                              │
│ ┌──────────────────────────────────────────┐ │
│ │ ID │ Sección      │ Observación         │ │
│ ├────┼──────────────┼─────────────────────┤ │
│ │ 1  │ Introducción │ Falta objetivo      │ │
│ │    │              │ general             │ │
│ │    │              │ 📍 Ubicación:       │ │
│ │    │              │    Introducción     │ │
│ ├────┼──────────────┼─────────────────────┤ │
│ │ 2  │ Desarrollo   │ No menciona         │ │
│ │    │              │ competencias        │ │
│ │    │              │ 📍 Ubicación:       │ │
│ │    │              │    Cap. 2           │ │
│ ├────┼──────────────┼─────────────────────┤ │
│ │ 3  │ Conclusiones │ No relaciona con    │ │
│ │    │              │ objetivos           │ │
│ │    │              │ 📍 Ubicación:       │ │
│ │    │              │    Conclusiones     │ │
│ └──────────────────────────────────────────┘ │
│                                              │
│ [← Volver al inicio]                         │
└──────────────────────────────────────────────┘
```

**Elementos:**
- Card con información del informe
- Badge de estado (Enviado/En Revisión/Completado)
- Tabla responsive con observaciones
- Colores por sección
- Ubicación específica del error

**Ubicación:** `/home/chapitec/Documents/chapitec/andre/T.A-Arquitectura-de-software/proyecto_untels/templates/validation_result.html`

---

### 6. historial.html (76 líneas)

**Propósito:** Ver historial de informes del usuario

**Ruta:** `/historial/`

**Requiere:** Usuario autenticado

**Interfaz:**
```html
┌───────────────────────────────────────────────────────────┐
│  Historial de Informes                                    │
│  Juan Pérez - 2021101234                                  │
│                                                           │
│  [Subir Nuevo Informe] [Panel Docente] [Cerrar Sesión]   │
├───────────────────────────────────────────────────────────┤
│                                                           │
│ ┌───────────────────────────────────────────────────────┐ │
│ │ Archivo │ Fecha      │ Estado      │ Obs. │ Acciones │ │
│ ├─────────┼────────────┼─────────────┼──────┼──────────┤ │
│ │ inf.docx│ 16/06 22:30│ Completado ✓│  3   │ [Ver]    │ │
│ │ inf2.docx│ 15/06 18:15│ En Revisión│  -   │ [Ver]    │ │
│ │ inf3.docx│ 14/06 10:00│ Enviado    │  -   │ [Ver]    │ │
│ └───────────────────────────────────────────────────────┘ │
│                                                           │
│ O (si no hay informes):                                   │
│ "No has subido ningún informe aún"                        │
│ [Subir mi Primer Informe]                                 │
└───────────────────────────────────────────────────────────┘
```

**Características:**
- Tabla ordenada por fecha (más reciente primero)
- Badges de color por estado
- Contador de observaciones
- Botón "Ver Resultado" lleva a validation_result.html
- Navegación rápida a otras secciones

**Ubicación:** `/home/chapitec/Documents/chapitec/andre/T.A-Arquitectura-de-software/proyecto_untels/templates/historial.html`

---

### 7. panel_docente.html (99 líneas)

**Propósito:** Panel administrativo para revisar todos los informes

**Ruta:** `/panel-docente/`

**Requiere:** Usuario autenticado Y tipo = 'docente'

**Interfaz:**
```html
┌─────────────────────────────────────────────────────────────────┐
│  Panel del Docente                                              │
│  Revisión de Informes de Estudiantes                            │
│                                                                 │
│  [Inicio] [Mi Historial] [Cerrar Sesión]                       │
├─────────────────────────────────────────────────────────────────┤
│  Total de informes: 15                                          │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ Estudiante │ Código │ Tipo │ Archivo │ Fecha │ Estado │ Obs│ │
│ ├────────────┼────────┼──────┼─────────┼───────┼────────┼────┤ │
│ │ Juan Pérez │2021..  │[E]   │ inf.docx│16/06  │Compl. ✓│ 3  │ │
│ │ María L.   │2022..  │[E]   │ prac.doc│15/06  │En Rev. │ -  │ │
│ │ Pedro S.   │2019..  │[EG]  │ final.do│14/06  │Enviado │ -  │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ [E] = Estudiante, [EG] = Egresado                               │
│                                                                 │
│ Badge rojo si hay observaciones, verde si 0 observaciones       │
└─────────────────────────────────────────────────────────────────┘
```

**Características:**
- Vista de TODOS los informes del sistema
- Información del estudiante (nombre, código, tipo)
- Filtrado visual por tipo de usuario
- Contador total de informes
- Badge de alerta si hay observaciones
- Botón "Ver Detalle" lleva a validation_result.html
- **Control de acceso:** redirige si no es docente

**Ubicación:** `/home/chapitec/Documents/chapitec/andre/T.A-Arquitectura-de-software/proyecto_untels/templates/panel_docente.html`

---

## ESTILOS Y DISEÑO

### Colores UNTELS

```css
--untels-blue: #1a3a6b;    /* Azul institucional */
--untels-gold: #f0a500;    /* Dorado institucional */
```

### Badges de Estado

```css
.badge-enviado    → Gris     (bg-secondary)
.badge-en_revision → Amarillo (bg-warning)
.badge-completado → Verde    (bg-success)
```

### Badges de Tipo de Usuario

```css
.badge-estudiante → Azul UNTELS
.badge-egresado   → Gris oscuro
.badge-docente    → Verde
```

---

## NAVEGACIÓN ENTRE PÁGINAS

```
       [login.html]
            │
    ┌───────┴────────┐
    │                │
[registro.html]   ┌──▼──────────────┐
                  │ upload_report   │
                  │                 │
                  │ [Validar]       │
                  └────┬─────┬──────┘
                       │     │
           ┌───────────┘     └────────────┐
           │                              │
      [validation_result]          [historial.html]
                                          │
                                          │
                                   [panel_docente]
                                   (solo docentes)
```

---

## MENSAJES FLASH

Los templates usan el sistema de mensajes de Django:

```html
{% if messages %}
  {% for message in messages %}
    <div class="alert alert-{{ message.tags }}">
      {{ message }}
    </div>
  {% endfor %}
{% endif %}
```

**Tipos de mensajes:**
- `success` (verde): "Registro exitoso"
- `error` (rojo): "Código o contraseña incorrectos"
- `warning` (amarillo): "Acceso denegado"
- `info` (azul): Mensajes informativos

---

## RESPONSIVE DESIGN

Todos los templates usan Bootstrap 5.3, son responsive y funcionan en:

- ✓ Desktop (1920x1080)
- ✓ Tablet (768x1024)
- ✓ Móvil (375x667)

**Clases Bootstrap usadas:**
- `container`, `row`, `col-md-*`
- `card`, `card-body`, `card-header`
- `table-responsive`
- `btn`, `form-control`, `form-select`

---

## VALIDACIÓN EN FRONTEND

```html
<!-- Campos requeridos -->
<input type="text" name="codigo" required>

<!-- Tipos de input -->
<input type="password" name="password">
<input type="file" accept=".docx">

<!-- Longitud mínima -->
<input type="password" minlength="6">
```

---

## INTERACCIÓN CON CAPA DE NEGOCIO

Los templates NO tienen lógica de negocio. Solo:

1. **Reciben datos** desde las vistas (contexto)
2. **Muestran datos** con template tags de Django
3. **Envían datos** via formularios POST

**Ejemplo:**
```html
<!-- RECIBE datos de la vista -->
{{ usuario.nombre }}
{{ informe.estado }}

<!-- ENVÍA datos a la vista -->
<form method="POST">
    {% csrf_token %}
    <input name="codigo">
    <button type="submit">Enviar</button>
</form>
```

---

## RESUMEN

| Template | Propósito | Requiere Login | Requiere Rol |
|----------|-----------|----------------|--------------|
| base.html | Template base | No | - |
| login.html | Iniciar sesión | No | - |
| registro.html | Crear cuenta | No | - |
| upload_report.html | Subir informe | ✓ Sí | - |
| validation_result.html | Ver resultados | ✓ Sí | - |
| historial.html | Ver historial | ✓ Sí | - |
| panel_docente.html | Panel admin | ✓ Sí | ✓ Docente |

**Total:** 7 templates, 526 líneas HTML

---

**Esta es la CAPA DE PRESENTACIÓN completa.**

**Siguiente:** Lee `CAPA_NEGOCIO.md` para entender la lógica de aplicación.
