# CLEAN ARCHITECTURE - SISTEMA DE COMPONENTES REUTILIZABLES

Sistema de Validación de Informes - UNTELS

---

## PRINCIPIOS DE CLEAN ARCHITECTURE APLICADOS

### 1. Separación de Responsabilidades

```
ANTES (mezclado):
templates/login.html → HTML + CSS inline + lógica de alertas

AHORA (separado):
templates/login.html → Solo estructura HTML
templates/components/alert.html → Componente reutilizable
static/css/untels-theme.css → Estilos centralizados
```

### 2. Componentes Reutilizables (DRY - Don't Repeat Yourself)

**Creamos 5 componentes base que se usan en TODO el sistema:**

---

## COMPONENTES DISPONIBLES

### 1. Alert (Notificaciones Formales)

**Archivo:** `templates/components/alert.html`

**Características:**
- ✅ Diseño formal y profesional
- ✅ 4 tipos: error (rojo), success (verde), warning (amarillo), info (azul)
- ✅ Título + Mensaje + Detalles opcionales
- ✅ Ícono personalizable
- ✅ Borde izquierdo de color
- ✅ Botón de cerrar
- ✅ Sombra sutil

**Uso:**
```django
{% include 'components/alert.html' with 
   type='error' 
   title='Error de Validación' 
   message='El archivo no cumple con el formato requerido'
   details='Solo se aceptan archivos .docx de máximo 10MB' 
%}
```

**Tipos disponibles:**
- `error` → Rojo con ✕
- `success` → Verde con ✓
- `warning` → Amarillo con ⚠
- `info` → Azul con ℹ

**Ejemplo visual:**
```
┌─────────────────────────────────────────────┐
│ ✕  Error de Validación                     │ │
│    El archivo no cumple con el formato     │
│    requerido                               │
│    ───────────────────────────────────────  │
│    Solo se aceptan archivos .docx de      │
│    máximo 10MB                             │
└─────────────────────────────────────────────┘
```

---

### 2. Card (Tarjeta Formal)

**Archivo:** `templates/components/card.html`

**Características:**
- ✅ Header con color institucional UNTELS
- ✅ Título + Subtítulo
- ✅ Ícono opcional
- ✅ Cuerpo con padding consistente
- ✅ Footer opcional
- ✅ Sombra elevada

**Uso:**
```django
<div>
  {% include 'components/card.html' with 
     title='Carga de Informe' 
     subtitle='Suba su archivo .docx'
     icon='📄'
  %}
    <form>...</form>
  {% endinclude %}
</div>
```

**O con bloques:**
```django
{% load static %}
<div class="card">
  <div class="card-header-untels">
    <h5>{{ title }}</h5>
  </div>
  <div class="card-body">
    {{ content }}
  </div>
</div>
```

---

### 3. Table (Tabla Formal)

**Archivo:** `templates/components/table.html`

**Características:**
- ✅ Headers con fondo gris claro
- ✅ Borde inferior azul UNTELS
- ✅ Filas alternadas (striped)
- ✅ Efecto hover
- ✅ Mensaje cuando está vacía
- ✅ Responsive

**Uso:**
```django
{% include 'components/table.html' with 
   headers=headers_list 
   data=data_rows
   empty_message='No hay informes registrados'
%}
```

**Ejemplo de datos:**
```python
# En la vista
headers = ['Archivo', 'Fecha', 'Estado', 'Acciones']
data = [
    ['informe.docx', '16/06/2026', badge_html, button_html],
    ['practica.docx', '15/06/2026', badge_html, button_html],
]
```

---

### 4. Badge (Etiquetas de Estado)

**Archivo:** `templates/components/badge.html`

**Características:**
- ✅ 6 tipos de colores
- ✅ Ícono + Texto
- ✅ 3 tamaños (sm, md, lg)
- ✅ Padding consistente
- ✅ Fuente en mayúsculas

**Uso:**
```django
{% include 'components/badge.html' with type='success' text='Completado' icon='✓' %}
{% include 'components/badge.html' with type='warning' text='En Revisión' size='sm' %}
{% include 'components/badge.html' with type='danger' text='Error' %}
```

**Tipos:**
- `primary` → Azul UNTELS
- `success` → Verde
- `danger` → Rojo
- `warning` → Amarillo
- `info` → Celeste
- `secondary` → Gris

---

### 5. Button (Botones Formales)

**Archivo:** `templates/components/button.html`

**Características:**
- ✅ Diseño consistente
- ✅ Ícono + Texto
- ✅ Múltiples variantes
- ✅ 3 tamaños
- ✅ Soporte para disabled
- ✅ Tipo link o submit

