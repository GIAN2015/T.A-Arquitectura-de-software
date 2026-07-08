# 🎨 Frontend - Sistema de Validación UNTELS

> Documentación de la capa de presentación

## Tecnologías

- **Bootstrap 5.3** - Framework CSS
- **Bootstrap Icons** - Iconografía
- **JavaScript Vanilla** - Interactividad
- **Django Templates** - Motor de plantillas

## Estructura

```
frontend/
├── templates/
│   ├── base.html              # Template base legacy
│   ├── base_v2.html           # Template base moderno
│   ├── estudiante/            # UI Estudiantes
│   ├── docente/               # UI Docentes  
│   ├── presidente/            # UI Presidentes
│   ├── secretaria/            # UI Secretarias
│   └── admin/                 # UI Admin
└── static/
    ├── css/
    ├── js/
    └── images/
```

## Paleta de Colores

```css
--untels-blue: #1a3a6b;     /* Azul UNTELS oficial */
--primary: #0d6efd;         /* Bootstrap primary */
--success: #198754;
--warning: #ffc107;
--danger: #dc3545;
```

## Componentes Principales

### 1. Dashboard por Rol

Cada rol tiene su propio dashboard con:
- Cards de estadísticas
- Tablas de informes
- Notificaciones
- Acciones rápidas

### 2. Modales

- Selección de banco de observaciones
- Confirmación de acciones
- Vista previa de dictámenes
- Re-validación con IA

### 3. Formularios

- Subir informe (estudiante)
- Confirmar observaciones (docente)
- Aprobar/rechazar (presidente)
- Derivar informes (secretaria)

## JavaScript

### Progreso de Validación IA

```javascript
// Simulación de progreso durante validación
const messages = [
  { sec: 0, msg: 'Leyendo banco...', progress: 5 },
  { sec: 4, msg: 'Conectando con IA...', progress: 15 },
  { sec: 10, msg: 'Analizando informe...', progress: 40 },
  // ...
];
```

## Templates Django

### Herencia

```django
{% extends 'docente/base_docente.html' %}
{% load dictamen_filters %}

{% block content %}
  {{ informe.comentario_docente|formatear_dictamen }}
{% endblock %}
```

---

**Ver también**: [Backend](BACKEND.md)
