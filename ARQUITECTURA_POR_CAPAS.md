# ARQUITECTURA DEL SISTEMA - SEPARACIÓN POR CAPAS

Sistema de Validación de Informes de Prácticas Preprofesionales - UNTELS

---

## ÍNDICE DE DOCUMENTOS

Este sistema está documentado en **4 archivos separados por capa**:

1. **CAPA_PRESENTACION.md** - Todo lo relacionado con la interfaz de usuario
2. **CAPA_NEGOCIO.md** - Lógica de aplicación y servicios
3. **CAPA_DATOS.md** - Base de datos y modelos
4. **CAPA_INFRAESTRUCTURA.md** - Docker, deployment, configuración

**Lee cada archivo para entender esa capa específica.**

---

## DIAGRAMA GENERAL DE ARQUITECTURA

```
┌─────────────────────────────────────────────────────────────┐
│                    CAPA PRESENTACIÓN                        │
│                  (Ver CAPA_PRESENTACION.md)                 │
│                                                             │
│  Templates HTML + Bootstrap 5.3                             │
│  • login.html, registro.html, upload_report.html           │
│  • validation_result.html, historial.html                  │
│  • panel_docente.html                                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                     CAPA NEGOCIO                            │
│                   (Ver CAPA_NEGOCIO.md)                     │
│                                                             │
│  Views (apps/core/views.py)                                 │
│  Services (apps/*/services.py)                              │
│  • UserService, DocumentService                             │
│  • RegulationService, ObservationService                    │
│  • AIValidationService (Groq API)                           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                      CAPA DATOS                             │
│                    (Ver CAPA_DATOS.md)                      │
│                                                             │
│  Models (apps/*/models.py)                                  │
│  • Usuario, Informe, Reglamento                             │
│  • BancoObservaciones, ObservacionGenerada                  │
│                                                             │
│  PostgreSQL (producción) / SQLite (desarrollo)              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  CAPA INFRAESTRUCTURA                       │
│                (Ver CAPA_INFRAESTRUCTURA.md)                │
│                                                             │
│  Docker, Settings, Deployment                               │
│  • docker-compose.yml (desarrollo)                          │
│  • docker-compose.prod.yml (producción)                     │
│  • config/settings/ (base, dev, prod)                       │
└─────────────────────────────────────────────────────────────┘
```

---

## FLUJO DE UNA PETICIÓN

**Ejemplo: Usuario sube un informe**

```
1. PRESENTACIÓN
   Usuario hace clic en "Validar Informe" en upload_report.html
   ↓

2. NEGOCIO
   apps/core/views.py → upload_view()
   ├─ apps/informes/services.py → leer_archivo()
   ├─ apps/reglamento/services.py → obtener_reglamento()
   ├─ apps/observaciones/services.py → obtener_observaciones()
   └─ apps/observaciones/services.py → validar_informe() [IA]
   ↓

3. DATOS
   apps/informes/models.py → Informe.objects.create()
   apps/observaciones/models.py → ObservacionGenerada.objects.create()
   ↓

4. PRESENTACIÓN (respuesta)
   Redirect a validation_result.html
   Muestra tabla de observaciones
```

---

## PRINCIPIOS DE SEPARACIÓN

### 1. Capa de Presentación
- **Responsabilidad:** Solo renderizar vistas y capturar entrada del usuario
- **NO debe:** Contener lógica de negocio o acceso directo a base de datos
- **Archivos:** `templates/*.html`

### 2. Capa de Negocio
- **Responsabilidad:** Procesar lógica de aplicación, validaciones, llamadas a servicios
- **NO debe:** Contener SQL directo o código HTML
- **Archivos:** `apps/*/views.py`, `apps/*/services.py`

### 3. Capa de Datos
- **Responsabilidad:** Definir estructura de datos y acceso a base de datos
- **NO debe:** Contener lógica de negocio o validaciones complejas
- **Archivos:** `apps/*/models.py`

### 4. Capa de Infraestructura
- **Responsabilidad:** Configuración, deployment, orquestación
- **NO debe:** Contener lógica de aplicación
- **Archivos:** `config/settings/`, `docker-compose.yml`, `Dockerfile`

---

## COMUNICACIÓN ENTRE CAPAS

```
PERMITIDO:
✓ Presentación → Negocio (via views)
✓ Negocio → Datos (via models)
✓ Negocio → Negocio (servicios llaman a otros servicios)

NO PERMITIDO:
✗ Presentación → Datos directamente
✗ Datos → Negocio
✗ Infraestructura → Negocio
```