**Uso:**
```django
{# Botón normal #}
{% include 'components/button.html' with 
   type='untels' 
   text='Guardar' 
   icon='💾' 
   form_submit=True 
%}

{# Botón link #}
{% include 'components/button.html' with 
   type='outline-primary' 
   text='Ver Historial' 
   href='/historial/' 
%}

{# Botón deshabilitado #}
{% include 'components/button.html' with 
   type='secondary' 
   text='No disponible' 
   disabled=True 
%}
```

**Tipos:**
- `untels` → Azul institucional (recomendado)
- `primary` → Azul Bootstrap
- `success` → Verde
- `danger` → Rojo
- `warning` → Amarillo
- `secondary` → Gris
- `outline-primary` → Borde azul, fondo transparente

**Tamaños:**
- `sm` → Pequeño
- `md` → Mediano (default)
- `lg` → Grande

---

## SISTEMA DE ESTILOS (CSS)

### Archivo: `static/css/untels-theme.css`

**Características:**
- ✅ 450+ líneas de CSS profesional
- ✅ Variables CSS (Design System)
- ✅ Responsive design
- ✅ Accesibilidad (WCAG 2.1)
- ✅ Print styles
- ✅ Animaciones suaves
- ✅ Tema oscuro preparado (futuro)

### Variables CSS Definidas

```css
:root {
  /* Colores Institucionales */
  --untels-blue: #1a3a6b;
  --untels-blue-dark: #0f2342;
  --untels-blue-light: #2d5a9b;
  --untels-gold: #f0a500;
  
  /* Estados */
  --color-success: #198754;
  --color-danger: #dc3545;
  --color-warning: #ffc107;
  --color-info: #0dcaf0;
  
  /* Sombras */
  --shadow-sm: 0 2px 4px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.08);
  --shadow-lg: 0 8px 24px rgba(0,0,0,0.12);
  
  /* Espaciado */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
  
  /* Bordes */
  --border-radius: 0.375rem;
  --border-radius-lg: 0.5rem;
  
  /* Transiciones */
  --transition-base: all 0.2s ease-in-out;
}
```

### Clases Utilitarias Personalizadas

```css
.text-untels-blue    /* Color de texto azul UNTELS */
.bg-untels-blue      /* Fondo azul UNTELS */
.text-untels-gold    /* Color de texto dorado */
.bg-untels-gold      /* Fondo dorado */
.shadow-untels       /* Sombra mediana */
.shadow-untels-lg    /* Sombra grande */
.btn-untels          /* Botón institucional */
.navbar-untels       /* Navbar con gradiente */
.card-header-untels  /* Header de card formal */
```

---

## NOTIFICACIONES FORMALES

### Sistema de Mensajes Mejorado

**ANTES:**
```html
<div class="alert alert-danger">
  Error
</div>
```

**AHORA:**
```django
{% include 'components/alert.html' with 
   type='error' 
   title='Error de Validación del Documento' 
   message='El archivo cargado no cumple con los requisitos establecidos en el Reglamento de Prácticas Preprofesionales'
   details='Motivo específico: El documento debe estar en formato .docx y no exceder los 10MB de tamaño'
%}
```

**Resultado visual más formal:**
```
┌───────────────────────────────────────────────────────┐
│  ✕  ERROR DE VALIDACIÓN DEL DOCUMENTO              [x]│
│                                                        │
│  El archivo cargado no cumple con los requisitos      │
│  establecidos en el Reglamento de Prácticas          │
│  Preprofesionales                                     │
│  ─────────────────────────────────────────────────    │
│  Motivo específico: El documento debe estar en        │
│  formato .docx y no exceder los 10MB de tamaño       │
└───────────────────────────────────────────────────────┘
```

---

## ESTRUCTURA DE ARCHIVOS

```
proyecto_untels/
├── templates/
│   ├── components/              ← NUEVOS COMPONENTES
│   │   ├── alert.html           ← Notificaciones formales
│   │   ├── card.html            ← Tarjetas
│   │   ├── table.html           ← Tablas
│   │   ├── badge.html           ← Etiquetas
│   │   └── button.html          ← Botones
│   ├── base.html                ← ACTUALIZADO (usa CSS externo)
│   ├── login.html               ← ACTUALIZADO (usa componentes)
│   ├── registro.html
│   ├── upload_report.html
│   ├── validation_result.html
│   ├── historial.html
│   └── panel_docente.html
│
├── static/
│   ├── css/
│   │   └── untels-theme.css     ← NUEVO (450+ líneas)
│   ├── js/                      ← Para JavaScript futuro
│   └── img/                     ← Para imágenes
│
└── staticfiles/                 ← Generado por collectstatic
    └── css/
        └── untels-theme.css
```

---

## CÓMO USAR LOS COMPONENTES

### Paso 1: Incluir el componente

```django
{% include 'components/alert.html' with type='error' title='Título' message='Mensaje' %}
```

### Paso 2: Pasar parámetros

Parámetros obligatorios:
- `type` → Tipo de componente
- `text` o `message` → Contenido

