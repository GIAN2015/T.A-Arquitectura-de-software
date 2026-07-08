# 🎨 Frontend - Sistema de Validación UNTELS

> Documentación completa de la capa de presentación

---

## 📋 Tabla de Contenidos

1. [Tecnologías](#tecnologías)
2. [Estructura Completa](#estructura-completa)
3. [Paleta de Colores](#paleta-de-colores)
4. [Componentes Principales](#componentes-principales)
5. [Dashboards por Rol](#dashboards-por-rol)
6. [JavaScript y Funcionalidades](#javascript-y-funcionalidades)
7. [Templates Django](#templates-django)

---

## 🛠️ Tecnologías

### Core
- **Bootstrap 5.3** - Framework CSS moderno
- **Bootstrap Icons 1.11** - Iconografía completa
- **JavaScript Vanilla ES6+** - Sin dependencias de jQuery
- **Django Templates 4.2** - Motor de plantillas server-side

### Librerías Adicionales
- **SweetAlert2** - Modales y alertas personalizadas (opcional)
- **Chart.js** - Gráficos estadísticos (en dashboard admin)
- **Flatpickr** - Date picker (futuro)

---

## 📁 Estructura Completa

```
frontend/
├── templates/
│   │
│   ├── base.html                    # Template base legacy (v1.0)
│   ├── base_v2.html                 # Template base moderno (v2.0+)
│   │                                # Incluye:
│   │                                # - Navbar responsive
│   │                                # - Sidebar colapsable
│   │                                # - Área de notificaciones
│   │                                # - Footer
│   │
│   ├── login.html                   # Página de inicio de sesión
│   │                                # - Form con validación
│   │                                # - Recordar sesión
│   │                                # - Logo UNTELS
│   │
│   ├── estudiante/                  # 🎓 UI para Estudiantes
│   │   ├── base_estudiante.html    # Hereda base_v2, navbar específico
│   │   ├── dashboard.html          # Dashboard principal
│   │   │                            # - Cards: Total, Pendientes, Aprobados, Rechazados
│   │   │                            # - Tabla últimos informes
│   │   │                            # - Botón destacado "Enviar Nuevo Informe"
│   │   ├── enviar_informe.html     # Formulario de envío
│   │   │                            # - Upload PDF/DOCX con drag & drop
│   │   │                            # - Validación de tamaño/tipo
│   │   │                            # - Preview del nombre
│   │   ├── historial.html          # Historial completo de informes
│   │   │                            # - Tabla con filtros
│   │   │                            # - Badges de estado
│   │   │                            # - Botón "Reenviar" (solo última versión rechazada)
│   │   │                            # - Link a detalle
│   │   └── detalle_informe.html    # Ver detalle del informe
│   │                                # - Estado actual
│   │                                # - Timeline del flujo
│   │                                # - Dictamen completo (si rechazado)
│   │                                # - Observaciones categorizadas
│   │
│   ├── docente/                     # 👨‍🏫 UI para Docentes
│   │   ├── base_docente.html       # Hereda base_v2
│   │   ├── dashboard.html          # Dashboard con tabs
│   │   │                            # Tab 1: Informes Asignados
│   │   │                            # Tab 2: Informes Revisados
│   │   │                            # Tab 3: Estadísticas
│   │   ├── revisar.html            # Validación con IA
│   │   │                            # - Visor del informe (iframe PDF)
│   │   │                            # - Botón "Validar con IA" → Modal
│   │   │                            # - Barra de progreso animada
│   │   │                            # - Lista de observaciones generadas
│   │   │                            # - Confirmar/Descartar cada obs
│   │   │                            # - Textarea para dictamen
│   │   │                            # - Radio: Recomendar Aprobar/Rechazar
│   │   ├── banco.html              # Gestión de bancos
│   │   │                            # - Lista de bancos (activo/inactivos)
│   │   │                            # - Upload nuevo banco
│   │   │                            # - Activar/Desactivar
│   │   │                            # - Ver contenido
│   │   ├── detalle_banco.html      # Ver contenido del banco
│   │   └── estadisticas.html       # Métricas del docente
│   │                                # - Charts: Informes por mes
│   │                                # - Promedio observaciones
│   │                                # - Tiempo promedio
│   │
│   ├── presidente/                  # 👔 UI para Presidentes
│   │   ├── base_presidente.html    # Hereda base_v2
│   │   ├── dashboard.html          # Dashboard con secciones
│   │   │                            # - Pendientes de asignar docente
│   │   │                            # - Pendientes de revisar dictamen
│   │   │                            # - Estadísticas de la escuela
│   │   ├── asignar.html            # Asignar docente revisor
│   │   │                            # - Datos del informe
│   │   │                            # - Select de docentes disponibles
│   │   │                            # - Info de carga actual de cada docente
│   │   ├── revisar.html            # ⭐ Revisar dictamen (3 decisiones)
│   │   │                            # - Dictamen formateado del docente
│   │   │                            # - Observaciones confirmadas
│   │   │                            # - Textarea para comentario presidente
│   │   │                            # - 3 botones claramente separados:
│   │   │                            #   1. ✅ Aprobar Informe → secretaría
│   │   │                            #   2. ❌ Rechazar Informe → secretaría
│   │   │                            #   3. 🔄 Devolver Dictamen → docente
│   │   └── estadisticas.html       # Métricas de la escuela
│   │
│   ├── secretaria/                  # 📋 UI para Secretarias
│   │   ├── base_secretaria.html    # Hereda base_v2
│   │   ├── dashboard.html          # Dashboard con tabs
│   │   │                            # Tab 1: Nuevos (para derivar)
│   │   │                            # Tab 2: Completados
│   │   │                            #   - Muestra si terminó aprobado/rechazado
│   │   │                            #   - Badge verde/rojo según resultado
│   │   ├── derivar.html            # Derivar a escuela profesional
│   │   │                            # - Select de escuelas
│   │   │                            # - Textarea comentario
│   │   ├── notificar.html          # Notificar aprobación/rechazo final
│   │   │                            # - Ver dictamen completo
│   │   │                            # - Botón "Notificar Aprobación"
│   │   │                            # - Botón "Notificar Rechazo"
│   │   └── historial.html          # Historial completo
│   │
│   ├── admin/                       # 🔧 UI para Administradores
│   │   ├── base_admin.html         # Hereda base_v2
│   │   ├── dashboard.html          # Dashboard global
│   │   │                            # - Cards: Usuarios, Escuelas, Informes
│   │   │                            # - Gráficos con Chart.js
│   │   ├── usuarios.html           # CRUD de usuarios
│   │   ├── escuelas.html           # CRUD de escuelas
│   │   └── reportes.html           # Reportes y analytics
│   │
│   └── components/                  # Componentes reutilizables
│       ├── notificaciones.html     # Widget de notificaciones
│       │                            # - Dropdown con lista
│       │                            # - Badge contador no leídas
│       │                            # - Link "Ver todas"
│       ├── tabla_informes.html     # Tabla genérica
│       ├── modal_confirmacion.html # Modal de confirmación
│       └── timeline.html           # Timeline de estados
│
└── static/
    ├── css/
    │   ├── untels-theme.css        # ⭐ Tema principal UNTELS
    │   │                            # - Variables CSS para colores
    │   │                            # - Estilos globales
    │   ├── custom.css              # Estilos personalizados
    │   ├── responsive.css          # Media queries
    │   └── components/             # Estilos por componente
    │       ├── navbar.css
    │       ├── sidebar.css
    │       ├── cards.css
    │       └── tables.css
    │
    ├── js/
    │   ├── multi-tab-sessions.js   # ⭐ Gestión de sesiones multi-tab
    │   │                            # - localStorage sync
    │   │                            # - Previene conflictos
    │   ├── validacion-ia.js        # ⭐ Barra de progreso IA
    │   │                            # - Mensajes dinámicos
    │   │                            # - Animación smooth
    │   ├── notificaciones.js       # Polling de notificaciones
    │   │                            # - Actualiza cada 30s
    │   │                            # - Badge contador
    │   ├── confirmar-observaciones.js  # UI para confirmar/descartar
    │   ├── upload-file.js          # Drag & drop upload
    │   ├── charts.js               # Configuración Chart.js
    │   └── utils.js                # Funciones auxiliares
    │
    └── images/
        ├── logo-untels.png         # Logo oficial (400x100)
        ├── favicon.ico             # 32x32
        ├── placeholders/           # Imágenes de placeholder
        └── icons/                  # Iconos personalizados
```

---

## 🎨 Paleta de Colores

### Colores Principales (untels-theme.css)

```css
:root {
    /* Colores UNTELS Oficial */
    --untels-blue: #1a3a6b;          /* Azul UNTELS oficial */
    --untels-blue-dark: #0f2342;     /* Azul oscuro */
    --untels-blue-light: #2c5aa0;    /* Azul claro */
    
    /* Colores del Sistema */
    --primary: #0d6efd;              /* Bootstrap primary */
    --secondary: #6c757d;            /* Gris */
    --success: #198754;              /* Verde éxito */
    --warning: #ffc107;              /* Amarillo advertencia */
    --danger: #dc3545;               /* Rojo error */
    --info: #0dcaf0;                 /* Azul info */
    
    /* Estados del Informe */
    --estado-enviado: #6c757d;       /* Gris */
    --estado-pendiente: #ffc107;     /* Amarillo */
    --estado-validando: #0dcaf0;     /* Azul claro */
    --estado-revision: #fd7e14;      /* Naranja */
    --estado-aprobado: #198754;      /* Verde */
    --estado-rechazado: #dc3545;     /* Rojo */
    
    /* Severidades de Observaciones */
    --obs-critica: #dc3545;          /* 🔴 Rojo */
    --obs-importante: #fd7e14;       /* 🟠 Naranja */
    --obs-menor: #ffc107;            /* 🟡 Amarillo */
    --obs-sugerencia: #0dcaf0;       /* 💡 Azul */
    
    /* Fondos y Bordes */
    --bg-light: #f8f9fa;
    --bg-dark: #212529;
    --border-color: #dee2e6;
    
    /* Shadows */
    --shadow-sm: 0 .125rem .25rem rgba(0,0,0,.075);
    --shadow-md: 0 .5rem 1rem rgba(0,0,0,.15);
    --shadow-lg: 0 1rem 3rem rgba(0,0,0,.175);
}
```

### Uso de Colores por Contexto

| Contexto | Color | Uso |
|----------|-------|-----|
| **Navbar** | `--untels-blue` | Fondo del navbar principal |
| **Sidebar** | `--untels-blue-dark` | Fondo del sidebar |
| **Enlaces hover** | `--untels-blue-light` | Estado hover |
| **Botón primario** | `--untels-blue` | Acciones principales |
| **Estado aprobado** | `--success` | Badges, cards de aprobados |
| **Estado rechazado** | `--danger` | Badges, cards de rechazados |
| **Estado pendiente** | `--warning` | Badges de pendientes |
| **Validando IA** | `--info` | Indicador de proceso |

### Badges de Estado

```html
<!-- Ejemplos de badges según estado -->
<span class="badge bg-secondary">Enviado</span>
<span class="badge bg-warning text-dark">Pendiente Secretaria</span>
<span class="badge bg-info text-dark">Validando IA</span>
<span class="badge bg-success">Aprobado Final</span>
<span class="badge bg-danger">Rechazado</span>
```

### Badges de Severidad

```html
<!-- Observaciones con severidad -->
<span class="badge" style="background: var(--obs-critica)">🔴 Crítica</span>
<span class="badge" style="background: var(--obs-importante)">🟠 Importante</span>
<span class="badge" style="background: var(--obs-menor)">🟡 Menor</span>
<span class="badge" style="background: var(--obs-sugerencia)">💡 Sugerencia</span>
```

---

## 🧩 Componentes Principales

### 1. Dashboard por Rol

Cada rol tiene su dashboard personalizado:

#### Estudiante
```html
<!-- Cards de métricas -->
<div class="row">
    <div class="col-md-3">
        <div class="card text-center">
            <div class="card-body">
                <h3 class="text-primary">{{ total_informes }}</h3>
                <p>Total Informes</p>
            </div>
        </div>
    </div>
    <!-- Pendientes, Aprobados, Rechazados -->
</div>

<!-- Tabla últimos informes -->
<div class="card mt-4">
    <div class="card-header">
        <h5>Mis Informes</h5>
    </div>
    <div class="card-body">
        <table class="table table-hover">
            <!-- Filas con badges de estado -->
        </table>
    </div>
</div>
```

#### Docente
```html
<!-- Tabs: Asignados / Revisados / Estadísticas -->
<ul class="nav nav-tabs" role="tablist">
    <li class="nav-item">
        <a class="nav-link active" data-bs-toggle="tab" href="#asignados">
            Asignados <span class="badge bg-warning">{{ count }}</span>
        </a>
    </li>
    <!-- Otros tabs -->
</ul>
```

#### Presidente
```html
<!-- Secciones: Asignar Docente / Revisar Dictamen -->
<div class="row">
    <div class="col-md-6">
        <div class="card border-warning">
            <div class="card-header bg-warning text-dark">
                <i class="bi bi-person-plus"></i> Pendientes de Asignar
            </div>
            <!-- Lista informes -->
        </div>
    </div>
    <div class="col-md-6">
        <div class="card border-info">
            <div class="card-header bg-info text-dark">
                <i class="bi bi-clipboard-check"></i> Dictámenes para Revisar
            </div>
            <!-- Lista dictámenes -->
        </div>
    </div>
</div>
```

#### Secretaria
```html
<!-- Tabs: Nuevos / Completados -->
<div class="tab-content">
    <div id="nuevos" class="tab-pane active">
        <!-- Tabla informes para derivar -->
    </div>
    <div id="completados" class="tab-pane">
        <!-- Tabla con resultado final (aprobado/rechazado) -->
        <table class="table">
            <tr>
                <td>{{ informe.nombre }}</td>
                <td>
                    {% if informe.estado == 'aprobado_final' %}
                        <span class="badge bg-success">✅ Aprobado</span>
                    {% else %}
                        <span class="badge bg-danger">❌ Rechazado</span>
                    {% endif %}
                </td>
            </tr>
        </table>
    </div>
</div>
```

---

### 2. Modales

#### Modal de Selección de Banco
```html
<div class="modal fade" id="modalSeleccionBanco">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5>Seleccionar Banco de Observaciones</h5>
            </div>
            <div class="modal-body">
                <div class="list-group">
                    {% for banco in bancos %}
                    <label class="list-group-item">
                        <input type="radio" name="banco_id" value="{{ banco.id }}"
                               {% if banco.activo %}checked{% endif %}>
                        <strong>{{ banco.nombre }}</strong>
                        {% if banco.activo %}
                            <span class="badge bg-success ms-2">Activo</span>
                        {% endif %}
                        <small class="d-block text-muted">
                            Usado {{ banco.veces_usado }} veces
                        </small>
                    </label>
                    {% endfor %}
                </div>
            </div>
            <div class="modal-footer">
                <button class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                <button class="btn btn-primary" onclick="iniciarValidacionIA()">
                    Validar con IA
                </button>
            </div>
        </div>
    </div>
</div>
```

#### Modal de Progreso de IA
```html
<div class="modal fade" id="modalProgresoIA" data-bs-backdrop="static">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-body text-center py-5">
                <div class="spinner-border text-primary mb-3" style="width: 3rem; height: 3rem;">
                </div>
                <h5 id="mensajeProgreso">Conectando con IA...</h5>
                <div class="progress mt-3" style="height: 25px;">
                    <div id="barraProgreso" class="progress-bar progress-bar-striped progress-bar-animated"
                         style="width: 0%">0%</div>
                </div>
                <p class="text-muted mt-3">No cierre esta ventana</p>
            </div>
        </div>
    </div>
</div>
```

---

### 3. Formularios

#### Formulario de Subir Informe (Estudiante)
```html
<form method="post" enctype="multipart/form-data" id="formEnviarInforme">
    {% csrf_token %}
    
    <!-- Drag & Drop Area -->
    <div class="upload-area border rounded p-5 text-center"
         id="uploadArea"
         ondrop="handleDrop(event)"
         ondragover="handleDragOver(event)">
        <i class="bi bi-cloud-upload display-1 text-muted"></i>
        <p class="mt-3">Arrastra tu informe aquí o haz clic para seleccionar</p>
        <input type="file" name="archivo" id="inputArchivo"
               accept=".pdf,.docx"
               class="d-none"
               onchange="handleFileSelect(event)">
        <button type="button" class="btn btn-outline-primary mt-2"
                onclick="document.getElementById('inputArchivo').click()">
            Seleccionar Archivo
        </button>
    </div>
    
    <!-- Preview del archivo -->
    <div id="previewArchivo" class="mt-3 d-none">
        <div class="alert alert-info">
            <i class="bi bi-file-earmark-pdf"></i>
            <strong id="nombreArchivo"></strong>
            <button type="button" class="btn-close float-end" onclick="limpiarArchivo()"></button>
        </div>
    </div>
    
    <button type="submit" class="btn btn-primary btn-lg w-100 mt-4">
        <i class="bi bi-send"></i> Enviar Informe
    </button>
</form>
```

#### Formulario de Confirmar Observaciones (Docente)
```html
<form method="post" action="{% url 'docente:enviar_dictamen' informe.id %}">
    {% csrf_token %}
    
    <!-- Lista de observaciones -->
    <div id="listaObservaciones">
        {% for obs in observaciones %}
        <div class="card mb-2 border-{{ obs.severidad|severidad_color }}">
            <div class="card-body">
                <div class="d-flex justify-content-between">
                    <div>
                        <span class="badge bg-{{ obs.severidad|severidad_color }}">
                            {{ obs.get_severidad_display }}
                        </span>
                        <strong>{{ obs.seccion }}</strong>
                    </div>
                    <div class="btn-group btn-group-sm">
                        <button type="button" class="btn btn-success"
                                onclick="confirmarObservacion({{ obs.id }})">
                            ✅ Confirmar
                        </button>
                        <button type="button" class="btn btn-danger"
                                onclick="descartarObservacion({{ obs.id }})">
                            ❌ Descartar
                        </button>
                    </div>
                </div>
                <p class="mt-2 mb-0">{{ obs.observacion }}</p>
            </div>
        </div>
        {% endfor %}
    </div>
    
    <!-- Dictamen y recomendación -->
    <div class="mt-4">
        <label class="form-label">Comentario Adicional (Dictamen)</label>
        <textarea name="comentario" class="form-control" rows="5" required></textarea>
    </div>
    
    <div class="mt-3">
        <label class="form-label">Recomendación</label>
        <div>
            <input type="radio" name="recomendar" value="aprobar" id="radioAprobar" required>
            <label for="radioAprobar">✅ Recomendar Aprobar</label>
        </div>
        <div>
            <input type="radio" name="recomendar" value="rechazar" id="radioRechazar">
            <label for="radioRechazar">❌ Recomendar Rechazar</label>
        </div>
    </div>
    
    <button type="submit" class="btn btn-primary btn-lg w-100 mt-4">
        Enviar Dictamen al Presidente
    </button>
</form>
```

#### Formulario de 3 Decisiones (Presidente)
```html
<div class="card">
    <div class="card-header bg-primary text-white">
        <h5>Decisión del Presidente</h5>
    </div>
    <div class="card-body">
        <!-- Mostrar dictamen del docente -->
        <div class="border rounded p-3 bg-light mb-4">
            {{ informe.comentario_docente|formatear_dictamen|safe }}
        </div>
        
        <!-- Comentario del presidente -->
        <div class="mb-4">
            <label class="form-label">Comentario del Presidente</label>
            <textarea id="comentarioPresidente" class="form-control" rows="4"
                      placeholder="Opcional para aprobar, obligatorio para rechazar o devolver"></textarea>
        </div>
        
        <!-- 3 BOTONES SEPARADOS -->
        <div class="d-grid gap-2">
            <button class="btn btn-success btn-lg"
                    onclick="confirmarDecision('aprobar_informe')">
                ✅ Aprobar Informe Final
                <small class="d-block">Enviar a secretaría para notificar aprobación</small>
            </button>
            
            <button class="btn btn-danger btn-lg"
                    onclick="confirmarDecision('rechazar_informe')">
                ❌ Rechazar Informe Final
                <small class="d-block">Enviar a secretaría para notificar rechazo</small>
            </button>
            
            <button class="btn btn-warning btn-lg text-dark"
                    onclick="confirmarDecision('devolver_dictamen')">
                🔄 Devolver Dictamen al Docente
                <small class="d-block">El docente debe rehacer la revisión</small>
            </button>
        </div>
    </div>
</div>
```

---

### 4. Vistas Clave v2.1

#### `presidente/revisar.html` - 3 Decisiones Separadas
- ✅ Botón verde "Aprobar Informe"
- ❌ Botón rojo "Rechazar Informe"  
- 🔄 Botón amarillo "Devolver Dictamen"
- Cada uno con tooltip explicativo
- Modales de confirmación diferenciados

#### `secretaria/dashboard.html` - Resultado Final Visible
```html
<tr>
    <td>{{ informe.usuario.nombre }}</td>
    <td>{{ informe.nombre_archivo }}</td>
    <td>
        {% if informe.estado == 'aprobado_final' %}
            <span class="badge bg-success fs-6">✅ APROBADO</span>
        {% elif informe.estado == 'rechazado_estudiante' %}
            <span class="badge bg-danger fs-6">❌ RECHAZADO</span>
        {% else %}
            <span class="badge bg-secondary">{{ informe.get_estado_display }}</span>
        {% endif %}
    </td>
    <td>{{ informe.fecha_completado|date:"d/m/Y H:i" }}</td>
</tr>
```

#### `estudiante/historial.html` - Botón Reenvío Condicional
```html
{% for informe in informes %}
<tr>
    <td>v{{ informe.version }}</td>
    <td>{{ informe.nombre_archivo }}</td>
    <td>
        <span class="badge bg-{{ informe.estado|estado_color }}">
            {{ informe.get_estado_display }}
        </span>
    </td>
    <td>
        {% if informe.estado == 'rechazado_estudiante' and not informe.versiones_posteriores.exists %}
            <!-- Solo mostrar en la ÚLTIMA versión rechazada -->
            <a href="{% url 'estudiante:reenviar' informe.id %}"
               class="btn btn-warning btn-sm">
                🔄 Reenviar Corregido
            </a>
        {% elif informe.estado == 'rechazado_estudiante' %}
            <span class="text-muted">
                <i class="bi bi-check-circle"></i> Ya reenviado
            </span>
        {% else %}
            <a href="{% url 'estudiante:detalle' informe.id %}"
               class="btn btn-sm btn-outline-primary">
                Ver Detalle
            </a>
        {% endif %}
    </td>
</tr>
{% endfor %}
```

---

## ⚡ JavaScript y Funcionalidades

### 1. Progreso de Validación IA (validacion-ia.js)

```javascript
/**
 * Simula progreso durante validación con IA
 * Muestra mensajes y barra de progreso animada
 */
const MENSAJES_PROGRESO = [
    { segundos: 0, mensaje: 'Iniciando validación...', progreso: 5 },
    { segundos: 2, mensaje: 'Leyendo banco de observaciones...', progreso: 15 },
    { segundos: 5, mensaje: 'Conectando con API de IA...', progreso: 25 },
    { segundos: 8, mensaje: 'Extrayendo texto del informe...', progreso: 35 },
    { segundos: 12, mensaje: 'Analizando contenido con IA...', progreso: 50 },
    { segundos: 18, mensaje: 'Detectando observaciones...', progreso: 70 },
    { segundos: 24, mensaje: 'Categorizando por severidad...', progreso: 85 },
    { segundos: 28, mensaje: 'Generando reporte final...', progreso: 95 },
    { segundos: 30, mensaje: '¡Validación completada!', progreso: 100 }
];

function iniciarValidacionIA() {
    const modal = new bootstrap.Modal(document.getElementById('modalProgresoIA'));
    modal.show();
    
    const bancoId = document.querySelector('input[name="banco_id"]:checked')?.value;
    if (!bancoId) {
        alert('Debe seleccionar un banco');
        return;
    }
    
    // Iniciar simulación de progreso
    let indice = 0;
    const interval = setInterval(() => {
        if (indice < MENSAJES_PROGRESO.length) {
            const item = MENSAJES_PROGRESO[indice];
            actualizarProgreso(item.mensaje, item.progreso);
            indice++;
        } else {
            clearInterval(interval);
        }
    }, 2000);
    
    // Llamada AJAX real al backend
    fetch(`/docente/validar/${informeId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ banco_id: bancoId })
    })
    .then(response => response.json())
    .then(data => {
        clearInterval(interval);
        if (data.success) {
            modal.hide();
            location.reload();  // Recargar para mostrar observaciones
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        clearInterval(interval);
        console.error('Error:', error);
        alert('Error al validar con IA');
    });
}

function actualizarProgreso(mensaje, progreso) {
    document.getElementById('mensajeProgreso').textContent = mensaje;
    const barra = document.getElementById('barraProgreso');
    barra.style.width = progreso + '%';
    barra.textContent = progreso + '%';
}
```

---

### 2. Gestión de Sesiones Multi-Tab (multi-tab-sessions.js)

```javascript
/**
 * Previene conflictos cuando el usuario tiene múltiples tabs abiertos
 * con diferentes sesiones (ej: docente + presidente en tabs distintos)
 */

// Guardar sesión actual en localStorage
function guardarSesionActual() {
    const sesion = {
        usuario_id: sessionStorage.getItem('usuario_id'),
        usuario_tipo: sessionStorage.getItem('usuario_tipo'),
        timestamp: Date.now()
    };
    localStorage.setItem('sesion_activa', JSON.stringify(sesion));
}

// Verificar sesión en otros tabs
window.addEventListener('storage', (e) => {
    if (e.key === 'sesion_activa') {
        const sesionNueva = JSON.parse(e.newValue);
        const sesionActual = {
            usuario_id: sessionStorage.getItem('usuario_id'),
            usuario_tipo: sessionStorage.getItem('usuario_tipo')
        };
        
        // Si es diferente usuario, mostrar advertencia
        if (sesionNueva.usuario_id !== sesionActual.usuario_id) {
            mostrarAdvertenciaMultiSesion();
        }
    }
});

function mostrarAdvertenciaMultiSesion() {
    const toast = `
        <div class="position-fixed top-0 end-0 p-3" style="z-index: 11">
            <div class="toast show" role="alert">
                <div class="toast-header bg-warning text-dark">
                    <strong class="me-auto">⚠️ Múltiples sesiones</strong>
                </div>
                <div class="toast-body">
                    Detectamos que inició sesión con otro usuario en otra pestaña.
                    Recomendamos cerrar las sesiones anteriores.
                </div>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', toast);
}

// Guardar sesión al cargar la página
document.addEventListener('DOMContentLoaded', guardarSesionActual);
```

---

### 3. Notificaciones en Tiempo Real (notificaciones.js)

```javascript
/**
 * Actualiza el contador de notificaciones cada 30 segundos
 * Muestra badge con número de no leídas
 */

let intervalo_notificaciones;

function iniciarPollingNotificaciones() {
    // Primera carga inmediata
    actualizarNotificaciones();
    
    // Luego cada 30 segundos
    intervalo_notificaciones = setInterval(actualizarNotificaciones, 30000);
}

function actualizarNotificaciones() {
    fetch('/api/notificaciones/no_leidas/')
        .then(response => response.json())
        .then(data => {
            const badge = document.getElementById('badgeNotificaciones');
            if (data.count > 0) {
                badge.textContent = data.count;
                badge.classList.remove('d-none');
                badge.classList.add('badge', 'bg-danger', 'rounded-pill');
            } else {
                badge.classList.add('d-none');
            }
            
            // Actualizar lista en dropdown
            actualizarListaNotificaciones(data.notificaciones);
        })
        .catch(error => console.error('Error al cargar notificaciones:', error));
}

function actualizarListaNotificaciones(notificaciones) {
    const lista = document.getElementById('listaNotificaciones');
    if (notificaciones.length === 0) {
        lista.innerHTML = '<li class="dropdown-item text-muted">No hay notificaciones</li>';
        return;
    }
    
    lista.innerHTML = notificaciones.map(n => `
        <li>
            <a class="dropdown-item ${n.leida ? '' : 'fw-bold'}" 
               href="/notificaciones/${n.id}/">
                <small class="text-muted">${n.fecha}</small><br>
                ${n.titulo}<br>
                <small>${n.mensaje}</small>
            </a>
        </li>
    `).join('');
}

function marcarComoLeida(notificacionId) {
    fetch(`/notificaciones/${notificacionId}/marcar_leida/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(() => actualizarNotificaciones());
}

// Iniciar al cargar la página
document.addEventListener('DOMContentLoaded', iniciarPollingNotificaciones);

// Detener al cerrar
window.addEventListener('beforeunload', () => {
    clearInterval(intervalo_notificaciones);
});
```

---

### 4. Confirmar/Descartar Observaciones (confirmar-observaciones.js)

```javascript
/**
 * Permite al docente confirmar o descartar cada observación generada por IA
 */

function confirmarObservacion(observacionId) {
    fetch(`/docente/observacion/${observacionId}/confirmar/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Actualizar UI
            const card = document.querySelector(`[data-obs-id="${observacionId}"]`);
            card.classList.remove('border-warning');
            card.classList.add('border-success');
            
            const badge = card.querySelector('.badge-estado');
            badge.textContent = '✅ Confirmada';
            badge.classList.remove('bg-warning');
            badge.classList.add('bg-success');
            
            // Deshabilitar botones
            const botones = card.querySelectorAll('button');
            botones.forEach(btn => btn.disabled = true);
            
            // Actualizar contador
            actualizarContadorConfirmadas();
        }
    });
}

function descartarObservacion(observacionId) {
    const motivo = prompt('¿Por qué descarta esta observación? (opcional)');
    
    fetch(`/docente/observacion/${observacionId}/descartar/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ comentario: motivo || '' })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Ocultar card con animación
            const card = document.querySelector(`[data-obs-id="${observacionId}"]`);
            card.style.opacity = '0.3';
            card.style.textDecoration = 'line-through';
            
            const badge = card.querySelector('.badge-estado');
            badge.textContent = '❌ Descartada';
            badge.classList.remove('bg-warning');
            badge.classList.add('bg-secondary');
        }
    });
}