---

## MAPEO DE ARCHIVOS POR CAPA

### Presentación
```
proyecto_untels/templates/
├── base.html                    # Template base
├── login.html                   # Login
├── registro.html                # Registro
├── upload_report.html           # Subida de informes
├── validation_result.html       # Resultados
├── historial.html               # Historial
└── panel_docente.html           # Panel administrativo
```

### Negocio
```
proyecto_untels/apps/
├── core/
│   ├── views.py                 # 7 vistas (login, registro, upload, etc.)
│   └── urls.py                  # Rutas
├── usuarios/
│   └── services.py              # UserService (3 funciones)
├── informes/
│   └── services.py              # DocumentService (2 funciones)
├── reglamento/
│   └── services.py              # RegulationService (1 función)
└── observaciones/
    └── services.py              # AIValidationService (2 funciones)
```

### Datos
```
proyecto_untels/apps/
├── usuarios/
│   └── models.py                # Usuario
├── informes/
│   └── models.py                # Informe
├── reglamento/
│   └── models.py                # Reglamento
└── observaciones/
    └── models.py                # BancoObservaciones, ObservacionGenerada
```

### Infraestructura
```
proyecto_untels/
├── config/
│   ├── settings/
│   │   ├── base.py              # Settings base
│   │   ├── development.py       # Settings desarrollo
│   │   └── production.py        # Settings producción
│   ├── urls.py                  # URLs principales
│   └── wsgi.py                  # WSGI config
├── docker-compose.yml           # Docker desarrollo
├── docker-compose.prod.yml      # Docker producción
├── Dockerfile                   # Imagen Docker
└── requirements.txt             # Dependencias Python
```

---

## EJEMPLO PRÁCTICO DE SEPARACIÓN

### ❌ MAL (todo mezclado en una vista):

```python
# apps/core/views.py
def upload_view(request):
    # PRESENTACIÓN + NEGOCIO + DATOS todo mezclado
    archivo = request.FILES.get('informe')
    doc = Document(archivo)
    texto = '\n'.join([p.text for p in doc.paragraphs])
    
    # SQL directo (MAL)
    cursor.execute("INSERT INTO informe VALUES ...")
    
    # Lógica de IA mezclada (MAL)
    response = requests.post("https://api.groq.com/...")
    
    # HTML mezclado (MAL)
    return HttpResponse("<html><body>...</body></html>")
```

### ✅ BIEN (separado en capas):

```python
# CAPA PRESENTACIÓN (templates/upload_report.html)
<form method="POST" enctype="multipart/form-data">
    <input type="file" name="informe">
    <button type="submit">Validar</button>
</form>

# CAPA NEGOCIO (apps/core/views.py)
def upload_view(request):
    archivo = request.FILES.get('informe')
    
    # Delega a servicios
    contenido = leer_archivo(archivo)  # DocumentService
    reglamento = obtener_reglamento()  # RegulationService
    resultado = validar_informe(contenido, reglamento)  # AIService
    
    # Delega a modelos
    informe = Informe.objects.create(...)
    
    return render(request, 'validation_result.html', {...})

# CAPA NEGOCIO - SERVICIOS (apps/informes/services.py)
def leer_archivo(archivo):
    doc = Document(archivo)
    return '\n'.join([p.text for p in doc.paragraphs])

# CAPA DATOS (apps/informes/models.py)
class Informe(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    contenido = models.TextField()
    estado = models.CharField(max_length=20)
```

---

## BENEFICIOS DE ESTA ARQUITECTURA

1. **Mantenibilidad:** Fácil encontrar y modificar código
2. **Testabilidad:** Cada capa se puede testear independientemente
3. **Escalabilidad:** Se puede cambiar una capa sin afectar las demás
4. **Reutilización:** Los servicios se pueden usar desde múltiples vistas
5. **Claridad:** Cada archivo tiene una responsabilidad clara

---

## LECTURA RECOMENDADA

**Para entender el sistema completo, lee en este orden:**

1. **CAPA_PRESENTACION.md** - Entender la interfaz de usuario
2. **CAPA_NEGOCIO.md** - Entender la lógica de aplicación
3. **CAPA_DATOS.md** - Entender los modelos y base de datos
4. **CAPA_INFRAESTRUCTURA.md** - Entender deployment y configuración

Cada documento es independiente y explica esa capa en detalle.

---

**Sistema desarrollado para UNTELS**