Parámetros opcionales:
- `title` → Título (para alerts y cards)
- `icon` → Ícono personalizado
- `size` → Tamaño (sm, md, lg)
- `details` → Información adicional

### Paso 3: Personalizar si es necesario

Los componentes aceptan clases adicionales:

```django
<div class="my-custom-class">
  {% include 'components/alert.html' with ... %}
</div>
```

---

## EJEMPLO COMPLETO: Página de Login

**ANTES (sin componentes):**
```html
{% extends 'base.html' %}
{% block content %}
<div class="card">
  <div style="background: #1a3a6b; color: white;">
    <h5>Login</h5>
  </div>
  <div class="card-body">
    <form>...</form>
    <button class="btn btn-primary">Entrar</button>
  </div>
</div>
{% endblock %}
```

**AHORA (con componentes y Clean Architecture):**
```django
{% extends 'base.html' %}
{% block title %}Iniciar Sesión{% endblock %}

{% block content %}
<div class="row justify-content-center mt-5">
  <div class="col-lg-5">
    <!-- Encabezado formal -->
    <div class="text-center mb-4">
      <h2 class="fw-bold text-untels-blue">Autenticación de Usuario</h2>
      <p class="text-muted">Sistema Institucional</p>
    </div>

    <!-- Card usando estilos predefinidos -->
    <div class="card shadow-untels">
      <div class="card-header-untels">
        <h5>🔐 Inicio de Sesión</h5>
        <small class="text-white-50">Credenciales institucionales</small>
      </div>
      <div class="card-body p-4">
        <form method="POST">
          {% csrf_token %}
          
          <div class="mb-4">
            <label class="form-label">Código Universitario *</label>
            <input type="text" name="codigo" class="form-control" required>
          </div>
          
          <div class="mb-4">
            <label class="form-label">Contraseña</label>
            <input type="password" name="password" class="form-control">
          </div>
          
          <!-- Botón usando componente -->
          {% include 'components/button.html' with 
             type='untels' 
             text='Iniciar Sesión' 
             icon='→' 
             form_submit=True 
             size='lg' 
          %}
        </form>
      </div>
    </div>
  </div>
</div>
{% endblock %}
```

---

## VENTAJAS DE ESTA ARQUITECTURA

### 1. **Reutilización**
Un componente se crea una vez y se usa en TODO el sistema.

### 2. **Mantenimiento**
Cambiar el diseño de alertas → Solo editas `alert.html`

### 3. **Consistencia**
Todas las alertas, tablas, botones se ven igual en todo el sistema.

### 4. **Escalabilidad**
Agregar nuevas páginas es más rápido (usas los componentes existentes).

### 5. **Testing**
Componentes aislados son más fáciles de testear.

### 6. **Performance**
CSS separado se cachea en el navegador.

### 7. **Formalidad**
Diseño profesional y consistente en todas las páginas.

---

## MEJORES PRÁCTICAS

### ✅ DO (Hacer):

```django
<!-- Usar componentes -->
{% include 'components/alert.html' with type='error' message='...' %}

<!-- Usar variables CSS -->
<div style="background-color: var(--untels-blue);">

<!-- Usar clases del tema -->
<button class="btn-untels">Guardar</button>
```

### ❌ DON'T (No hacer):

```django
<!-- NO mezclar estilos inline -->
<div style="background: #1a3a6b; padding: 20px;">

<!-- NO duplicar código de alertas -->
<div class="alert alert-danger">Error</div>

<!-- NO usar colores hardcodeados -->
<button style="background-color: #dc3545;">
```

---

## PRÓXIMOS COMPONENTES A CREAR

1. **Modal** → Para confirmaciones
2. **Dropdown** → Menús desplegables
3. **Breadcrumb** → Navegación
4. **Pagination** → Paginación de tablas
5. **Progress Bar** → Barra de progreso
6. **Toast** → Notificaciones temporales
7. **Spinner** → Indicador de carga

---

## COMANDOS ÚTILES

### Recopilar archivos estáticos
```bash
python manage.py collectstatic --noinput
```

### Ver archivos estáticos servidos
```bash
ls -la staticfiles/css/
```

### Verificar que CSS se carga
```bash
# En el navegador
View Page Source → buscar "untels-theme.css"
```

---

## RESUMEN

✅ **Componentes creados:** 5 (alert, card, table, badge, button)
✅ **CSS centralizado:** 450+ líneas en untels-theme.css
✅ **Variables CSS:** 30+ variables (colores, sombras, espaciado)
✅ **Base.html actualizado:** Usa CSS externo, footer, metadata
✅ **Login actualizado:** Más formal, usa componentes
✅ **Notificaciones:** Formales con título + mensaje + detalles

**Próximo paso:** Actualizar los demás templates para usar los componentes.

---

**Sistema diseñado con Clean Architecture - UNTELS 2.0**
