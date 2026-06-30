# PLAN DE IMPLEMENTACIÓN: FLUJO COMPLETO DE VALIDACIÓN DE INFORMES

**Sistema de Validación de Informes de Prácticas Preprofesionales - UNTELS**

**Fecha de creación:** 29 de Junio de 2026  
**Versión:** 2.0  
**Autor:** Sistema de desarrollo - Clean Architecture & 3 Capas

---

## ÍNDICE

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Análisis del Estado Actual](#análisis-del-estado-actual)
3. [Flujo Nuevo Requerido](#flujo-nuevo-requerido)
4. [Arquitectura de Implementación](#arquitectura-de-implementación)
5. [Plan Detallado por Fases](#plan-detallado-por-fases)
6. [Metas y Progreso](#metas-y-progreso)
7. [Checklist de Verificación](#checklist-de-verificación)
8. [Glosario de Términos](#glosario-de-términos)

---

## RESUMEN EJECUTIVO

### ¿Qué vamos a hacer?

Vamos a **transformar el flujo actual de validación de informes** para implementar un sistema completo de gestión académica que involucra a **4 roles diferentes** con responsabilidades específicas.

### Estado Actual vs Estado Deseado

| Aspecto | Estado Actual | Estado Deseado |
|---------|---------------|----------------|
| **Flujo** | Estudiante → IA → Docente | Estudiante → Secretaria → Presidente → Docente → Presidente → Secretaria → Estudiante |
| **Roles** | 3 roles (Estudiante, Egresado, Docente) | 5 roles (+ Secretaria, Presidente) |
| **Gestión** | Docente gestiona todo | Cada rol tiene responsabilidades específicas |
| **IA** | Banco global de observaciones | Cada docente tiene su propio banco personalizado |
| **Notificaciones** | No hay sistema formal | Sistema completo de notificaciones por rol |
| **Admin** | Admin personalizado básico | Admin avanzado con flujos por rol |

### Impacto del Cambio

**Complejidad:** Alta  
**Esfuerzo estimado:** 20-25 horas  
**Archivos a modificar:** ~30 archivos  
**Archivos nuevos:** ~25 archivos  
**Migraciones de BD:** 3-4 migraciones  

### Principios Arquitectónicos

Este proyecto usa **Clean Architecture** y **Arquitectura de 3 Capas**:

```
┌─────────────────────────────────────┐
│     CAPA DE PRESENTACIÓN            │
│  (Templates, Forms, UI)             │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     CAPA DE NEGOCIO                 │
│  (Views, Services, Logic)           │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     CAPA DE DATOS                   │
│  (Models, Repositories)             │
└─────────────────────────────────────┘
```

**NO mezclaremos lógica entre capas.**  
**Cada cambio respetará la separación de responsabilidades.**

---

## ANÁLISIS DEL ESTADO ACTUAL

### Modelos Existentes

#### 1. Usuario (`apps/usuarios/models.py`)
```python
class Usuario(models.Model):
    codigo = CharField(max_length=20, unique=True)
    nombre = CharField(max_length=200)
    tipo_usuario = CharField(max_length=20, choices=TIPO_CHOICES)
    password = CharField(max_length=255)
    
    TIPO_CHOICES = [
        ('estudiante', 'Estudiante'),
        ('egresado', 'Egresado'),
        ('docente', 'Docente'),
    ]
```

**Problemas:**
- Falta rol `presidente`
- Falta rol `secretaria`
- No hay relación con escuelas/carreras

#### 2. Informe (`apps/informes/models.py`)
```python
class Informe(models.Model):
    usuario = ForeignKey(Usuario)
    nombre_archivo = CharField(max_length=255)
    contenido = TextField()
    estado = CharField(max_length=30, choices=ESTADO_CHOICES)
    docente_revisor = ForeignKey(Usuario, null=True)
    comentario_docente = TextField(null=True)
    
    ESTADOS = [
        'enviado', 'validando', 'observado',
        'revision_docente', 'rechazado', 'aprobado', 'completado'
    ]
```

**Problemas:**
- Estados no reflejan el flujo completo
- Falta campo `secretaria_asignada`
- Falta campo `presidente_asignado`
- Falta campo `escuela`

#### 3. BancoObservaciones (`apps/observaciones/models.py`)
```python
class BancoObservaciones(models.Model):
    seccion = CharField(max_length=100)
    descripcion = TextField()
```

**Problemas:**
- Es un banco GLOBAL (todos los docentes usan el mismo)
- No hay banco personalizado por docente
- No permite que cada docente suba su propio PDF/DOCX

#### 4. ObservacionGenerada (`apps/observaciones/models.py`)
```python
class ObservacionGenerada(models.Model):
    informe = ForeignKey(Informe)
    seccion = CharField(max_length=100)
    observacion = TextField()
    ubicacion_error = CharField(max_length=255)
    estado = CharField(max_length=20)
    comentario_docente = TextField(null=True)
    severidad = CharField(max_length=20)
```

**Estado:** OK (no requiere cambios mayores)

#### 5. Reglamento (`apps/reglamento/models.py`)
```python
class Reglamento(models.Model):
    nombre = CharField(max_length=255)
    contenido = TextField()
    activo = BooleanField(default=True)
```

**Estado:** OK (no requiere cambios)

### Admin Actual

El proyecto ya tiene un **admin personalizado** (NO usa `django.contrib.admin` para funcionalidad):

- `/admin/dashboard/` - Dashboard general
- `/admin/usuarios/` - Gestión de usuarios
- `/admin/reglamento/` - Gestión de reglamento
- `/admin/observaciones/` - Gestión de banco de observaciones
- `/admin/reportes/` - Reportes estadísticos

**Estado:** BIEN - Ya no usa el admin de Django para funcionalidad principal

### Vistas Actuales

**Estudiante:**
- `login_view()` - Login
- `registro_view()` - Registro
- `upload_view()` - Subir informe
- `resultado_view()` - Ver resultado de validación
- `historial_view()` - Ver historial de informes

**Docente:**
- `login_docente_view()` - Login docente
- `panel_docente_view()` - Panel principal
- `admin_revisar_informe()` - Revisar informe con observaciones

**Admin:**
- `admin_dashboard()` - Dashboard estadísticas
- `admin_usuarios()` - Gestión usuarios
- `admin_reglamento()` - Gestión reglamento
- `admin_observaciones()` - Gestión observaciones
- `admin_reportes()` - Reportes

**Problemas:**
- No hay vistas para Secretaria
- No hay vistas para Presidente
- Docente no puede gestionar su propio banco de observaciones
- No hay sistema de notificaciones

---

## FLUJO NUEVO REQUERIDO

### Diagrama del Flujo Completo

```
┌──────────────┐
│  ESTUDIANTE  │
│              │
│ 1. Envía     │
│    informe   │
│    (PDF/DOCX)│
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│   SECRETARIA     │
│                  │
│ 2. Recibe        │
│ 3. Verifica      │
│ 4. Deriva a      │
│    Presidente    │
│    de Escuela    │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│   PRESIDENTE     │
│   DE ESCUELA     │
│                  │
│ 5. Revisa        │
│ 6. Designa       │
│    Docente       │
└──────┬───────────┘
       │
       ▼
┌──────────────────────────┐
│       DOCENTE            │
│                          │
│ 7. Sube su Banco de      │
│    Observaciones         │
│    (PDF/DOCX propio)     │
│                          │
│ 8. Usa IA con su         │
│    banco personalizado   │
│                          │
│ 9. Revisa tabla          │
│    editable de           │
│    observaciones         │
│                          │
│ 10. Genera informe       │
│     con dictamen         │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────┐
│   PRESIDENTE     │
│                  │
│ 11. Revisa       │
│     dictamen     │
│                  │
│ 12. APRUEBA o    │
│     RECHAZA      │
└──────┬───────────┘
       │
       ├─────── RECHAZA ────────┐
       │                        │
       │                        ▼
       │              ┌─────────────────┐
       │              │    DOCENTE      │
       │              │                 │
       │              │ Vuelve al       │
       │              │ paso 7          │
       │              └─────────────────┘
       │
       ▼ APRUEBA
┌──────────────────┐
│   SECRETARIA     │
│                  │
│ 13. Recibe       │
│     aprobación   │
│                  │
│ 14. Notifica     │
│     a estudiante │
└──────┬───────────┘
       │
       ▼
┌──────────────┐
│  ESTUDIANTE  │
│              │
│ 15. Recibe   │
│     resultado│
│              │
│ SI RECHAZADO │
│ → Vuelve al  │
│   paso 1     │
└──────────────┘
```

### Estados del Informe

```python
# ESTADOS COMPLETOS DEL NUEVO FLUJO
ESTADO_ENVIADO = 'enviado'                          # 1. Estudiante envió
ESTADO_PENDIENTE_SECRETARIA = 'pendiente_secretaria'  # 2. En bandeja de secretaria
ESTADO_PENDIENTE_PRESIDENTE = 'pendiente_presidente'  # 3. En bandeja de presidente
ESTADO_PENDIENTE_DOCENTE = 'pendiente_docente'        # 4. Asignado a docente
ESTADO_VALIDANDO_IA = 'validando_ia'                  # 5. IA procesando con banco docente
ESTADO_REVISION_DOCENTE = 'revision_docente'          # 6. Docente revisando observaciones
ESTADO_PENDIENTE_APROBACION_PRESIDENTE = 'pendiente_aprobacion_presidente'  # 7. Esperando aprobación
ESTADO_APROBADO_PRESIDENTE = 'aprobado_presidente'    # 8. Presidente aprobó
ESTADO_RECHAZADO_PRESIDENTE = 'rechazado_presidente'  # 9. Presidente rechazó (vuelve a docente)
ESTADO_APROBADO_FINAL = 'aprobado_final'              # 10. Estudiante aprobado
ESTADO_RECHAZADO_ESTUDIANTE = 'rechazado_estudiante'  # 11. Estudiante debe corregir
```

### Roles y Responsabilidades

#### 1. Estudiante
- **Login:** Login separado (ya existe)
- **Acciones:**
  - Enviar informe (PDF/DOCX)
  - Ver estado actual del informe
  - Ver historial de informes
  - Recibir notificaciones de aprobación/rechazo
- **No puede:** Ver otros informes, gestionar observaciones

#### 2. Secretaria
- **Login:** Login separado (nuevo)
- **Acciones:**
  - Ver bandeja de informes recibidos
  - Verificar que el archivo sea válido
  - Asignar a escuela de carrera
  - Derivar a presidente de escuela
  - Recibir informe aprobado del presidente
  - Notificar resultado final al estudiante
- **Dashboard:**
  - Informes pendientes de derivar
  - Informes enviados a presidentes
  - Informes completados
  - Historial completo

#### 3. Presidente de Escuela
- **Login:** Login separado (nuevo)
- **Acciones:**
  - Ver informes de SU escuela solamente
  - Designar docente revisor (de su escuela)
  - Recibir dictamen del docente
  - Aprobar o rechazar dictamen
  - Si rechaza → vuelve al docente con comentarios
  - Si aprueba → envía a secretaria
- **Dashboard:**
  - Informes pendientes de asignar
  - Informes en revisión (por docentes)
  - Informes pendientes de su aprobación
  - Historial de su escuela

#### 4. Docente
- **Login:** Login separado (ya existe)
- **Acciones:**
  - Gestionar su propio banco de observaciones
  - Subir archivo PDF/DOCX con su banco personalizado
  - Ver informes asignados a él
  - Usar IA con SU banco de observaciones
  - Editar tabla de observaciones generadas
  - Agregar/eliminar/modificar observaciones
  - Cambiar severidad de observaciones
  - Generar informe con dictamen
  - Enviar a presidente con recomendación (aprobar/rechazar)
- **Dashboard:**
  - Informes pendientes de revisar
  - Mi banco de observaciones
  - Informes revisados
  - Historial

---

## ARQUITECTURA DE IMPLEMENTACIÓN

### Separación por Capas

Siguiendo **Clean Architecture** y **Arquitectura de 3 Capas**:

```
proyecto_untels/
│
├── apps/
│   │
│   ├── usuarios/                          # CAPA DATOS - Usuarios
│   │   ├── models.py                      # ✏️ MODIFICAR
│   │   │   └── Usuario (+ presidente, secretaria, escuela)
│   │   ├── services.py                    # ✏️ MODIFICAR
│   │   │   └── UserService (+ roles nuevos)
│   │   └── admin.py                       # OK
│   │
│   ├── escuelas/                          # 🆕 NUEVA APP
│   │   ├── models.py                      # 🆕 CREAR
│   │   │   └── Escuela
│   │   └── services.py                    # 🆕 CREAR
│   │       └── EscuelaService
│   │
│   ├── informes/                          # CAPA DATOS - Informes
│   │   ├── models.py                      # ✏️ MODIFICAR
│   │   │   └── Informe (+ secretaria, presidente, nuevos estados)
│   │   ├── state.py                       # ✏️ MODIFICAR
│   │   │   └── Máquina de estados completa
│   │   └── services.py                    # ✏️ MODIFICAR
│   │       └── InformeService
│   │
│   ├── observaciones/                     # CAPA DATOS - Observaciones
│   │   ├── models.py                      # ✏️ MODIFICAR
│   │   │   ├── BancoObservaciones (global - mantener)
│   │   │   └── BancoObservacionesDocente  # 🆕 CREAR
│   │   └── services.py                    # ✏️ MODIFICAR
│   │       └── ObservacionService (+ banco por docente)
│   │
│   ├── notificaciones/                    # 🆕 NUEVA APP
│   │   ├── models.py                      # 🆕 CREAR
│   │   │   └── Notificacion
│   │   └── services.py                    # 🆕 CREAR
│   │       └── NotificacionService
│   │
│   ├── negocio/                           # CAPA NEGOCIO
│   │   └── servicios/
│   │       ├── usuarios.py                # ✏️ MODIFICAR
│   │       ├── informes.py                # ✏️ MODIFICAR
│   │       ├── observaciones.py           # ✏️ MODIFICAR
│   │       ├── reglamento.py              # OK
│   │       ├── secretaria.py              # 🆕 CREAR
│   │       ├── presidente.py              # 🆕 CREAR
│   │       ├── docente.py                 # 🆕 CREAR
│   │       └── notificaciones.py          # 🆕 CREAR
│   │
│   ├── presentacion/                      # CAPA PRESENTACIÓN
│   │   └── web/
│   │       ├── auth_views.py              # ✏️ MODIFICAR (+ login secretaria, presidente)
│   │       ├── estudiante_views.py        # ✏️ MODIFICAR
│   │       ├── secretaria_views.py        # 🆕 CREAR
│   │       ├── presidente_views.py        # 🆕 CREAR
│   │       ├── docente_views.py           # ✏️ MODIFICAR
│   │       └── admin_views.py             # ✏️ MODIFICAR
│   │
│   └── core/                              # CAPA PRESENTACIÓN (coordinación)
│       ├── views.py                       # ✏️ MODIFICAR (facades)
│       ├── urls.py                        # ✏️ MODIFICAR (+ rutas nuevas)
│       └── admin_views.py                 # ✏️ MODIFICAR
│
└── frontend/                              # CAPA PRESENTACIÓN - UI
    └── templates/
        ├── secretaria/                    # 🆕 CREAR
        │   ├── dashboard.html
        │   ├── derivar.html
        │   └── notificar.html
        │
        ├── presidente/                    # 🆕 CREAR
        │   ├── dashboard.html
        │   ├── designar_docente.html
        │   ├── revisar_dictamen.html
        │   └── aprobar_rechazar.html
        │
        ├── docente/                       # 🆕 CREAR
        │   ├── dashboard.html
        │   ├── banco_observaciones.html
        │   ├── subir_banco.html
        │   ├── revisar_ia.html
        │   ├── tabla_editable.html
        │   └── generar_dictamen.html
        │
        ├── estudiante/                    # ✏️ MODIFICAR
        │   ├── historial.html             # ✏️ MEJORAR
        │   └── notificaciones.html        # 🆕 CREAR
        │
        └── admin/                         # ✏️ MODIFICAR
            └── ...                        # Ya existen, mejorar
```

### Resumen de Cambios por Capa

| Capa | Archivos Nuevos | Archivos Modificados | Total |
|------|-----------------|---------------------|-------|
| **DATOS** | 3 modelos nuevos | 3 modelos modificados | 6 |
| **NEGOCIO** | 4 servicios nuevos | 3 servicios modificados | 7 |
| **PRESENTACIÓN** | 15 templates + 2 vistas | 5 vistas modificadas | 22 |
| **INFRAESTRUCTURA** | 0 | 1 (urls.py) | 1 |
| **TOTAL** | ~25 archivos | ~12 archivos | **~37 archivos** |

---

## PLAN DETALLADO POR FASES

### FASE 1: CAPA DE DATOS (Modelos y Migraciones)

**Objetivo:** Crear y modificar modelos para soportar el nuevo flujo

**Duración estimada:** 3-4 horas

#### 1.1 Crear modelo Escuela

**Archivo:** `apps/escuelas/models.py` (nueva app)

```python
from django.db import models
from apps.usuarios.models import Usuario

class Escuela(models.Model):
    """
    Representa una escuela profesional (carrera) de la universidad
    Cada escuela tiene un presidente asignado
    """
    nombre = models.CharField(
        max_length=200,
        help_text="Ej: Ingeniería de Sistemas, Ingeniería Ambiental"
    )
    codigo = models.CharField(
        max_length=20, 
        unique=True,
        help_text="Código único de la escuela (Ej: IS, IA, IM)"
    )
    presidente = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='escuela_presidida',
        limit_choices_to={'tipo_usuario': 'presidente'},
        help_text="Presidente de esta escuela"
    )
    activo = models.BooleanField(
        default=True,
        help_text="Si la escuela está activa"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'escuela'
        verbose_name = 'Escuela Profesional'
        verbose_name_plural = 'Escuelas Profesionales'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
```

**Crear app:**
```bash
python manage.py startapp escuelas
```

**Registrar en settings:**
```python
INSTALLED_APPS = [
    # ...
    'apps.escuelas',
]
```

#### 1.2 Modificar modelo Usuario

**Archivo:** `apps/usuarios/models.py` (modificar)

```python
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Usuario(models.Model):
    """
    Usuario del sistema con múltiples roles
    """
    TIPO_CHOICES = [
        ('estudiante', 'Estudiante'),
        ('egresado', 'Egresado'),
        ('docente', 'Docente'),
        ('presidente', 'Presidente de Escuela'),     # 🆕 NUEVO
        ('secretaria', 'Secretaria Académica'),      # 🆕 NUEVO
    ]
    
    codigo = models.CharField(
        max_length=20, 
        unique=True,
        help_text="Código único del usuario"
    )
    nombre = models.CharField(max_length=200)
    tipo_usuario = models.CharField(
        max_length=20, 
        choices=TIPO_CHOICES, 
        default='estudiante'
    )
    password = models.CharField(max_length=255, blank=True, null=True)
    
    # 🆕 NUEVO: Relación con escuela
    escuela = models.ForeignKey(
        'escuelas.Escuela',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios',
        help_text="Escuela a la que pertenece (estudiantes, docentes, presidente)"
    )
    
    # 🆕 NUEVO: Email para notificaciones
    email = models.EmailField(
        blank=True,
        null=True,
        help_text="Email para notificaciones"
    )
    
    # 🆕 NUEVO: Estado activo
    activo = models.BooleanField(
        default=True,
        help_text="Si el usuario está activo en el sistema"
    )
    
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['tipo_usuario', 'nombre']

    def __str__(self):
        return f"{self.codigo} - {self.nombre} ({self.get_tipo_usuario_display()})"
    
    def set_password(self, raw_password):
        """Encriptar contraseña"""
        self.password = make_password(raw_password)
        self.save()
    
    def check_password(self, raw_password):
        """Verificar contraseña"""
        if not self.password:
            return False
        return check_password(raw_password, self.password)
    
    # 🆕 NUEVO: Métodos de utilidad
    def is_secretaria(self):
        return self.tipo_usuario == 'secretaria'
    
    def is_presidente(self):
        return self.tipo_usuario == 'presidente'
    
    def is_docente(self):
        return self.tipo_usuario == 'docente'
    
    def is_estudiante(self):
        return self.tipo_usuario in ['estudiante', 'egresado']
```

#### 1.3 Crear modelo BancoObservacionesDocente

**Archivo:** `apps/observaciones/models.py` (modificar - agregar modelo)

```python
# Agregar al archivo existente

class BancoObservacionesDocente(models.Model):
    """
    Banco de observaciones personalizado de cada docente
    Cada docente puede subir su propio PDF/DOCX con observaciones
    """
    docente = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.CASCADE,
        related_name='bancos_observaciones',
        limit_choices_to={'tipo_usuario': 'docente'},
        help_text="Docente propietario de este banco"
    )
    nombre = models.CharField(
        max_length=255,
        help_text="Nombre descriptivo del banco (Ej: Observaciones 2026-1)"
    )
    archivo = models.FileField(
        upload_to='bancos_observaciones/%Y/%m/',
        help_text="Archivo PDF o DOCX con observaciones"
    )
    contenido_extraido = models.TextField(
        blank=True,
        help_text="Texto extraído del archivo para usar con IA"
    )
    activo = models.BooleanField(
        default=True,
        help_text="Si este banco está activo (solo uno activo por docente)"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'banco_observaciones_docente'
        verbose_name = 'Banco de Observaciones del Docente'
        verbose_name_plural = 'Bancos de Observaciones de Docentes'
        ordering = ['-activo', '-fecha_creacion']
        unique_together = [['docente', 'nombre']]

    def __str__(self):
        return f"{self.docente.nombre} - {self.nombre} {'(Activo)' if self.activo else ''}"
    
    def save(self, *args, **kwargs):
        """Al activar este banco, desactivar los demás del mismo docente"""
        if self.activo:
            BancoObservacionesDocente.objects.filter(
                docente=self.docente,
                activo=True
            ).exclude(id=self.id).update(activo=False)
        super().save(*args, **kwargs)
```

#### 1.4 Modificar modelo Informe

**Archivo:** `apps/informes/models.py` (modificar)

```python
from django.db import models
from apps.usuarios.models import Usuario
from apps.informes.state import get_state

class Informe(models.Model):
    """
    Informe de práctica preprofesional enviado por estudiante
    Pasa por múltiples estados y roles
    """
    # 🆕 ESTADOS COMPLETOS DEL NUEVO FLUJO
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

    ESTADO_CHOICES = [
        (ESTADO_ENVIADO, 'Enviado por Estudiante'),
        (ESTADO_PENDIENTE_SECRETARIA, 'Pendiente - Secretaría'),
        (ESTADO_PENDIENTE_PRESIDENTE, 'Pendiente - Presidente'),
        (ESTADO_PENDIENTE_DOCENTE, 'Pendiente - Docente Asignado'),
        (ESTADO_VALIDANDO_IA, 'Validando con IA'),
        (ESTADO_REVISION_DOCENTE, 'En Revisión del Docente'),
        (ESTADO_PENDIENTE_APROBACION_PRESIDENTE, 'Pendiente Aprobación Presidente'),
        (ESTADO_APROBADO_PRESIDENTE, 'Aprobado por Presidente'),
        (ESTADO_RECHAZADO_PRESIDENTE, 'Rechazado por Presidente'),
        (ESTADO_APROBADO_FINAL, 'APROBADO FINAL'),
        (ESTADO_RECHAZADO_ESTUDIANTE, 'Rechazado - Estudiante debe Corregir'),
    ]

    # Campos básicos
    usuario = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE,
        related_name='informes_enviados',
        help_text="Estudiante que envió el informe"
    )
    nombre_archivo = models.CharField(max_length=255)
    archivo = models.FileField(
        upload_to='informes/%Y/%m/',
        help_text="Archivo PDF o DOCX del informe"
    )
    contenido = models.TextField(help_text="Texto extraído del archivo")
    estado = models.CharField(
        max_length=50,
        choices=ESTADO_CHOICES,
        default=ESTADO_ENVIADO,
    )
    
    # 🆕 NUEVO: Asignaciones de roles
    secretaria_asignada = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='informes_secretaria',
        limit_choices_to={'tipo_usuario': 'secretaria'},
        help_text="Secretaria que procesó el informe"
    )
    presidente_asignado = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='informes_presidente',
        limit_choices_to={'tipo_usuario': 'presidente'},
        help_text="Presidente de escuela asignado"
    )
    docente_revisor = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='informes_docente',
        limit_choices_to={'tipo_usuario': 'docente'},
        help_text="Docente revisor asignado"
    )
    
    # 🆕 NUEVO: Escuela
    escuela = models.ForeignKey(
        'escuelas.Escuela',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='informes',
        help_text="Escuela profesional del estudiante"
    )
    
    # 🆕 NUEVO: Banco usado
    banco_observaciones_usado = models.ForeignKey(
        'observaciones.BancoObservacionesDocente',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='informes_validados',
        help_text="Banco de observaciones que usó el docente"
    )
    
    # Comentarios por rol
    comentario_secretaria = models.TextField(blank=True, null=True)
    comentario_presidente = models.TextField(blank=True, null=True)
    comentario_docente = models.TextField(blank=True, null=True)
    
    # Fechas de procesamiento
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_asignacion_secretaria = models.DateTimeField(null=True, blank=True)
    fecha_asignacion_presidente = models.DateTimeField(null=True, blank=True)
    fecha_asignacion_docente = models.DateTimeField(null=True, blank=True)
    fecha_revision_docente = models.DateTimeField(null=True, blank=True)
    fecha_aprobacion_presidente = models.DateTimeField(null=True, blank=True)
    fecha_completado = models.DateTimeField(null=True, blank=True)
    
    # Versionado
    version = models.IntegerField(default=1)
    informe_anterior = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='versiones_posteriores'
    )

    class Meta:
        db_table = 'informe'
        verbose_name = 'Informe de Práctica'
        verbose_name_plural = 'Informes de Práctica'
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.nombre_archivo} - {self.usuario.nombre} [{self.get_estado_display()}]"

    def transition_to(self, next_state):
        """Cambiar de estado usando máquina de estados"""
        state = get_state(self.estado)
        state.transition(self, next_state)
        return self
```

#### 1.5 Crear modelo Notificacion

**Archivo:** `apps/notificaciones/models.py` (nueva app)

```python
from django.db import models
from apps.usuarios.models import Usuario
from apps.informes.models import Informe

class Notificacion(models.Model):
    """
    Sistema de notificaciones para todos los roles
    """
    TIPO_CHOICES = [
        ('nuevo_informe', 'Nuevo Informe Recibido'),
        ('asignado_presidente', 'Informe Asignado a Presidente'),
        ('asignado_docente', 'Informe Asignado a Docente'),
        ('revision_completa', 'Revisión Completada'),
        ('aprobado_presidente', 'Aprobado por Presidente'),
        ('rechazado_presidente', 'Rechazado por Presidente'),
        ('aprobado_final', 'Informe Aprobado - Proceso Completo'),
        ('rechazado_estudiante', 'Informe Rechazado - Requiere Correcciones'),
    ]
    
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='notificaciones',
        help_text="Usuario que recibe la notificación"
    )
    informe = models.ForeignKey(
        Informe,
        on_delete=models.CASCADE,
        related_name='notificaciones',
        help_text="Informe relacionado"
    )
    tipo = models.CharField(
        max_length=50,
        choices=TIPO_CHOICES,
        help_text="Tipo de notificación"
    )
    titulo = models.CharField(
        max_length=255,
        help_text="Título de la notificación"
    )
    mensaje = models.TextField(
        help_text="Mensaje completo de la notificación"
    )
    leida = models.BooleanField(
        default=False,
        help_text="Si el usuario ya leyó la notificación"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_leida = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'notificacion'
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.usuario.nombre} - {self.titulo} {'(Leída)' if self.leida else '(No leída)'}"
    
    def marcar_como_leida(self):
        """Marcar notificación como leída"""
        from django.utils import timezone
        self.leida = True
        self.fecha_leida = timezone.now()
        self.save()
```

**Crear app:**
```bash
python manage.py startapp notificaciones
```

**Registrar en settings:**
```python
INSTALLED_APPS = [
    # ...
    'apps.notificaciones',
]
```

#### 1.6 Crear migraciones

```bash
# Crear apps nuevas
python manage.py startapp escuelas
python manage.py startapp notificaciones

# Hacer migraciones
python manage.py makemigrations escuelas
python manage.py makemigrations usuarios
python manage.py makemigrations observaciones
python manage.py makemigrations informes
python manage.py makemigrations notificaciones

# Aplicar migraciones
python manage.py migrate
```

**Checklist Fase 1:**
- [ ] Crear app `escuelas`
- [ ] Crear modelo `Escuela`
- [ ] Modificar modelo `Usuario` (+ presidente, secretaria, escuela)
- [ ] Crear modelo `BancoObservacionesDocente`
- [ ] Modificar modelo `Informe` (+ nuevos campos y estados)
- [ ] Crear app `notificaciones`
- [ ] Crear modelo `Notificacion`
- [ ] Crear y aplicar migraciones
- [ ] Verificar que no hay errores en BD

---

### FASE 2: CAPA DE NEGOCIO (Servicios)

**Objetivo:** Implementar lógica de negocio en servicios reutilizables

**Duración estimada:** 5-6 horas

#### 2.1 Servicio de Escuelas

**Archivo:** `apps/escuelas/services.py` (nuevo)

```python
"""
Servicio de negocio para gestión de escuelas
Capa de Negocio - Clean Architecture
"""
from apps.escuelas.models import Escuela
from apps.usuarios.models import Usuario

class EscuelaService:
    """
    Servicio para gestionar escuelas profesionales
    """
    
    @staticmethod
    def obtener_todas_activas():
        """Obtener todas las escuelas activas"""
        return Escuela.objects.filter(activo=True).select_related('presidente')
    
    @staticmethod
    def obtener_por_codigo(codigo):
        """Obtener escuela por código"""
        try:
            return Escuela.objects.get(codigo=codigo, activo=True)
        except Escuela.DoesNotExist:
            return None
    
    @staticmethod
    def asignar_presidente(escuela_id, presidente_id):
        """Asignar presidente a una escuela"""
        try:
            escuela = Escuela.objects.get(id=escuela_id)
            presidente = Usuario.objects.get(id=presidente_id, tipo_usuario='presidente')
            escuela.presidente = presidente
            escuela.save()
            return escuela
        except (Escuela.DoesNotExist, Usuario.DoesNotExist):
            return None
    
    @staticmethod
    def obtener_docentes_de_escuela(escuela_id):
        """Obtener todos los docentes de una escuela"""
        return Usuario.objects.filter(
            escuela_id=escuela_id,
            tipo_usuario='docente',
            activo=True
        )
```

#### 2.2 Servicio de Notificaciones

**Archivo:** `apps/notificaciones/services.py` (nuevo)

```python
"""
Servicio de notificaciones
Capa de Negocio - Clean Architecture
"""
from apps.notificaciones.models import Notificacion
from apps.usuarios.models import Usuario
from apps.informes.models import Informe

class NotificacionService:
    """
    Servicio para gestionar notificaciones
    """
    
    @staticmethod
    def crear_notificacion(usuario, informe, tipo, titulo, mensaje):
        """
        Crear una nueva notificación
        
        Args:
            usuario: Usuario que recibe la notificación
            informe: Informe relacionado
            tipo: Tipo de notificación
            titulo: Título
            mensaje: Mensaje completo
        
        Returns:
            Notificacion creada
        """
        return Notificacion.objects.create(
            usuario=usuario,
            informe=informe,
            tipo=tipo,
            titulo=titulo,
            mensaje=mensaje
        )
    
    @staticmethod
    def notificar_nuevo_informe_a_secretaria(informe):
        """
        Notificar a secretaria cuando estudiante envía informe
        """
        # Obtener secretaria activa (podría ser un sistema de rotación)
        secretaria = Usuario.objects.filter(
            tipo_usuario='secretaria',
            activo=True
        ).first()
        
        if not secretaria:
            return None
        
        return NotificacionService.crear_notificacion(
            usuario=secretaria,
            informe=informe,
            tipo='nuevo_informe',
            titulo='Nuevo Informe Recibido',
            mensaje=f'El estudiante {informe.usuario.nombre} ({informe.usuario.codigo}) '
                    f'ha enviado el informe "{informe.nombre_archivo}". '
                    f'Debe ser derivado a la escuela correspondiente.'
        )
    
    @staticmethod
    def notificar_asignacion_presidente(informe, presidente):
        """
        Notificar a presidente cuando secretaria deriva informe
        """
        return NotificacionService.crear_notificacion(
            usuario=presidente,
            informe=informe,
            tipo='asignado_presidente',
            titulo='Informe Asignado a su Escuela',
            mensaje=f'Se le ha asignado el informe "{informe.nombre_archivo}" '
                    f'del estudiante {informe.usuario.nombre}. '
                    f'Debe designar un docente revisor.'
        )
    
    @staticmethod
    def notificar_asignacion_docente(informe, docente):
        """
        Notificar a docente cuando presidente le asigna informe
        """
        return NotificacionService.crear_notificacion(
            usuario=docente,
            informe=informe,
            tipo='asignado_docente',
            titulo='Informe Asignado para Revisión',
            mensaje=f'El presidente {informe.presidente_asignado.nombre} le ha asignado '
                    f'el informe "{informe.nombre_archivo}" del estudiante {informe.usuario.nombre}. '
                    f'Debe revisar el informe con su banco de observaciones.'
        )
    
    @staticmethod
    def notificar_revision_completa_a_presidente(informe):
        """
        Notificar a presidente cuando docente completa revisión
        """
        return NotificacionService.crear_notificacion(
            usuario=informe.presidente_asignado,
            informe=informe,
            tipo='revision_completa',
            titulo='Revisión de Docente Completada',
            mensaje=f'El docente {informe.docente_revisor.nombre} ha completado '
                    f'la revisión del informe "{informe.nombre_archivo}". '
                    f'Debe aprobar o rechazar el dictamen.'
        )
    
    @staticmethod
    def notificar_aprobacion_presidente_a_secretaria(informe):
        """
        Notificar a secretaria cuando presidente aprueba
        """
        return NotificacionService.crear_notificacion(
            usuario=informe.secretaria_asignada,
            informe=informe,
            tipo='aprobado_presidente',
            titulo='Informe Aprobado por Presidente',
            mensaje=f'El presidente {informe.presidente_asignado.nombre} ha aprobado '
                    f'el informe "{informe.nombre_archivo}". '
                    f'Debe notificar al estudiante.'
        )
    
    @staticmethod
    def notificar_aprobacion_final_a_estudiante(informe):
        """
        Notificar a estudiante cuando es aprobado
        """
        return NotificacionService.crear_notificacion(
            usuario=informe.usuario,
            informe=informe,
            tipo='aprobado_final',
            titulo='¡Informe APROBADO!',
            mensaje=f'¡Felicitaciones! Su informe "{informe.nombre_archivo}" '
                    f'ha sido APROBADO. El proceso de validación ha concluido exitosamente.'
        )
    
    @staticmethod
    def notificar_rechazo_a_estudiante(informe):
        """
        Notificar a estudiante cuando es rechazado
        """
        return NotificacionService.crear_notificacion(
            usuario=informe.usuario,
            informe=informe,
            tipo='rechazado_estudiante',
            titulo='Informe Rechazado - Requiere Correcciones',
            mensaje=f'Su informe "{informe.nombre_archivo}" requiere correcciones. '
                    f'Por favor revise las observaciones y vuelva a enviar. '
                    f'Comentario del docente: {informe.comentario_docente or "N/A"}'
        )
    
    @staticmethod
    def obtener_no_leidas(usuario):
        """Obtener notificaciones no leídas de un usuario"""
        return Notificacion.objects.filter(
            usuario=usuario,
            leida=False
        ).select_related('informe', 'informe__usuario')
    
    @staticmethod
    def contar_no_leidas(usuario):
        """Contar notificaciones no leídas"""
        return Notificacion.objects.filter(
            usuario=usuario,
            leida=False
        ).count()
```

#### 2.3 Servicio de Secretaria

**Archivo:** `apps/negocio/servicios/secretaria.py` (nuevo)

```python
"""
Servicio de negocio para funciones de Secretaria
Capa de Negocio - Clean Architecture
"""
from django.utils import timezone
from apps.informes.models import Informe
from apps.escuelas.models import Escuela
from apps.notificaciones.services import NotificacionService

class SecretariaService:
    """
    Lógica de negocio para operaciones de Secretaria
    """
    
    @staticmethod
    def obtener_informes_pendientes():
        """Obtener informes pendientes de derivar"""
        return Informe.objects.filter(
            estado=Informe.ESTADO_PENDIENTE_SECRETARIA
        ).select_related('usuario', 'escuela')
    
    @staticmethod
    def derivar_a_presidente(informe_id, escuela_id, secretaria):
        """
        Derivar informe a presidente de escuela
        
        Args:
            informe_id: ID del informe
            escuela_id: ID de la escuela
            secretaria: Usuario secretaria
        
        Returns:
            tuple: (success: bool, informe: Informe, error: str)
        """
        try:
            informe = Informe.objects.get(id=informe_id)
            escuela = Escuela.objects.get(id=escuela_id)
            
            # Validar que la escuela tenga presidente
            if not escuela.presidente:
                return False, None, "La escuela seleccionada no tiene presidente asignado"
            
            # Actualizar informe
            informe.secretaria_asignada = secretaria
            informe.escuela = escuela
            informe.presidente_asignado = escuela.presidente
            informe.fecha_asignacion_secretaria = timezone.now()
            informe.transition_to(Informe.ESTADO_PENDIENTE_PRESIDENTE)
            informe.save()
            
            # Notificar al presidente
            NotificacionService.notificar_asignacion_presidente(
                informe, 
                escuela.presidente
            )
            
            return True, informe, None
            
        except (Informe.DoesNotExist, Escuela.DoesNotExist) as e:
            return False, None, str(e)
    
    @staticmethod
    def obtener_informes_enviados(secretaria):
        """Obtener informes que esta secretaria derivó"""
        return Informe.objects.filter(
            secretaria_asignada=secretaria
        ).exclude(
            estado=Informe.ESTADO_PENDIENTE_SECRETARIA
        ).select_related('usuario', 'escuela', 'presidente_asignado')
    
    @staticmethod
    def obtener_informes_aprobados_pendientes_notificar(secretaria):
        """Obtener informes aprobados por presidente pendientes de notificar"""
        return Informe.objects.filter(
            secretaria_asignada=secretaria,
            estado=Informe.ESTADO_APROBADO_PRESIDENTE
        ).select_related('usuario', 'presidente_asignado')
    
    @staticmethod
    def notificar_estudiante_aprobado(informe_id):
        """
        Notificar a estudiante que su informe fue aprobado
        
        Args:
            informe_id: ID del informe
        
        Returns:
            tuple: (success: bool, informe: Informe, error: str)
        """
        try:
            informe = Informe.objects.get(id=informe_id)
            
            # Actualizar estado
            informe.transition_to(Informe.ESTADO_APROBADO_FINAL)
            informe.fecha_completado = timezone.now()
            informe.save()
            
            # Notificar al estudiante
            NotificacionService.notificar_aprobacion_final_a_estudiante(informe)
            
            return True, informe, None
            
        except Informe.DoesNotExist as e:
            return False, None, str(e)
```

#### 2.4 Servicio de Presidente

**Archivo:** `apps/negocio/servicios/presidente.py` (nuevo)

```python
"""
Servicio de negocio para funciones de Presidente
Capa de Negocio - Clean Architecture
"""
from django.utils import timezone
from apps.informes.models import Informe
from apps.usuarios.models import Usuario
from apps.notificaciones.services import NotificacionService

class PresidenteService:
    """
    Lógica de negocio para operaciones de Presidente de Escuela
    """
    
    @staticmethod
    def obtener_informes_pendientes_asignar(presidente):
        """Obtener informes pendientes de asignar docente"""
        return Informe.objects.filter(
            presidente_asignado=presidente,
            estado=Informe.ESTADO_PENDIENTE_PRESIDENTE
        ).select_related('usuario', 'escuela')
    
    @staticmethod
    def obtener_informes_en_revision(presidente):
        """Obtener informes que están siendo revisados por docentes"""
        return Informe.objects.filter(
            presidente_asignado=presidente,
            estado__in=[
                Informe.ESTADO_PENDIENTE_DOCENTE,
                Informe.ESTADO_VALIDANDO_IA,
                Informe.ESTADO_REVISION_DOCENTE
            ]
        ).select_related('usuario', 'docente_revisor')
    
    @staticmethod
    def obtener_informes_pendientes_aprobar(presidente):
        """Obtener informes pendientes de aprobación del presidente"""
        return Informe.objects.filter(
            presidente_asignado=presidente,
            estado=Informe.ESTADO_PENDIENTE_APROBACION_PRESIDENTE
        ).select_related('usuario', 'docente_revisor')
    
    @staticmethod
    def obtener_docentes_disponibles(presidente):
        """Obtener docentes de la escuela del presidente"""
        if not presidente.escuela:
            return Usuario.objects.none()
        
        return Usuario.objects.filter(
            escuela=presidente.escuela,
            tipo_usuario='docente',
            activo=True
        )
    
    @staticmethod
    def designar_docente(informe_id, docente_id):
        """
        Designar docente revisor a un informe
        
        Args:
            informe_id: ID del informe
            docente_id: ID del docente
        
        Returns:
            tuple: (success: bool, informe: Informe, error: str)
        """
        try:
            informe = Informe.objects.get(id=informe_id)
            docente = Usuario.objects.get(
                id=docente_id,
                tipo_usuario='docente',
                activo=True
            )
            
            # Validar que el docente pertenece a la misma escuela
            if informe.escuela != docente.escuela:
                return False, None, "El docente no pertenece a la escuela del informe"
            
            # Actualizar informe
            informe.docente_revisor = docente
            informe.fecha_asignacion_docente = timezone.now()
            informe.transition_to(Informe.ESTADO_PENDIENTE_DOCENTE)
            informe.save()
            
            # Notificar al docente
            NotificacionService.notificar_asignacion_docente(informe, docente)
            
            return True, informe, None
            
        except (Informe.DoesNotExist, Usuario.DoesNotExist) as e:
            return False, None, str(e)
    
    @staticmethod
    def aprobar_dictamen_docente(informe_id, comentario_presidente=""):
        """
        Aprobar el dictamen del docente
        
        Args:
            informe_id: ID del informe
            comentario_presidente: Comentario opcional del presidente
        
        Returns:
            tuple: (success: bool, informe: Informe, error: str)
        """
        try:
            informe = Informe.objects.get(id=informe_id)
            
            # Actualizar informe
            informe.comentario_presidente = comentario_presidente
            informe.fecha_aprobacion_presidente = timezone.now()
            informe.transition_to(Informe.ESTADO_APROBADO_PRESIDENTE)
            informe.save()
            
            # Notificar a secretaria
            NotificacionService.notificar_aprobacion_presidente_a_secretaria(informe)
            
            return True, informe, None
            
        except Informe.DoesNotExist as e:
            return False, None, str(e)
    
    @staticmethod
    def rechazar_dictamen_docente(informe_id, comentario_presidente):
        """
        Rechazar el dictamen del docente (vuelve a revisión docente)
        
        Args:
            informe_id: ID del informe
            comentario_presidente: Motivo del rechazo
        
        Returns:
            tuple: (success: bool, informe: Informe, error: str)
        """
        try:
            informe = Informe.objects.get(id=informe_id)
            
            # Actualizar informe
            informe.comentario_presidente = comentario_presidente
            informe.transition_to(Informe.ESTADO_RECHAZADO_PRESIDENTE)
            informe.save()
            
            # Notificar al docente (reutilizamos notificación de asignación)
            NotificacionService.crear_notificacion(
                usuario=informe.docente_revisor,
                informe=informe,
                tipo='rechazado_presidente',
                titulo='Dictamen Rechazado por Presidente',
                mensaje=f'El presidente {informe.presidente_asignado.nombre} ha rechazado '
                        f'su dictamen del informe "{informe.nombre_archivo}". '
                        f'Motivo: {comentario_presidente}. '
                        f'Debe revisar nuevamente el informe.'
            )
            
            return True, informe, None
            
        except Informe.DoesNotExist as e:
            return False, None, str(e)
```

#### 2.5 Servicio de Docente (ampliado)

**Archivo:** `apps/negocio/servicios/docente.py` (nuevo)

```python
"""
Servicio de negocio para funciones de Docente
Capa de Negocio - Clean Architecture
"""
from django.utils import timezone
from apps.informes.models import Informe
from apps.observaciones.models import BancoObservacionesDocente, ObservacionGenerada
from apps.notificaciones.services import NotificacionService
import docx
import pypdf

class DocenteService:
    """
    Lógica de negocio para operaciones de Docente
    """
    
    @staticmethod
    def obtener_informes_asignados(docente):
        """Obtener informes asignados a este docente"""
        return Informe.objects.filter(
            docente_revisor=docente,
            estado__in=[
                Informe.ESTADO_PENDIENTE_DOCENTE,
                Informe.ESTADO_VALIDANDO_IA,
                Informe.ESTADO_REVISION_DOCENTE,
                Informe.ESTADO_RECHAZADO_PRESIDENTE
            ]
        ).select_related('usuario', 'presidente_asignado')
    
    @staticmethod
    def obtener_banco_activo(docente):
        """Obtener el banco de observaciones activo del docente"""
        return BancoObservacionesDocente.objects.filter(
            docente=docente,
            activo=True
        ).first()
    
    @staticmethod
    def obtener_todos_bancos(docente):
        """Obtener todos los bancos del docente"""
        return BancoObservacionesDocente.objects.filter(
            docente=docente
        ).order_by('-activo', '-fecha_creacion')
    
    @staticmethod
    def crear_banco_observaciones(docente, nombre, archivo):
        """
        Crear un nuevo banco de observaciones para el docente
        
        Args:
            docente: Usuario docente
            nombre: Nombre descriptivo del banco
            archivo: Archivo PDF o DOCX
        
        Returns:
            tuple: (success: bool, banco: BancoObservacionesDocente, error: str)
        """
        try:
            # Extraer contenido del archivo
            contenido = DocenteService._extraer_contenido_archivo(archivo)
            
            # Crear banco
            banco = BancoObservacionesDocente.objects.create(
                docente=docente,
                nombre=nombre,
                archivo=archivo,
                contenido_extraido=contenido,
                activo=True  # Al crear se vuelve activo automáticamente
            )
            
            return True, banco, None
            
        except Exception as e:
            return False, None, str(e)
    
    @staticmethod
    def _extraer_contenido_archivo(archivo):
        """
        Extraer texto de archivo PDF o DOCX
        
        Args:
            archivo: FileField de Django
        
        Returns:
            str: Contenido extraído
        """
        nombre = archivo.name.lower()
        
        if nombre.endswith('.docx'):
            doc = docx.Document(archivo)
            return '\n'.join([p.text for p in doc.paragraphs])
        
        elif nombre.endswith('.pdf'):
            reader = pypdf.PdfReader(archivo)
            texto = []
            for page in reader.pages:
                texto.append(page.extract_text())
            return '\n'.join(texto)
        
        else:
            raise ValueError("Formato no soportado. Solo PDF o DOCX.")
    
    @staticmethod
    def activar_banco(banco_id, docente):
        """
        Activar un banco específico (desactiva los demás)
        
        Args:
            banco_id: ID del banco a activar
            docente: Usuario docente propietario
        
        Returns:
            tuple: (success: bool, banco: BancoObservacionesDocente, error: str)
        """
        try:
            # Desactivar todos los bancos del docente
            BancoObservacionesDocente.objects.filter(
                docente=docente
            ).update(activo=False)
            
            # Activar el seleccionado
            banco = BancoObservacionesDocente.objects.get(
                id=banco_id,
                docente=docente
            )
            banco.activo = True
            banco.save()
            
            return True, banco, None
            
        except BancoObservacionesDocente.DoesNotExist:
            return False, None, "Banco no encontrado"
    
    @staticmethod
    def validar_informe_con_ia(informe_id, docente):
        """
        Validar informe usando IA con el banco del docente
        
        Args:
            informe_id: ID del informe
            docente: Usuario docente
        
        Returns:
            tuple: (success: bool, observaciones: list, error: str)
        """
        try:
            informe = Informe.objects.get(id=informe_id)
            banco = DocenteService.obtener_banco_activo(docente)
            
            if not banco:
                return False, [], "No tiene un banco de observaciones activo"
            
            # Actualizar estado
            informe.banco_observaciones_usado = banco
            informe.transition_to(Informe.ESTADO_VALIDANDO_IA)
            informe.save()
            
            # Llamar al servicio de IA (importar dinámicamente para evitar circular import)
            from apps.observaciones.services import validar_informe_con_ia
            
            observaciones = validar_informe_con_ia(
                contenido_informe=informe.contenido,
                banco_observaciones=banco.contenido_extraido
            )
            
            # Crear observaciones generadas
            for obs in observaciones:
                ObservacionGenerada.objects.create(
                    informe=informe,
                    seccion=obs.get('seccion', 'General'),
                    observacion=obs.get('observacion', ''),
                    ubicacion_error=obs.get('ubicacion', 'No especificada'),
                    severidad=obs.get('severidad', ObservacionGenerada.SEVERIDAD_IMPORTANTE),
                    estado=ObservacionGenerada.ESTADO_PENDIENTE
                )
            
            # Actualizar estado a revisión
            informe.transition_to(Informe.ESTADO_REVISION_DOCENTE)
            informe.save()
            
            return True, observaciones, None
            
        except Informe.DoesNotExist:
            return False, [], "Informe no encontrado"
        except Exception as e:
            return False, [], str(e)
    
    @staticmethod
    def enviar_dictamen_a_presidente(informe_id, comentario_docente, aprobar=True):
        """
        Enviar dictamen final al presidente
        
        Args:
            informe_id: ID del informe
            comentario_docente: Comentario del docente
            aprobar: Si recomienda aprobar o no
        
        Returns:
            tuple: (success: bool, informe: Informe, error: str)
        """
        try:
            informe = Informe.objects.get(id=informe_id)
            
            # Actualizar informe
            informe.comentario_docente = comentario_docente
            informe.fecha_revision_docente = timezone.now()
            informe.transition_to(Informe.ESTADO_PENDIENTE_APROBACION_PRESIDENTE)
            informe.save()
            
            # Notificar al presidente
            NotificacionService.notificar_revision_completa_a_presidente(informe)
            
            return True, informe, None
            
        except Informe.DoesNotExist:
            return False, None, "Informe no encontrado"
```

**Checklist Fase 2:**
- [ ] Crear `EscuelaService`
- [ ] Crear `NotificacionService`
- [ ] Crear `SecretariaService`
- [ ] Crear `PresidenteService`
- [ ] Crear `DocenteService`
- [ ] Modificar `apps/observaciones/services.py` para IA con banco docente
- [ ] Modificar máquina de estados en `apps/informes/state.py`
- [ ] Probar cada servicio individualmente

---

### FASE 3: CAPA DE PRESENTACIÓN - VISTAS

**Objetivo:** Crear vistas para cada rol

**Duración estimada:** 6-7 horas

#### 3.1 Vistas de Secretaria

**Archivo:** `apps/presentacion/web/secretaria_views.py` (nuevo)

```python
"""
Vistas para Secretaria
Capa de Presentación - Clean Architecture
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.negocio.servicios.secretaria import SecretariaService
from apps.escuelas.services import EscuelaService
from apps.usuarios.models import Usuario
from apps.informes.models import Informe

def secretaria_dashboard(request):
    """Dashboard principal de secretaria"""
    # Verificar sesión
    if 'usuario_id' not in request.session:
        return redirect('login_secretaria')
    
    if request.session.get('usuario_tipo') != 'secretaria':
        messages.error(request, 'Acceso denegado. Solo secretarias pueden acceder.')
        return redirect('login')
    
    secretaria = Usuario.objects.get(id=request.session['usuario_id'])
    
    # Obtener datos
    informes_pendientes = SecretariaService.obtener_informes_pendientes()
    informes_enviados = SecretariaService.obtener_informes_enviados(secretaria)
    informes_aprobados = SecretariaService.obtener_informes_aprobados_pendientes_notificar(secretaria)
    
    # Estadísticas
    total_pendientes = informes_pendientes.count()
    total_en_proceso = informes_enviados.filter(
        estado__in=[
            Informe.ESTADO_PENDIENTE_PRESIDENTE,
            Informe.ESTADO_PENDIENTE_DOCENTE,
            Informe.ESTADO_VALIDANDO_IA,
            Informe.ESTADO_REVISION_DOCENTE,
            Informe.ESTADO_PENDIENTE_APROBACION_PRESIDENTE
        ]
    ).count()
    total_aprobados_hoy = informes_aprobados.count()
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'informes_pendientes': informes_pendientes[:10],  # Últimos 10
        'informes_enviados': informes_enviados[:10],
        'informes_aprobados': informes_aprobados,
        'total_pendientes': total_pendientes,
        'total_en_proceso': total_en_proceso,
        'total_aprobados_hoy': total_aprobados_hoy,
    }
    
    return render(request, 'secretaria/dashboard.html', context)

def secretaria_derivar(request, informe_id):
    """Derivar informe a presidente de escuela"""
    if 'usuario_id' not in request.session:
        return redirect('login_secretaria')
    
    if request.session.get('usuario_tipo') != 'secretaria':
        messages.error(request, 'Acceso denegado.')
        return redirect('login')
    
    secretaria = Usuario.objects.get(id=request.session['usuario_id'])
    informe = get_object_or_404(Informe, id=informe_id)
    
    if request.method == 'POST':
        escuela_id = request.POST.get('escuela_id')
        comentario = request.POST.get('comentario', '')
        
        success, informe_actualizado, error = SecretariaService.derivar_a_presidente(
            informe_id, escuela_id, secretaria
        )
        
        if success:
            messages.success(request, f'Informe derivado exitosamente a {informe_actualizado.escuela.nombre}')
            return redirect('secretaria_dashboard')
        else:
            messages.error(request, f'Error al derivar: {error}')
    
    # GET: Mostrar formulario
    escuelas = EscuelaService.obtener_todas_activas()
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'informe': informe,
        'escuelas': escuelas,
    }
    
    return render(request, 'secretaria/derivar.html', context)

def secretaria_notificar_estudiante(request, informe_id):
    """Notificar resultado final al estudiante"""
    if 'usuario_id' not in request.session:
        return redirect('login_secretaria')
    
    if request.session.get('usuario_tipo') != 'secretaria':
        messages.error(request, 'Acceso denegado.')
        return redirect('login')
    
    informe = get_object_or_404(Informe, id=informe_id)
    
    if request.method == 'POST':
        success, informe_actualizado, error = SecretariaService.notificar_estudiante_aprobado(informe_id)
        
        if success:
            messages.success(request, f'Estudiante {informe.usuario.nombre} notificado exitosamente.')
            return redirect('secretaria_dashboard')
        else:
            messages.error(request, f'Error: {error}')
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'informe': informe,
    }
    
    return render(request, 'secretaria/notificar.html', context)
```

#### 3.2 Vistas de Presidente

**Archivo:** `apps/presentacion/web/presidente_views.py` (nuevo)

```python
"""
Vistas para Presidente de Escuela
Capa de Presentación - Clean Architecture
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.negocio.servicios.presidente import PresidenteService
from apps.usuarios.models import Usuario
from apps.informes.models import Informe

def presidente_dashboard(request):
    """Dashboard principal de presidente"""
    if 'usuario_id' not in request.session:
        return redirect('login_presidente')
    
    if request.session.get('usuario_tipo') != 'presidente':
        messages.error(request, 'Acceso denegado. Solo presidentes pueden acceder.')
        return redirect('login')
    
    presidente = Usuario.objects.get(id=request.session['usuario_id'])
    
    # Obtener datos
    pendientes_asignar = PresidenteService.obtener_informes_pendientes_asignar(presidente)
    en_revision = PresidenteService.obtener_informes_en_revision(presidente)
    pendientes_aprobar = PresidenteService.obtener_informes_pendientes_aprobar(presidente)
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'escuela': presidente.escuela.nombre if presidente.escuela else 'Sin escuela',
        'pendientes_asignar': pendientes_asignar,
        'en_revision': en_revision,
        'pendientes_aprobar': pendientes_aprobar,
        'total_pendientes_asignar': pendientes_asignar.count(),
        'total_en_revision': en_revision.count(),
        'total_pendientes_aprobar': pendientes_aprobar.count(),
    }
    
    return render(request, 'presidente/dashboard.html', context)

def presidente_designar_docente(request, informe_id):
    """Designar docente revisor"""
    if 'usuario_id' not in request.session:
        return redirect('login_presidente')
    
    if request.session.get('usuario_tipo') != 'presidente':
        messages.error(request, 'Acceso denegado.')
        return redirect('login')
    
    presidente = Usuario.objects.get(id=request.session['usuario_id'])
    informe = get_object_or_404(Informe, id=informe_id, presidente_asignado=presidente)
    
    if request.method == 'POST':
        docente_id = request.POST.get('docente_id')
        
        success, informe_actualizado, error = PresidenteService.designar_docente(
            informe_id, docente_id
        )
        
        if success:
            messages.success(request, f'Docente {informe_actualizado.docente_revisor.nombre} asignado exitosamente.')
            return redirect('presidente_dashboard')
        else:
            messages.error(request, f'Error: {error}')
    
    # GET: Mostrar formulario
    docentes = PresidenteService.obtener_docentes_disponibles(presidente)
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'informe': informe,
        'docentes': docentes,
    }
    
    return render(request, 'presidente/designar_docente.html', context)

def presidente_revisar_dictamen(request, informe_id):
    """Revisar dictamen del docente y aprobar/rechazar"""
    if 'usuario_id' not in request.session:
        return redirect('login_presidente')
    
    if request.session.get('usuario_tipo') != 'presidente':
        messages.error(request, 'Acceso denegado.')
        return redirect('login')
    
    presidente = Usuario.objects.get(id=request.session['usuario_id'])
    informe = get_object_or_404(
        Informe, 
        id=informe_id, 
        presidente_asignado=presidente,
        estado=Informe.ESTADO_PENDIENTE_APROBACION_PRESIDENTE
    )
    
    if request.method == 'POST':
        accion = request.POST.get('accion')  # 'aprobar' o 'rechazar'
        comentario = request.POST.get('comentario', '')
        
        if accion == 'aprobar':
            success, informe_actualizado, error = PresidenteService.aprobar_dictamen_docente(
                informe_id, comentario
            )
            if success:
                messages.success(request, 'Dictamen aprobado. Secretaría ha sido notificada.')
                return redirect('presidente_dashboard')
            else:
                messages.error(request, f'Error: {error}')
        
        elif accion == 'rechazar':
            if not comentario:
                messages.error(request, 'Debe proporcionar un motivo para rechazar.')
            else:
                success, informe_actualizado, error = PresidenteService.rechazar_dictamen_docente(
                    informe_id, comentario
                )
                if success:
                    messages.warning(request, 'Dictamen rechazado. El docente ha sido notificado.')
                    return redirect('presidente_dashboard')
                else:
                    messages.error(request, f'Error: {error}')
    
    # Obtener observaciones
    observaciones = informe.observaciones.all().order_by('seccion')
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'informe': informe,
        'observaciones': observaciones,
        'total_observaciones': observaciones.count(),
        'observaciones_confirmadas': observaciones.filter(estado='confirmada').count(),
    }
    
    return render(request, 'presidente/revisar_dictamen.html', context)
```

#### 3.3 Vistas de Docente (ampliadas)

**Archivo:** `apps/presentacion/web/docente_views.py` (modificar/ampliar)

```python
"""
Vistas para Docente
Capa de Presentación - Clean Architecture
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.negocio.servicios.docente import DocenteService
from apps.usuarios.models import Usuario
from apps.informes.models import Informe
from apps.observaciones.models import ObservacionGenerada

def docente_dashboard(request):
    """Dashboard principal de docente"""
    if 'usuario_id' not in request.session:
        return redirect('login_docente')
    
    if request.session.get('usuario_tipo') != 'docente':
        messages.error(request, 'Acceso denegado.')
        return redirect('login')
    
    docente = Usuario.objects.get(id=request.session['usuario_id'])
    
    # Obtener datos
    informes_asignados = DocenteService.obtener_informes_asignados(docente)
    banco_activo = DocenteService.obtener_banco_activo(docente)
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'informes_asignados': informes_asignados,
        'total_asignados': informes_asignados.count(),
        'banco_activo': banco_activo,
        'tiene_banco': banco_activo is not None,
    }
    
    return render(request, 'docente/dashboard.html', context)

def docente_banco_observaciones(request):
    """Gestionar bancos de observaciones"""
    if 'usuario_id' not in request.session:
        return redirect('login_docente')
    
    if request.session.get('usuario_tipo') != 'docente':
        messages.error(request, 'Acceso denegado.')
        return redirect('login')
    
    docente = Usuario.objects.get(id=request.session['usuario_id'])
    
    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        if accion == 'crear':
            nombre = request.POST.get('nombre')
            archivo = request.FILES.get('archivo')
            
            if not nombre or not archivo:
                messages.error(request, 'Debe proporcionar nombre y archivo.')
            else:
                success, banco, error = DocenteService.crear_banco_observaciones(
                    docente, nombre, archivo
                )
                if success:
                    messages.success(request, f'Banco "{nombre}" creado y activado exitosamente.')
                    return redirect('docente_banco_observaciones')
                else:
                    messages.error(request, f'Error: {error}')
        
        elif accion == 'activar':
            banco_id = request.POST.get('banco_id')
            success, banco, error = DocenteService.activar_banco(banco_id, docente)
            if success:
                messages.success(request, f'Banco "{banco.nombre}" activado.')
                return redirect('docente_banco_observaciones')
            else:
                messages.error(request, f'Error: {error}')
    
    # GET: Mostrar lista
    bancos = DocenteService.obtener_todos_bancos(docente)
    banco_activo = DocenteService.obtener_banco_activo(docente)
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'bancos': bancos,
        'banco_activo': banco_activo,
    }
    
    return render(request, 'docente/banco_observaciones.html', context)

def docente_revisar_informe(request, informe_id):
    """Revisar informe con IA y tabla editable"""
    if 'usuario_id' not in request.session:
        return redirect('login_docente')
    
    if request.session.get('usuario_tipo') != 'docente':
        messages.error(request, 'Acceso denegado.')
        return redirect('login')
    
    docente = Usuario.objects.get(id=request.session['usuario_id'])
    informe = get_object_or_404(Informe, id=informe_id, docente_revisor=docente)
    
    # Si no se ha validado con IA, validar primero
    if informe.estado == Informe.ESTADO_PENDIENTE_DOCENTE:
        success, observaciones, error = DocenteService.validar_informe_con_ia(
            informe_id, docente
        )
        if not success:
            messages.error(request, f'Error al validar con IA: {error}')
            return redirect('docente_dashboard')
        
        messages.info(request, f'Validación con IA completada. {len(observaciones)} observaciones generadas.')
    
    # Procesar formulario de edición
    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        if accion == 'actualizar_observaciones':
            # Actualizar cada observación
            observaciones = informe.observaciones.all()
            for obs in observaciones:
                obs_accion = request.POST.get(f'obs_accion_{obs.id}')
                obs_comentario = request.POST.get(f'obs_comentario_{obs.id}', '')
                obs_severidad = request.POST.get(f'obs_severidad_{obs.id}')
                
                if obs_accion == 'confirmar':
                    obs.estado = ObservacionGenerada.ESTADO_CONFIRMADA
                elif obs_accion == 'descartar':
                    obs.estado = ObservacionGenerada.ESTADO_DESCARTADA
                
                obs.comentario_docente = obs_comentario
                if obs_severidad:
                    obs.severidad = obs_severidad
                obs.save()
            
            messages.success(request, 'Observaciones actualizadas.')
        
        elif accion == 'enviar_dictamen':
            comentario_general = request.POST.get('comentario_general')
            aprobar = request.POST.get('recomendar') == 'aprobar'
            
            success, informe_actualizado, error = DocenteService.enviar_dictamen_a_presidente(
                informe_id, comentario_general, aprobar
            )
            
            if success:
                messages.success(request, 'Dictamen enviado al presidente exitosamente.')
                return redirect('docente_dashboard')
            else:
                messages.error(request, f'Error: {error}')
    
    # Obtener observaciones
    observaciones = informe.observaciones.all().order_by('seccion')
    obs_confirmadas = observaciones.filter(estado=ObservacionGenerada.ESTADO_CONFIRMADA)
    obs_pendientes = observaciones.filter(estado=ObservacionGenerada.ESTADO_PENDIENTE)
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'informe': informe,
        'observaciones': observaciones,
        'obs_confirmadas': obs_confirmadas,
        'obs_pendientes': obs_pendientes,
        'total_observaciones': observaciones.count(),
    }
    
    return render(request, 'docente/revisar_informe.html', context)
```

**Checklist Fase 3:**
- [ ] Crear vistas de Secretaria (dashboard, derivar, notificar)
- [ ] Crear vistas de Presidente (dashboard, designar, revisar dictamen)
- [ ] Ampliar vistas de Docente (banco, revisar con IA, tabla editable)
- [ ] Modificar vistas de Estudiante (mejorar notificaciones)
- [ ] Crear vistas de login para cada rol
- [ ] Actualizar URLs en `apps/core/urls.py`

---

### FASE 4: CAPA DE PRESENTACIÓN - TEMPLATES

**Objetivo:** Crear interfaces de usuario con botones y UI completa

**Duración estimada:** 6-8 horas

*(Continuará en siguiente sección debido a límite de caracteres...)*

---

## METAS Y PROGRESO

### Meta General
Implementar flujo completo de validación de informes con 5 roles y sistema de notificaciones.

### Progreso por Fases

| Fase | Nombre | Estado | Progreso | Tiempo Estimado | Tiempo Real |
|------|--------|--------|----------|-----------------|-------------|
| 0 | Análisis y Planificación | ✅ Completado | 100% | 2h | - |
| 1 | Capa de Datos | ⏳ Pendiente | 0% | 3-4h | - |
| 2 | Capa de Negocio | ⏳ Pendiente | 0% | 5-6h | - |
| 3 | Capa de Presentación - Vistas | ⏳ Pendiente | 0% | 6-7h | - |
| 4 | Capa de Presentación - Templates | ⏳ Pendiente | 0% | 6-8h | - |
| 5 | Testing y Depuración | ⏳ Pendiente | 0% | 4-5h | - |
| 6 | Documentación | ⏳ Pendiente | 0% | 2h | - |
| **TOTAL** | | **0%** | **0%** | **28-37h** | **0h** |

### Seguimiento Detallado

#### Fase 1: CAPA DE DATOS (0%)
- [ ] 0% - Crear app `escuelas`
- [ ] 0% - Crear modelo `Escuela`
- [ ] 0% - Modificar modelo `Usuario`
- [ ] 0% - Crear modelo `BancoObservacionesDocente`
- [ ] 0% - Modificar modelo `Informe`
- [ ] 0% - Crear app `notificaciones`
- [ ] 0% - Crear modelo `Notificacion`
- [ ] 0% - Crear migraciones
- [ ] 0% - Aplicar migraciones

#### Fase 2: CAPA DE NEGOCIO (0%)
- [ ] 0% - Crear `EscuelaService`
- [ ] 0% - Crear `NotificacionService`
- [ ] 0% - Crear `SecretariaService`
- [ ] 0% - Crear `PresidenteService`
- [ ] 0% - Crear `DocenteService`
- [ ] 0% - Modificar máquina de estados
- [ ] 0% - Actualizar servicio de IA

#### Fase 3: VISTAS (0%)
- [ ] 0% - Vistas de Secretaria
- [ ] 0% - Vistas de Presidente
- [ ] 0% - Vistas de Docente ampliadas
- [ ] 0% - Login por roles
- [ ] 0% - URLs actualizadas

#### Fase 4: TEMPLATES (0%)
- [ ] 0% - Templates de Secretaria
- [ ] 0% - Templates de Presidente
- [ ] 0% - Templates de Docente
- [ ] 0% - Componentes reutilizables
- [ ] 0% - Sistema de notificaciones UI

#### Fase 5: TESTING (0%)
- [ ] 0% - Tests de modelos
- [ ] 0% - Tests de servicios
- [ ] 0% - Tests de vistas
- [ ] 0% - Tests de flujo completo

#### Fase 6: DOCUMENTACIÓN (0%)
- [ ] 0% - Actualizar documentación de arquitectura
- [ ] 0% - Guía de uso para cada rol
- [ ] 0% - Diagramas actualizados

---

## CHECKLIST DE VERIFICACIÓN

### Modelos
- [ ] Escuela creada con presidente
- [ ] Usuario con roles presidente y secretaria
- [ ] BancoObservacionesDocente funcional
- [ ] Informe con nuevos estados y campos
- [ ] Notificacion funcional
- [ ] Todas las relaciones FK correctas
- [ ] Migraciones aplicadas sin errores

### Servicios
- [ ] EscuelaService con métodos básicos
- [ ] NotificacionService con todas las notificaciones
- [ ] SecretariaService con flujo completo
- [ ] PresidenteService con aprobar/rechazar
- [ ] DocenteService con banco y validación IA
- [ ] Máquina de estados actualizada
- [ ] Todos los servicios probados

### Vistas
- [ ] Secretaria: dashboard, derivar, notificar
- [ ] Presidente: dashboard, designar, revisar
- [ ] Docente: dashboard, banco, revisar IA, tabla editable
- [ ] Login separado por roles
- [ ] Protección de rutas por rol
- [ ] Mensajes de error y éxito

### Templates
- [ ] Secretaria: 3 templates completos
- [ ] Presidente: 4 templates completos
- [ ] Docente: 5 templates completos
- [ ] Componentes reutilizables
- [ ] Botones con acciones claras
- [ ] UI responsive con Bootstrap
- [ ] Notificaciones visuales

### Flujo Completo
- [ ] Estudiante puede enviar informe
- [ ] Secretaria recibe notificación
- [ ] Secretaria puede derivar a presidente
- [ ] Presidente recibe notificación
- [ ] Presidente puede designar docente
- [ ] Docente recibe notificación
- [ ] Docente puede subir banco
- [ ] Docente puede validar con IA usando su banco
- [ ] Docente puede editar observaciones
- [ ] Docente puede enviar dictamen
- [ ] Presidente recibe notificación de dictamen
- [ ] Presidente puede aprobar/rechazar
- [ ] Si rechaza, vuelve a docente
- [ ] Si aprueba, secretaria recibe notificación
- [ ] Secretaria notifica a estudiante
- [ ] Estudiante recibe resultado

### Testing
- [ ] Tests de modelos (save, validaciones)
- [ ] Tests de servicios (lógica de negocio)
- [ ] Tests de vistas (GET, POST, permisos)
- [ ] Tests de flujo completo end-to-end
- [ ] Todos los tests pasan (100%)

---

## GLOSARIO DE TÉRMINOS

| Término | Definición |
|---------|------------|
| **Clean Architecture** | Patrón de arquitectura que separa lógica de negocio de infraestructura |
| **Arquitectura de 3 Capas** | Presentación, Negocio, Datos - separadas claramente |
| **Capa de Datos** | Modelos, BD, repositorios - `apps/*/models.py` |
| **Capa de Negocio** | Servicios, lógica de aplicación - `apps/*/services.py` |
| **Capa de Presentación** | Vistas, templates, UI - `apps/*/views.py`, `templates/` |
| **Máquina de Estados** | Patrón para gestionar transiciones de estado del informe |
| **Banco de Observaciones** | Conjunto de observaciones comunes para validación |
| **Banco Global** | `BancoObservaciones` - usado por todos |
| **Banco Docente** | `BancoObservacionesDocente` - personal de cada docente |
| **IA** | Inteligencia Artificial (Groq API con LLaMA 3.3 70B) |
| **Dictamen** | Informe final del docente con recomendación |
| **Observación Generada** | Observación detectada por IA |
| **Estado del Informe** | Fase actual del informe en el flujo |
| **Transición** | Cambio de un estado a otro |
| **Notificación** | Mensaje enviado a un usuario sobre un evento |
| **FK** | Foreign Key - llave foránea en base de datos |
| **PMV** | Producto Mínimo Viable |

---

**FIN DEL DOCUMENTO - PARTE 1**

**CONTINÚA EN:** 
- Fase 4 completa (Templates detallados)
- Fase 5 (Testing)
- Fase 6 (Documentación final)
- Instrucciones de deployment

**PRÓXIMOS PASOS:**
1. Revisar este plan
2. Aprobar cambios propuestos
3. Comenzar implementación Fase 1

---

**Sistema desarrollado para UNTELS - Universidad Nacional Tecnológica de Lima Sur**  
**Arquitectura:** Clean Architecture + 3 Capas  
**Framework:** Django 5.0  
**Base de Datos:** PostgreSQL (producción) / SQLite (desarrollo)  
**IA:** Groq API (LLaMA 3.3 70B)
