# 🔧 Backend - Sistema de Validación UNTELS

> Documentación técnica completa del backend Django

---

## 📋 Tabla de Contenidos

1. [Tecnologías](#tecnologías)
2. [Estructura del Backend](#estructura-del-backend)
3. [Modelos de Datos](#modelos-de-datos)
4. [Servicios de Negocio](#servicios-de-negocio)
5. [Repositorios](#repositorios)
6. [APIs Externas](#apis-externas)
7. [Autenticación y Autorización](#autenticación-y-autorización)

---

## 🛠️ Tecnologías

### Core
- **Django 4.2.11** - Framework web principal
- **Python 3.9+** - Lenguaje de programación
- **SQLite** - Base de datos (desarrollo)
- **Django ORM** - Mapeo objeto-relacional

### Librerías Clave

```python
# requirements.txt
Django==4.2.11
python-dotenv==1.0.0      # Variables de entorno
python-docx==1.1.0        # Procesamiento DOCX
pypdf==4.0.1              # Procesamiento PDF
requests==2.31.0          # HTTP requests para APIs IA
whitenoise==6.6.0         # Servir archivos estáticos
```

---

## 📁 Estructura del Backend

```
backend/
├── apps/                           # Aplicaciones Django
│   ├── core/                      # Núcleo del sistema
│   │   ├── decorators.py         # @requiere_rol
│   │   ├── admin_views.py        # Panel administrativo
│   │   └── templatetags/         # Filtros personalizados
│   │       └── dictamen_filters.py
│   │
│   ├── usuarios/                  # Gestión de usuarios
│   │   ├── models.py             # Modelo Usuario
│   │   └── migrations/
│   │
│   ├── informes/                  # Gestión de informes
│   │   ├── models.py             # Modelo Informe
│   │   ├── state.py              # State Machine
│   │   └── migrations/
│   │
│   ├── observaciones/             # Observaciones e IA
│   │   ├── models.py             # ObservacionGenerada, BancoObservaciones
│   │   ├── services.py           # Integración con IA
│   │   └── migrations/
│   │
│   ├── escuelas/                  # Escuelas profesionales
│   │   ├── models.py             # Modelo Escuela
│   │   └── services.py
│   │
│   ├── notificaciones/            # Sistema de notificaciones
│   │   ├── models.py             # Modelo Notificacion
│   │   └── services.py           # NotificacionService
│   │
│   ├── negocio/                   # ⭐ CAPA DE NEGOCIO
│   │   └── servicios/
│   │       ├── docente.py        # DocenteService
│   │       ├── presidente.py     # PresidenteService
│   │       ├── secretaria.py     # SecretariaService
│   │       └── estudiante.py     # EstudianteService (futuro)
│   │
│   ├── datos/                     # ⭐ CAPA DE DATOS
│   │   └── repositorios/
│   │       ├── informes.py       # InformeRepository
│   │       ├── usuarios.py       # UsuarioRepository
│   │       └── observaciones.py  # ObservacionRepository
│   │
│   └── presentacion/              # ⭐ CAPA DE PRESENTACIÓN
│       └── web/
│           ├── auth_views.py     # Login, logout, registro
│           ├── estudiante_views.py
│           ├── docente_views.py
│           ├── presidente_views.py
│           └── secretaria_views.py
│
├── config/                         # Configuración Django
│   ├── settings/
│   │   ├── base.py               # Configuración base
│   │   ├── development.py        # Desarrollo
│   │   └── production.py         # Producción
│   ├── urls.py                    # URLs principales
│   └── wsgi.py
│
├── media/                          # Archivos subidos
│   ├── informes/                  # PDFs de informes
│   └── bancos/                    # Bancos de observaciones
│
├── venv/                           # Entorno virtual
├── manage.py                       # CLI de Django
└── .env                            # Variables de entorno
```

---

## 💾 Modelos de Datos

### 1. Usuario

**Ubicación**: `apps/usuarios/models.py`

```python
class Usuario(models.Model):
    """
    Modelo principal de usuarios del sistema
    Gestiona estudiantes, docentes, presidentes y secretarias
    """
    TIPO_ESTUDIANTE = 'estudiante'
    TIPO_DOCENTE = 'docente'
    TIPO_PRESIDENTE = 'presidente'
    TIPO_SECRETARIA = 'secretaria'
    TIPO_ADMIN = 'admin'
    
    TIPO_CHOICES = [
        (TIPO_ESTUDIANTE, 'Estudiante'),
        (TIPO_DOCENTE, 'Docente'),
        (TIPO_PRESIDENTE, 'Presidente de Escuela'),
        (TIPO_SECRETARIA, 'Secretaria Académica'),
        (TIPO_ADMIN, 'Administrador'),
    ]
    
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=200)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_CHOICES)
    password = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    escuela = models.ForeignKey('escuelas.Escuela', ...)
    activo = models.BooleanField(default=True)
```

**Características**:
- ✅ Autenticación personalizada (sin django.contrib.auth)
- ✅ Campo `codigo` como identificador único
- ✅ Múltiples tipos de usuario en un solo modelo
- ✅ Relación con escuela profesional

---

### 2. Informe

**Ubicación**: `apps/informes/models.py`

```python
class Informe(models.Model):
    """
    Informe de práctica preprofesional
    Gestiona el flujo completo de revisión
    """
    # Estados del flujo v2.1
    ESTADO_ENVIADO = 'enviado'
    ESTADO_PENDIENTE_SECRETARIA = 'pendiente_secretaria'
    ESTADO_PENDIENTE_PRESIDENTE = 'pendiente_presidente'
    ESTADO_PENDIENTE_DOCENTE = 'pendiente_docente'
    ESTADO_VALIDANDO_IA = 'validando_ia'
    ESTADO_REVISION_DOCENTE = 'revision_docente'
    ESTADO_PENDIENTE_APROBACION_PRESIDENTE = 'pendiente_aprobacion_presidente'
    ESTADO_APROBADO_PRESIDENTE = 'aprobado_presidente'
    ESTADO_RECHAZADO_PRESIDENTE = 'rechazado_presidente'
    ESTADO_APROBADO_FINAL = 'aprobado_final'
    ESTADO_RECHAZADO_ESTUDIANTE = 'rechazado_estudiante'
    
    # Campos principales
    usuario = models.ForeignKey(Usuario, related_name='informes_enviados')
    nombre_archivo = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='informes/')
    contenido = models.TextField()
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES)
    version = models.IntegerField(default=1)
    
    # Relaciones con roles
    secretaria_asignada = models.ForeignKey(Usuario, related_name='informes_derivados')
    presidente_asignado = models.ForeignKey(Usuario, related_name='informes_presidente')
    docente_revisor = models.ForeignKey(Usuario, related_name='informes_revisor')
    escuela = models.ForeignKey(Escuela)
    
    # Dictámenes y comentarios
    comentario_docente = models.TextField()      # Dictamen estructurado
    comentario_presidente = models.TextField()
    comentario_secretaria = models.TextField()
    
    # Banco usado en validación
    banco_observaciones_usado = models.ForeignKey(BancoObservacionesDocente)
    
    # Versionado
    informe_anterior = models.ForeignKey('self', null=True)
    
    # Fechas de trazabilidad
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_asignacion_secretaria = models.DateTimeField(null=True)
    fecha_asignacion_presidente = models.DateTimeField(null=True)
    fecha_asignacion_docente = models.DateTimeField(null=True)
    fecha_revision_docente = models.DateTimeField(null=True)
    fecha_aprobacion_presidente = models.DateTimeField(null=True)
    fecha_completado = models.DateTimeField(null=True)
    
    def transition_to(self, next_state):
        """Cambiar estado usando State Machine"""
        state = get_state(self.estado)
        state.transition(self, next_state)
```

**Características**:
- ✅ **State Machine**: Gestión de 11 estados
- ✅ **Trazabilidad completa**: Fecha de cada transición
- ✅ **Versionado**: Relación con versiones anteriores
- ✅ **Multi-rol**: Campos para cada participante

---

### 3. ObservacionGenerada

**Ubicación**: `apps/observaciones/models.py`

```python
class ObservacionGenerada(models.Model):
    """
    Observación generada por IA sobre un informe
    El docente puede confirmar o descartar
    """
    ESTADO_PENDIENTE = 'pendiente'
    ESTADO_CONFIRMADA = 'confirmada'
    ESTADO_DESCARTADA = 'descartada'
    ESTADO_CORREGIDA = 'corregida'
    
    SEVERIDAD_CRITICA = 'critica'
    SEVERIDAD_IMPORTANTE = 'importante'
    SEVERIDAD_MENOR = 'menor'
    SEVERIDAD_SUGERENCIA = 'sugerencia'
    
    informe = models.ForeignKey(Informe, related_name='observaciones')
    seccion = models.CharField(max_length=100)
    observacion = models.TextField()
    ubicacion_error = models.CharField(max_length=255)
    severidad = models.CharField(max_length=20, choices=SEVERIDAD_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    
    # Revisión del docente
    comentario_docente = models.TextField(blank=True)
    fecha_revision = models.DateTimeField(null=True)
```

---

### 4. BancoObservacionesDocente

**Ubicación**: `apps/observaciones/models.py`

```python
class BancoObservacionesDocente(models.Model):
    """
    Banco personalizado de observaciones del docente
    v2.1: Permite múltiples bancos activos
    """
    docente = models.ForeignKey(Usuario, related_name='bancos_observaciones')
    nombre = models.CharField(max_length=200)
    archivo = models.FileField(upload_to='bancos/')
    contenido_extraido = models.TextField()
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
```

---

## 💼 Servicios de Negocio

### DocenteService

**Ubicación**: `apps/negocio/servicios/docente.py`

```python
class DocenteService:
    """
    Servicio de negocio para operaciones de Docentes
    TODA la lógica de negocio está aquí
    """
    
    @staticmethod
    def obtener_informes_asignados(docente):
        """Obtiene informes asignados al docente"""
        return Informe.objects.filter(
            docente_revisor=docente,
            estado__in=[
                Informe.ESTADO_PENDIENTE_DOCENTE,
                Informe.ESTADO_VALIDANDO_IA,
                Informe.ESTADO_REVISION_DOCENTE,
                Informe.ESTADO_RECHAZADO_PRESIDENTE
            ]
        ).select_related('usuario', 'escuela')
    
    @staticmethod
    def validar_informe_con_ia(informe_id, docente, banco_especifico=None):
        """
        Valida informe con IA usando banco de observaciones
        
        Returns:
            tuple: (success: bool, observaciones: list, error: str)
        """
        # ... lógica completa de validación ...
    
    @staticmethod
    def enviar_dictamen_a_presidente(informe_id, docente, comentario, recomendar):
        """
        Genera dictamen estructurado y envía al presidente
        
        Proceso:
        1. Actualiza observaciones confirmadas
        2. Genera dictamen estructurado con formato
        3. Cambia estado a PENDIENTE_APROBACION_PRESIDENTE
        4. Notifica al presidente
        """
        # ... lógica completa ...
```

**Métodos Principales**:
- ✅ `obtener_informes_asignados()` - Lista de informes
- ✅ `obtener_informes_revisados()` - Informes enviados al presidente
- ✅ `obtener_banco_activo()` - Banco actual
- ✅ `crear_banco_observaciones()` - Sube nuevo banco
- ✅ `validar_informe_con_ia()` - Validación automática
- ✅ `enviar_dictamen_a_presidente()` - Dictamen final
- ✅ `obtener_estadisticas()` - Métricas del docente

---

### PresidenteService

**Ubicación**: `apps/negocio/servicios/presidente.py`

```python
class PresidenteService:
    """Servicio de negocio para operaciones de Presidentes"""
    
    @staticmethod
    def obtener_informes_pendientes(presidente):
        """Informes pendientes de asignar docente"""
        return Informe.objects.filter(
            presidente_asignado=presidente,
            estado=Informe.ESTADO_PENDIENTE_PRESIDENTE
        )
    
    @staticmethod
    def asignar_docente(informe_id, presidente, docente_id):
        """Asigna docente revisor a un informe"""
        # ... validaciones y asignación ...
    
    @staticmethod
    def revisar_dictamen(informe_id, presidente, accion, comentario):
        """
        Aprueba o rechaza el dictamen del docente
        
        Args:
            accion: 'aprobar' o 'rechazar'
            comentario: Comentario del presidente
        """
        # ... lógica de aprobación/rechazo ...
```

---

### SecretariaService

**Ubicación**: `apps/negocio/servicios/secretaria.py`

```python
class SecretariaService:
    """Servicio de negocio para Secretarias Académicas"""
    
    @staticmethod
    def obtener_informes_pendientes():
        """Informes nuevos pendientes de derivar"""
        return Informe.objects.filter(
            estado__in=[
                Informe.ESTADO_ENVIADO,
                Informe.ESTADO_PENDIENTE_SECRETARIA
            ]
        )
    
    @staticmethod
    def derivar_a_presidente(informe_id, escuela_id, secretaria, comentario):
        """Deriva informe al presidente de la escuela"""
        # ... validaciones y derivación ...
    
    @staticmethod
    def notificar_estudiante_aprobado(informe_id, secretaria):
        """Notifica aprobación final al estudiante"""
        # ... cambio a APROBADO_FINAL ...
    
    @staticmethod
    def notificar_estudiante_rechazado(informe_id, secretaria):
        """Notifica rechazo al estudiante"""
        # ... cambio a RECHAZADO_ESTUDIANTE ...
```

---

## 🗄️ Repositorios

### InformeRepository

**Ubicación**: `apps/datos/repositorios/informes.py`

```python
class InformeRepository:
    """
    Patrón Repository para acceso a Informes
    Abstrae las queries de la base de datos
    """
    
    @staticmethod
    def obtener_por_id(informe_id):
        """Obtiene informe por ID con relaciones"""
        return Informe.objects.select_related(
            'usuario', 'escuela', 'docente_revisor',
            'presidente_asignado', 'secretaria_asignada'
        ).get(id=informe_id)
    
    @staticmethod
    def obtener_con_observaciones(informe_id):
        """Obtiene informe con observaciones precargadas"""
        return Informe.objects.prefetch_related(
            'observaciones'
        ).get(id=informe_id)
```

---

## 🤖 APIs Externas

### Integración con IA

**Ubicación**: `apps/observaciones/services.py`

```python
def validar_con_groq(informe, banco_observaciones):
    """
    Integración con APIs de IA (xAI Grok / Groq)
    
    Detección automática:
    - xai-... → xAI Grok API
    - gsk_... → Groq API (LLaMA)
    - otro → Modo local (fallback)
    """
    
    # Construir prompt
    prompt = f"""
    BANCO DE OBSERVACIONES (Memoria):
    {banco_observaciones.contenido_extraido}
    
    INFORME A VALIDAR:
    {informe.contenido}
    
    TAREA: Detecta errores y genera observaciones en JSON...
    """
    
    # Detectar API por prefijo
    if GROQ_API_KEY.startswith('xai-'):
        url = 'https://api.x.ai/v1/chat/completions'
        modelo = 'grok-beta'
    elif GROQ_API_KEY.startswith('gsk_'):
        url = 'https://api.groq.com/openai/v1/chat/completions'
        modelo = 'llama-3.3-70b-versatile'
    else:
        return validacion_local(informe, banco_observaciones)
    
    # Llamar API
    response = requests.post(url, json={
        'model': modelo,
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': 0.3
    }, headers={'Authorization': f'Bearer {GROQ_API_KEY}'})
    
    # Procesar respuesta
    data = response.json()
    observaciones = json.loads(data['choices'][0]['message']['content'])
    
    return observaciones
```

**APIs Soportadas**:
- ✅ **xAI Grok** (`https://api.x.ai/v1/`)
- ✅ **Groq** (`https://api.groq.com/`) - Recomendado (gratis)
- ✅ **Fallback local** - Si no hay créditos

---

## 🔐 Autenticación y Autorización

### Sistema de Sesiones

**NO usa django.contrib.auth**, sino sesiones personalizadas:

```python
# Login
def login_view(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        password = request.POST.get('password')
        
        usuario = Usuario.objects.filter(
            codigo=codigo,
            password=password,  # ⚠️ Sin hash (desarrollo)
            activo=True
        ).first()
        
        if usuario:
            # Guardar en sesión
            request.session['usuario_id'] = usuario.id
            request.session['usuario_codigo'] = usuario.codigo
            request.session['usuario_nombre'] = usuario.nombre
            request.session['usuario_tipo'] = usuario.tipo_usuario
            
            return redirect_por_rol(usuario.tipo_usuario)
```

### Decorador de Autorización

**Ubicación**: `apps/core/decorators.py`

```python
def requiere_rol(*roles_permitidos):
    """
    Decorador para proteger vistas por rol
    
    Uso:
        @requiere_rol('docente')
        def panel_docente(request):
            ...
        
        @requiere_rol('presidente', 'secretaria')
        def vista_compartida(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Verificar sesión
            if 'usuario_id' not in request.session:
                messages.error(request, 'Debe iniciar sesión')
                return redirect('login')
            
            # Verificar rol
            tipo = request.session.get('usuario_tipo')
            if tipo not in roles_permitidos:
                messages.error(request, 'Acceso denegado')
                return redirect('login')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
```

---

## 🎯 Filtros de Template Personalizados

### Formatear Dictamen

**Ubicación**: `apps/core/templatetags/dictamen_filters.py`

```python
@register.filter(name='formatear_dictamen')
def formatear_dictamen(texto):
    """
    Convierte dictamen en texto plano a HTML formateado
    
    Uso en template:
        {% load dictamen_filters %}
        {{ informe.comentario_docente|formatear_dictamen }}
    
    Detecta:
    - Encabezados (===)
    - Separadores (---)
    - Listas numeradas
    - Emojis (🔴, 🟠, 🟡)
    - Checkmarks (✅, ❌)
    
    Genera:
    - <h5> para títulos
    - <div class="card"> para observaciones
    - <div class="alert"> para recomendaciones
    - <p> para párrafos
    """
    # ... lógica de parseo y HTML ...
    return mark_safe(html)
```

---

## 📊 Configuración

### Variables de Entorno

**Archivo**: `backend/.env`

```bash
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de Datos
DATABASE_PATH=../database/db.sqlite3

# API de IA (elige una)
GROQ_API_KEY=xai-...          # xAI Grok
# GROQ_API_KEY=gsk_...        # Groq (gratis)

# Media
MEDIA_ROOT=media/
MEDIA_URL=/media/
```

---

## ✅ Conclusión

El backend implementa:
- ✅ **Clean Architecture** con 3 capas separadas
- ✅ **Django 4.2** como framework
- ✅ **ORM** para abstracción de BD
- ✅ **Servicios** con lógica de negocio centralizada
- ✅ **State Machine** para flujo de estados
- ✅ **Integración IA** con múltiples APIs
- ✅ **Autenticación personalizada** sin django.contrib.auth
- ✅ **Decoradores** para autorización por rol

---

**Siguiente**: [Frontend](FRONTEND.md) →
