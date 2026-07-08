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
    El docente puede confirmar, descartar o editar
    
    Estados posibles:
    - pendiente: IA generó, docente aún no revisa
    - confirmada: Docente la aceptó (se incluye en dictamen)
    - descartada: Docente la rechazó (no aparece en dictamen)
    - corregida: Estudiante ya corrigió (futuro)
    
    Severidades:
    - critica: Error grave que impide aprobación (🔴)
    - importante: Error significativo (🟠)
    - menor: Detalle a mejorar (🟡)
    - sugerencia: Recomendación opcional (💡)
    """
    ESTADO_PENDIENTE = 'pendiente'
    ESTADO_CONFIRMADA = 'confirmada'
    ESTADO_DESCARTADA = 'descartada'
    ESTADO_CORREGIDA = 'corregida'
    
    ESTADO_CHOICES = [
        (ESTADO_PENDIENTE, 'Pendiente de revisión'),
        (ESTADO_CONFIRMADA, 'Confirmada por docente'),
        (ESTADO_DESCARTADA, 'Descartada por docente'),
        (ESTADO_CORREGIDA, 'Corregida por estudiante'),
    ]
    
    SEVERIDAD_CRITICA = 'critica'
    SEVERIDAD_IMPORTANTE = 'importante'
    SEVERIDAD_MENOR = 'menor'
    SEVERIDAD_SUGERENCIA = 'sugerencia'
    
    SEVERIDAD_CHOICES = [
        (SEVERIDAD_CRITICA, 'Crítica'),
        (SEVERIDAD_IMPORTANTE, 'Importante'),
        (SEVERIDAD_MENOR, 'Menor'),
        (SEVERIDAD_SUGERENCIA, 'Sugerencia'),
    ]
    
    # Relaciones
    informe = models.ForeignKey(
        Informe, 
        on_delete=models.CASCADE,
        related_name='observaciones',
        help_text='Informe al que pertenece esta observación'
    )
    
    # Contenido de la observación
    seccion = models.CharField(
        max_length=100,
        help_text='Sección del informe (Introducción, Marco Teórico, etc.)'
    )
    observacion = models.TextField(
        help_text='Descripción detallada de la observación'
    )
    ubicacion_error = models.CharField(
        max_length=255,
        blank=True,
        help_text='Ubicación específica en el texto (página, párrafo)'
    )
    severidad = models.CharField(
        max_length=20,
        choices=SEVERIDAD_CHOICES,
        default=SEVERIDAD_MENOR,
        help_text='Nivel de severidad de la observación'
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default=ESTADO_PENDIENTE,
        help_text='Estado actual de la observación'
    )
    
    # Revisión del docente
    comentario_docente = models.TextField(
        blank=True,
        help_text='Comentario adicional del docente sobre esta observación'
    )
    fecha_generacion = models.DateTimeField(
        auto_now_add=True,
        help_text='Fecha en que la IA generó la observación'
    )
    fecha_revision = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Fecha en que el docente revisó (confirmó/descartó)'
    )
    
    class Meta:
        db_table = 'observaciones_observaciongenerada'
        ordering = ['-severidad', 'seccion']
        verbose_name = 'Observación Generada'
        verbose_name_plural = 'Observaciones Generadas'
        indexes = [
            models.Index(fields=['informe', 'estado']),
            models.Index(fields=['severidad']),
        ]
    
    def __str__(self):
        return f"{self.get_severidad_display()} - {self.seccion}: {self.observacion[:50]}"
    
    def confirmar(self, comentario=''):
        """Confirma la observación (docente la acepta)"""
        from django.utils import timezone
        self.estado = self.ESTADO_CONFIRMADA
        self.comentario_docente = comentario
        self.fecha_revision = timezone.now()
        self.save()
    
    def descartar(self, comentario=''):
        """Descarta la observación (docente la rechaza)"""
        from django.utils import timezone
        self.estado = self.ESTADO_DESCARTADA
        self.comentario_docente = comentario
        self.fecha_revision = timezone.now()
        self.save()
```

---

### 4. BancoObservacionesDocente

**Ubicación**: `apps/observaciones/models.py`

```python
class BancoObservacionesDocente(models.Model):
    """
    Banco personalizado de observaciones del docente
    
    v2.1 Features:
    - Permite múltiples bancos por docente
    - Solo UNO puede estar activo a la vez (el que se usa por defecto)
    - El docente puede elegir otro banco al validar
    - Soporta PDF, DOCX, TXT
    - Extracción automática de texto
    
    El banco contiene:
    - Criterios de evaluación
    - Errores comunes a buscar
    - Formato esperado
    - Estándares de la escuela
    
    La IA usa este banco como "memoria" contextual para generar
    observaciones coherentes con los criterios del docente.
    """
    
    # Relaciones
    docente = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.CASCADE,
        related_name='bancos_observaciones',
        limit_choices_to={'tipo_usuario': 'docente'},
        help_text='Docente propietario del banco'
    )
    
    # Información del banco
    nombre = models.CharField(
        max_length=200,
        help_text='Nombre descriptivo del banco (ej: "Criterios Informes ISI 2024")'
    )
    descripcion = models.TextField(
        blank=True,
        help_text='Descripción opcional de qué contiene este banco'
    )
    
    # Archivo y contenido
    archivo = models.FileField(
        upload_to='bancos/',
        help_text='Archivo PDF/DOCX/TXT con el banco de observaciones'
    )
    contenido_extraido = models.TextField(
        help_text='Texto extraído del archivo para usar con la IA'
    )
    
    # Estado
    activo = models.BooleanField(
        default=True,
        help_text='Si está activo, se usa por defecto en validaciones'
    )
    
    # Estadísticas de uso
    veces_usado = models.IntegerField(
        default=0,
        help_text='Contador de veces que se ha usado este banco'
    )
    
    # Fechas
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        help_text='Fecha de creación del banco'
    )
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        help_text='Última modificación'
    )
    
    class Meta:
        db_table = 'observaciones_bancoobservacionesdocente'
        ordering = ['-activo', '-fecha_creacion']
        verbose_name = 'Banco de Observaciones'
        verbose_name_plural = 'Bancos de Observaciones'
        indexes = [
            models.Index(fields=['docente', 'activo']),
        ]
        # Constraint: Solo UN banco activo por docente
        # (implementado en lógica de negocio)
    
    def __str__(self):
        estado = "✅ Activo" if self.activo else "⏸️ Inactivo"
        return f"{self.nombre} [{estado}] - {self.docente.nombre}"
    
    def activar(self):
        """
        Activa este banco y desactiva todos los demás del mismo docente
        """
        # Desactivar todos los bancos del docente
        BancoObservacionesDocente.objects.filter(
            docente=self.docente
        ).update(activo=False)
        
        # Activar este
        self.activo = True
        self.save()
    
    def incrementar_uso(self):
        """Incrementa el contador de uso"""
        self.veces_usado += 1
        self.save(update_fields=['veces_usado'])
    
    def save(self, *args, **kwargs):
        """
        Override save para garantizar solo UN banco activo
        """
        if self.activo:
            # Si este se está activando, desactivar los demás
            BancoObservacionesDocente.objects.filter(
                docente=self.docente
            ).exclude(pk=self.pk).update(activo=False)
        
        super().save(*args, **kwargs)
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
    def aprobar_dictamen_docente(informe_id, presidente, comentario, aprobar_informe=True):
        """
        Confirma el dictamen del docente y define la decisión final
        """
        # ... lógica de aprobación/rechazo ...

    @staticmethod
    def rechazar_dictamen_docente(informe_id, presidente, comentario):
        """Devuelve el dictamen al docente para una nueva revisión"""
        # ... lógica de devolución ...
```

**Decisiones del presidente**:
- ✅ Aprobar informe final → `aprobado_presidente`
- ✅ Rechazar informe final → `rechazado_presidente`
- ✅ Devolver dictamen al docente → `revision_docente`

**Versionado del estudiante**:
- El reenvío crea una nueva versión del `Informe`
- Solo la última versión en `rechazado_estudiante` puede reenviarse
- Si una versión ya tiene `versiones_posteriores`, queda cerrada

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