function actualizarContadorConfirmadas() {
    const confirmadas = document.querySelectorAll('.border-success').length;
    document.getElementById('contadorConfirmadas').textContent = confirmadas;
}
```

---

### 5. Upload con Drag & Drop (upload-file.js)

```javascript
/**
 * Permite arrastrar y soltar archivos para subir informes
 */

const uploadArea = document.getElementById('uploadArea');
const inputArchivo = document.getElementById('inputArchivo');

function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.classList.add('border-primary', 'bg-light');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.classList.remove('border-primary', 'bg-light');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.classList.remove('border-primary', 'bg-light');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        inputArchivo.files = files;
        handleFileSelect({ target: inputArchivo });
    }
}

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (!file) return;
    
    // Validar tipo
    const tiposPermitidos = ['.pdf', '.docx'];
    const extension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
    if (!tiposPermitidos.includes(extension)) {
        alert('Solo se permiten archivos PDF o DOCX');
        inputArchivo.value = '';
        return;
    }
    
    // Validar tamaño (máx 10 MB)
    const maxSize = 10 * 1024 * 1024;  // 10 MB
    if (file.size > maxSize) {
        alert('El archivo no debe superar 10 MB');
        inputArchivo.value = '';
        return;
    }
    
    // Mostrar preview
    document.getElementById('previewArchivo').classList.remove('d-none');
    document.getElementById('nombreArchivo').textContent = file.name;
}

function limpiarArchivo() {
    inputArchivo.value = '';
    document.getElementById('previewArchivo').classList.add('d-none');
}

// Event listeners
uploadArea.addEventListener('dragover', handleDragOver);
uploadArea.addEventListener('dragleave', handleDragLeave);
uploadArea.addEventListener('drop', handleDrop);
```

---

### 6. Utilidades Comunes (utils.js)

```javascript
/**
 * Funciones auxiliares compartidas
 */

// Obtener cookie CSRF para peticiones POST
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Formatear fecha
function formatearFecha(fecha) {
    const d = new Date(fecha);
    return d.toLocaleDateString('es-PE', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Mostrar toast de notificación
function mostrarToast(mensaje, tipo = 'info') {
    const colores = {
        success: 'bg-success',
        danger: 'bg-danger',
        warning: 'bg-warning',
        info: 'bg-info'
    };
    
    const toast = `
        <div class="position-fixed bottom-0 end-0 p-3" style="z-index: 11">
            <div class="toast show ${colores[tipo]}" role="alert">
                <div class="toast-body text-white">
                    ${mensaje}
                </div>
            </div>
        </div>
    `;
    
    const div = document.createElement('div');
    div.innerHTML = toast;
    document.body.appendChild(div);
    
    setTimeout(() => div.remove(), 3000);
}

// Confirmar acción
function confirmarAccion(mensaje, callback) {
    if (confirm(mensaje)) {
        callback();
    }
}
```

---

## 📄 Templates Django

### Herencia de Templates

```django
{# base_v2.html - Template raíz #}
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Sistema UNTELS{% endblock %}</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
    
    <!-- Custom CSS -->
    <link rel="stylesheet" href="{% static 'css/untels-theme.css' %}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark" style="background-color: var(--untels-blue);">
        {% block navbar %}
        <div class="container-fluid">
            <a class="navbar-brand" href="{% url 'dashboard' %}">
                <img src="{% static 'images/logo-untels.png' %}" height="40" alt="UNTELS">
            </a>
            <div class="navbar-nav ms-auto">
                <!-- Notificaciones -->
                <div class="nav-item dropdown">
                    <a class="nav-link position-relative" href="#" data-bs-toggle="dropdown">
                        <i class="bi bi-bell fs-5"></i>
                        <span id="badgeNotificaciones" class="badge bg-danger rounded-pill d-none">0</span>
                    </a>
                    <ul class="dropdown-menu dropdown-menu-end" id="listaNotificaciones">
                        <!-- Se llena con JS -->
                    </ul>
                </div>
                
                <!-- Usuario -->
                <div class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" data-bs-toggle="dropdown">
                        <i class="bi bi-person-circle"></i> {{ request.session.usuario_nombre }}
                    </a>
                    <ul class="dropdown-menu dropdown-menu-end">
                        <li><a class="dropdown-item" href="{% url 'perfil' %}">Mi Perfil</a></li>
                        <li><hr class="dropdown-divider"></li>
                        <li><a class="dropdown-item" href="{% url 'logout' %}">Cerrar Sesión</a></li>
                    </ul>
                </div>
            </div>
        </div>
        {% endblock %}
    </nav>
    
    <!-- Contenido -->
    <main class="container-fluid py-4">
        {% if messages %}
            {% for message in messages %}
            <div class="alert alert-{{ message.tags }} alert-dismissible fade show">
                {{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
            {% endfor %}
        {% endif %}
        
        {% block content %}{% endblock %}
    </main>
    
    <!-- Footer -->
    <footer class="bg-light text-center py-3 mt-5">
        {% block footer %}
        <p class="text-muted mb-0">
            © 2026 Universidad Nacional Tecnológica de Lima Sur - Sistema de Validación de Informes v2.1
        </p>
        {% endblock %}
    </footer>
    
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- Custom JS -->
    <script src="{% static 'js/utils.js' %}"></script>
    <script src="{% static 'js/notificaciones.js' %}"></script>
    <script src="{% static 'js/multi-tab-sessions.js' %}"></script>
    
    {% block extra_js %}{% endblock %}
</body>
</html>
```

```django
{# docente/base_docente.html - Hereda de base_v2 #}
{% extends 'base_v2.html' %}

{% block title %}Docente - {{ block.super }}{% endblock %}

{% block navbar %}
{{ block.super }}
<!-- Agregar items específicos del navbar docente -->
{% endblock %}

{% block content %}
<div class="row">
    <!-- Sidebar específico de docente -->
    <div class="col-md-2">
        <div class="list-group">
            <a href="{% url 'docente:dashboard' %}" class="list-group-item">
                <i class="bi bi-house"></i> Dashboard
            </a>
            <a href="{% url 'docente:banco' %}" class="list-group-item">
                <i class="bi bi-database"></i> Bancos
            </a>
            <a href="{% url 'docente:estadisticas' %}" class="list-group-item">
                <i class="bi bi-graph-up"></i> Estadísticas
            </a>
        </div>
    </div>
    
    <!-- Contenido específico -->
    <div class="col-md-10">
        {% block docente_content %}{% endblock %}
    </div>
</div>
{% endblock %}
```

```django
{# docente/revisar.html - Vista de revisión #}
{% extends 'docente/base_docente.html' %}
{% load dictamen_filters %}

{% block title %}Revisar Informe{% endblock %}

{% block extra_js %}
<script src="{% static 'js/validacion-ia.js' %}"></script>
<script src="{% static 'js/confirmar-observaciones.js' %}"></script>
<script>
    const informeId = {{ informe.id }};
</script>
{% endblock %}

{% block docente_content %}
<h2>Revisar Informe: {{ informe.nombre_archivo }}</h2>

<!-- Botón Validar con IA -->
<button class="btn btn-primary mb-3" data-bs-toggle="modal" data-bs-target="#modalSeleccionBanco">
    <i class="bi bi-robot"></i> Validar con IA
</button>

<!-- Observaciones generadas -->
{% if observaciones %}
<div class="mt-4">
    <h4>Observaciones Generadas ({{ observaciones|length }})</h4>
    
    {% for obs in observaciones %}
    <div class="card mb-2 border-{{ obs.severidad|severidad_color }}" data-obs-id="{{ obs.id }}">
        <div class="card-body">
            <div class="d-flex justify-content-between align-items-start">
                <div>
                    <span class="badge bg-{{ obs.severidad|severidad_color }} badge-estado">
                        {{ obs.get_severidad_display }}
                    </span>
                    <strong>{{ obs.seccion }}</strong>
                    
                    {% if obs.ubicacion_error %}
                    <small class="text-muted">- {{ obs.ubicacion_error }}</small>
                    {% endif %}
                </div>
                
                {% if obs.estado == 'pendiente' %}
                <div class="btn-group btn-group-sm">
                    <button type="button" class="btn btn-success" 
                            onclick="confirmarObservacion({{ obs.id }})">
                        ✅ Confirmar
                    </button>
                    <button type="button" class="btn btn-danger"
                            onclick="descartarObservacion({{ obs.id }})">
                        ❌ Descartar
                    </button>
                </div>
                {% elif obs.estado == 'confirmada' %}
                <span class="badge bg-success">✅ Confirmada</span>
                {% elif obs.estado == 'descartada' %}
                <span class="badge bg-secondary">❌ Descartada</span>
                {% endif %}
            </div>
            
            <p class="mt-2 mb-0">{{ obs.observacion }}</p>
            
            {% if obs.comentario_docente %}
            <div class="alert alert-info mt-2 mb-0">
                <strong>Tu comentario:</strong> {{ obs.comentario_docente }}
            </div>
            {% endif %}
        </div>
    </div>
    {% endfor %}
    
    <!-- Resumen -->
    <div class="alert alert-info mt-3">
        <strong>Confirmadas:</strong> <span id="contadorConfirmadas">{{ confirmadas_count }}</span> |
        <strong>Descartadas:</strong> {{ descartadas_count }} |
        <strong>Pendientes:</strong> {{ pendientes_count }}
    </div>
</div>
{% endif %}

<!-- Formulario de dictamen -->
<!-- (código del formulario aquí) -->

{% endblock %}
```

### Template Tags Personalizados

```django
{# Cargar template tags #}
{% load dictamen_filters %}

{# Filtro: formatear dictamen #}
{{ informe.comentario_docente|formatear_dictamen|safe }}

{# Filtro: color según severidad #}
<span class="badge bg-{{ observacion.severidad|severidad_color }}">
    {{ observacion.get_severidad_display }}
</span>

{# Filtro: color según estado #}
<span class="badge bg-{{ informe.estado|estado_color }}">
    {{ informe.get_estado_display }}
</span>
```

### Context Processors Personalizados

```python
# backend/apps/core/context_processors.py

def notificaciones_no_leidas(request):
    """Añade contador de notificaciones al contexto global"""
    if 'usuario_id' in request.session:
        from apps.notificaciones.models import Notificacion
        count = Notificacion.objects.filter(
            usuario_id=request.session['usuario_id'],
            leida=False
        ).count()
        return {'notificaciones_no_leidas': count}
    return {'notificaciones_no_leidas': 0}

def datos_sesion(request):
    """Añade datos de sesión al contexto"""
    return {
        'usuario_nombre': request.session.get('usuario_nombre', ''),
        'usuario_tipo': request.session.get('usuario_tipo', ''),
        'usuario_codigo': request.session.get('usuario_codigo', '')
    }
```

---

## ✅ Conclusión del Frontend

El frontend del sistema implementa:

- ✅ **Bootstrap 5.3** para diseño responsive y moderno
- ✅ **JavaScript Vanilla** sin dependencias externas pesadas
- ✅ **Django Templates** con herencia y componentes reutilizables
- ✅ **Paleta de colores UNTELS** corporativa
- ✅ **Interfaces diferenciadas** por rol de usuario
- ✅ **Progreso visual** para operaciones asíncronas (IA)
- ✅ **Notificaciones en tiempo real** con polling
- ✅ **Upload drag & drop** para archivos
- ✅ **Gestión multi-tab** de sesiones
- ✅ **Modales de confirmación** para acciones críticas
- ✅ **Badges y estados** visuales claros
- ✅ **Accesibilidad** y navegación por teclado

---

**Ver también**: [Backend](BACKEND.md) | [Arquitectura](ARQUITECTURA.md) | [PATRONES](PATRONES.md)
