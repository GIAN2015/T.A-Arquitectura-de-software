# CAPA DE DATOS

Sistema de Validación de Informes - UNTELS

---

## ¿QUÉ ES LA CAPA DE DATOS?

Es **la estructura de almacenamiento**. Define:

- Modelos de datos (tablas)
- Relaciones entre tablas
- Validaciones de integridad
- Acceso a la base de datos

**NO** contiene lógica de negocio ni presentación.

---

## BASE DE DATOS

### Desarrollo
- **Motor:** SQLite
- **Archivo:** `db.sqlite3`
- **Ubicación:** Raíz del proyecto

### Producción
- **Motor:** PostgreSQL 16
- **Host:** Configurado en Docker
- **Base de datos:** `untels_db`
- **Usuario:** `untels_user`

---

## MODELOS (5 TABLAS)

```
proyecto_untels/apps/
├── usuarios/
│   └── models.py                # Usuario
├── informes/
│   └── models.py                # Informe
├── reglamento/
│   └── models.py                # Reglamento
└── observaciones/
    └── models.py                # BancoObservaciones
                                 # ObservacionGenerada
```

---

## 1. MODELO USUARIO

**Archivo:** `/home/chapitec/Documents/chapitec/andre/T.A-Arquitectura-de-software/proyecto_untels/apps/usuarios/models.py`

**Líneas:** 28

### Código del Modelo

```python
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Usuario(models.Model):
    TIPO_CHOICES = [
        ('estudiante', 'Estudiante'),
        ('egresado', 'Egresado'),
        ('docente', 'Docente'),
    ]
    
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=200)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_CHOICES, default='estudiante')
    password = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    def set_password(self, raw_password):
        """Encripta y guarda la contraseña"""
        self.password = make_password(raw_password)
        self.save()
    
    def check_password(self, raw_password):
        """Verifica la contraseña (timing-safe)"""
        if not self.password:
            return False
        return check_password(raw_password, self.password)
```

### Estructura SQL Equivalente

```sql
CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    tipo_usuario VARCHAR(20) DEFAULT 'estudiante',
    password VARCHAR(255) NULL,
    
    CHECK (tipo_usuario IN ('estudiante', 'egresado', 'docente'))
);

CREATE UNIQUE INDEX idx_usuario_codigo ON usuario(codigo);
```

### Campos

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | AutoField | PK, auto-increment | ID único |
| `codigo` | CharField(20) | UNIQUE, NOT NULL | Código universitario |
| `nombre` | CharField(200) | NOT NULL | Nombre completo |
| `tipo_usuario` | CharField(20) | CHOICES | estudiante/egresado/docente |
| `password` | CharField(255) | NULL, BLANK | Contraseña encriptada |

### Métodos

#### set_password(raw_password)
```python
usuario = Usuario.objects.get(codigo='2021101234')
usuario.set_password('mi_password_123')
# Automáticamente encripta con PBKDF2/Bcrypt y guarda
```

#### check_password(raw_password)
```python
if usuario.check_password('mi_password_123'):
    print("Contraseña correcta")
else:
    print("Contraseña incorrecta")
```

**Algoritmo de encriptación:** PBKDF2_SHA256 (por defecto en Django)

### Ejemplo de Datos

| id | codigo | nombre | tipo_usuario | password |
|----|--------|--------|--------------|----------|
| 1 | 2021101234 | Juan Pérez | estudiante | pbkdf2_sha256$... |
| 2 | 2019103456 | María López | egresado | pbkdf2_sha256$... |
| 3 | DOC001 | Prof. García | docente | pbkdf2_sha256$... |

---

## 2. MODELO INFORME

**Archivo:** `/home/chapitec/Documents/chapitec/andre/T.A-Arquitectura-de-software/proyecto_untels/apps/informes/models.py`

**Líneas:** 29

### Código del Modelo

```python
from django.db import models
from apps.usuarios.models import Usuario

class Informe(models.Model):
    ESTADO_ENVIADO = 'enviado'
    ESTADO_EN_REVISION = 'en_revision'
    ESTADO_COMPLETADO = 'completado'

    ESTADO_CHOICES = [
        (ESTADO_ENVIADO, 'Enviado'),
        (ESTADO_EN_REVISION, 'En Revisión'),
        (ESTADO_COMPLETADO, 'Completado'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre_archivo = models.CharField(max_length=255)
    contenido = models.TextField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default=ESTADO_ENVIADO,
    )

    class Meta:
        db_table = 'informe'

    def __str__(self):
        return f"{self.nombre_archivo} [{self.get_estado_display()}]"
```

### Estructura SQL Equivalente

```sql
CREATE TABLE informe (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    nombre_archivo VARCHAR(255) NOT NULL,
    contenido TEXT NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'enviado',
    
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE,
    CHECK (estado IN ('enviado', 'en_revision', 'completado'))
);

CREATE INDEX idx_informe_usuario ON informe(usuario_id);
CREATE INDEX idx_informe_estado ON informe(estado);
CREATE INDEX idx_informe_fecha ON informe(fecha_registro DESC);
```

### Campos

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | AutoField | PK, auto-increment | ID único |
| `usuario` | ForeignKey | NOT NULL, CASCADE | Usuario que subió el informe |
| `nombre_archivo` | CharField(255) | NOT NULL | Nombre del archivo .docx |
| `contenido` | TextField | NOT NULL | Texto extraído del .docx |
| `fecha_registro` | DateTimeField | auto_now_add | Fecha de carga |
| `estado` | CharField(20) | CHOICES, DEFAULT='enviado' | Estado del proceso |

### Estados

```python
ENVIADO       → Informe recién subido
EN_REVISION   → IA está procesando
COMPLETADO    → Validación finalizada
```

### Relaciones

```
Usuario (1) ←──→ (N) Informe
Un usuario puede tener múltiples informes
```

### Ejemplo de Datos

| id | usuario_id | nombre_archivo | fecha_registro | estado |
|----|------------|----------------|----------------|--------|
| 1 | 1 | informe_practicas.docx | 2026-06-16 22:30 | completado |
| 2 | 1 | segundo_informe.docx | 2026-06-15 18:15 | en_revision |
| 3 | 2 | mi_informe.docx | 2026-06-14 10:00 | enviado |

### Métodos Útiles

```python
# Obtener todos los informes de un usuario
informes = Informe.objects.filter(usuario=usuario).order_by('-fecha_registro')

# Contar observaciones de un informe
num_obs = informe.observaciongenerada_set.count()

# Cambiar estado
informe.estado = Informe.ESTADO_COMPLETADO
informe.save()

# Obtener estado legible
print(informe.get_estado_display())  # "Completado"
```

---

## 3. MODELO REGLAMENTO

**Archivo:** `/home/chapitec/Documents/chapitec/andre/T.A-Arquitectura-de-software/proyecto_untels/apps/reglamento/models.py`

**Líneas:** 12

### Código del Modelo

```python
from django.db import models

class Reglamento(models.Model):
    nombre = models.CharField(max_length=255)
    contenido = models.TextField()
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'reglamento'

    def __str__(self):
        return self.nombre
```

### Estructura SQL Equivalente

```sql
CREATE TABLE reglamento (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    contenido TEXT NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_reglamento_activo ON reglamento(activo);
```

### Campos

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | AutoField | PK, auto-increment | ID único |
| `nombre` | CharField(255) | NOT NULL | Nombre del reglamento |
| `contenido` | TextField | NOT NULL | Texto completo del reglamento |
| `activo` | BooleanField | DEFAULT=True | Si está activo o no |

### Uso

```python
# Obtener reglamento activo
reglamento = Reglamento.objects.filter(activo=True).first()

# Crear nuevo reglamento
Reglamento.objects.create(
    nombre='Reglamento de Prácticas 2026',
    contenido='...',
    activo=True
)

# Desactivar reglamento anterior
reglamento_viejo.activo = False
reglamento_viejo.save()
```

### Ejemplo de Datos

| id | nombre | activo | contenido |
|----|--------|--------|-----------|
| 1 | Reglamento de Prácticas UNTELS 2026 | TRUE | El presente reglamento... |
| 2 | Reglamento de Prácticas UNTELS 2025 | FALSE | (versión anterior) |

---

## 4. MODELO BANCOOBSERVACIONES

**Archivo:** `/home/chapitec/Documents/chapitec/andre/T.A-Arquitectura-de-software/proyecto_untels/apps/observaciones/models.py`

**Líneas:** 12

### Código del Modelo

```python
from django.db import models

class BancoObservaciones(models.Model):
    seccion = models.CharField(max_length=100)
    descripcion = models.TextField()

    class Meta:
        db_table = 'banco_observaciones'

    def __str__(self):
        return f"{self.seccion}: {self.descripcion[:50]}"
```

### Estructura SQL Equivalente

```sql
CREATE TABLE banco_observaciones (
    id SERIAL PRIMARY KEY,
    seccion VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL
);

CREATE INDEX idx_banco_obs_seccion ON banco_observaciones(seccion);
```

### Campos

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | AutoField | PK, auto-increment | ID único |
| `seccion` | CharField(100) | NOT NULL | Sección del informe |
| `descripcion` | TextField | NOT NULL | Observación frecuente |

### Propósito

Almacenar **observaciones frecuentes** que los docentes han identificado en informes anteriores. La IA usa este banco como referencia para generar nuevas observaciones.

### Ejemplo de Datos

| id | seccion | descripcion |
|----|---------|-------------|
| 1 | Introducción | No presenta objetivo general |
| 2 | Introducción | Falta contexto de la empresa |
| 3 | Desarrollo | No menciona competencias adquiridas |
| 4 | Conclusiones | No se relaciona con los objetivos |
| 5 | Bibliografía | Formato APA incorrecto |

### Uso

```python
# Obtener todas las observaciones
observaciones = BancoObservaciones.objects.all()

# Filtrar por sección
obs_intro = BancoObservaciones.objects.filter(seccion='Introducción')

# Crear nueva observación frecuente
BancoObservaciones.objects.create(
    seccion='Anexos',
    descripcion='Faltan evidencias fotográficas'
)
```

---

## 5. MODELO OBSERVACIONGENERADA

**Archivo:** `/home/chapitec/Documents/chapitec/andre/T.A-Arquitectura-de-software/proyecto_untels/apps/observaciones/models.py`

**Líneas:** 24

### Código del Modelo

```python
from django.db import models
from apps.informes.models import Informe

class ObservacionGenerada(models.Model):
    informe = models.ForeignKey(Informe, on_delete=models.CASCADE)
    seccion = models.CharField(max_length=100)
    observacion = models.TextField()
    ubicacion_error = models.CharField(max_length=255)

    class Meta:
        db_table = 'observacion_generada'

    def __str__(self):
        return f"{self.informe.nombre_archivo} - {self.seccion}"
```

### Estructura SQL Equivalente

```sql
CREATE TABLE observacion_generada (
    id SERIAL PRIMARY KEY,
    informe_id INTEGER NOT NULL,
    seccion VARCHAR(100) NOT NULL,
    observacion TEXT NOT NULL,
    ubicacion_error VARCHAR(255) NOT NULL,
    
    FOREIGN KEY (informe_id) REFERENCES informe(id) ON DELETE CASCADE
);

CREATE INDEX idx_obs_gen_informe ON observacion_generada(informe_id);
CREATE INDEX idx_obs_gen_seccion ON observacion_generada(seccion);
```

### Campos

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | AutoField | PK, auto-increment | ID único |
| `informe` | ForeignKey | NOT NULL, CASCADE | Informe al que pertenece |
| `seccion` | CharField(100) | NOT NULL | Sección con error |
| `observacion` | TextField | NOT NULL | Descripción del problema |
| `ubicacion_error` | CharField(255) | NOT NULL | Ubicación específica |

### Relaciones

```
Informe (1) ←──→ (N) ObservacionGenerada
Un informe puede tener múltiples observaciones
```

### Ejemplo de Datos

| id | informe_id | seccion | observacion | ubicacion_error |
|----|------------|---------|-------------|-----------------|
| 1 | 1 | Introducción | Falta objetivo general | Introducción, párrafo 1 |
| 2 | 1 | Desarrollo | No menciona competencias | Capítulo 2 |
| 3 | 1 | Conclusiones | No relaciona con objetivos | Conclusiones |

### Uso

```python
# Crear observación (generada por la IA)
ObservacionGenerada.objects.create(
    informe=informe,
    seccion='Introducción',
    observacion='Falta objetivo general',
    ubicacion_error='Introducción, primer párrafo'
)

# Obtener todas las observaciones de un informe
observaciones = ObservacionGenerada.objects.filter(informe=informe)

# Contar observaciones
num_obs = informe.observaciongenerada_set.count()

# Agrupar por sección
from django.db.models import Count
obs_por_seccion = ObservacionGenerada.objects.values('seccion').annotate(
    total=Count('id')
)
```

---

## DIAGRAMA DE RELACIONES

```
┌─────────────────┐
│    Usuario      │
│─────────────────│
│ id (PK)         │
│ codigo (UNIQUE) │
│ nombre          │
│ tipo_usuario    │
│ password        │
└────────┬────────┘
         │ 1
         │
         │ N
┌────────▼────────┐
│    Informe      │
│─────────────────│
│ id (PK)         │
│ usuario_id (FK) │◄────────────┐
│ nombre_archivo  │             │
│ contenido       │             │
│ fecha_registro  │             │
│ estado          │             │
└────────┬────────┘             │
         │ 1                    │
         │                      │
         │ N                    │
┌────────▼─────────────────┐    │
│ ObservacionGenerada      │    │
│──────────────────────────│    │
│ id (PK)                  │    │
│ informe_id (FK)          │────┘
│ seccion                  │
│ observacion              │
│ ubicacion_error          │
└──────────────────────────┘


┌─────────────────────┐      ┌──────────────────────┐
│   Reglamento        │      │ BancoObservaciones   │
│─────────────────────│      │──────────────────────│
│ id (PK)             │      │ id (PK)              │
│ nombre              │      │ seccion              │
│ contenido           │      │ descripcion          │
│ activo              │      └──────────────────────┘
└─────────────────────┘
(No tiene relaciones)       (No tiene relaciones)
(Leído por servicios)       (Leído por IA)
```

---

## MIGRACIONES

Las migraciones están en:

```
apps/usuarios/migrations/
├── 0001_initial.py                          # Creación inicial
└── 0002_usuario_password_alter_usuario_...  # Agregar password + unique

apps/informes/migrations/
└── 0001_initial.py                          # Creación inicial

apps/reglamento/migrations/
└── 0001_initial.py                          # Creación inicial

apps/observaciones/migrations/
└── 0001_initial.py                          # Creación inicial
```

### Aplicar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## QUERIES COMUNES

### Obtener informes de un usuario con observaciones

```python
from apps.usuarios.models import Usuario
from apps.informes.models import Informe

usuario = Usuario.objects.get(codigo='2021101234')
informes = Informe.objects.filter(usuario=usuario).prefetch_related('observaciongenerada_set')

for informe in informes:
    print(f"{informe.nombre_archivo}: {informe.observaciongenerada_set.count()} observaciones")
```

### Obtener todos los informes con datos de usuario (evitar N+1)

```python
informes = Informe.objects.all().select_related('usuario').order_by('-fecha_registro')

for informe in informes:
    print(f"{informe.usuario.nombre} - {informe.nombre_archivo}")
```

### Contar informes por estado

```python
from django.db.models import Count

stats = Informe.objects.values('estado').annotate(total=Count('id'))
# [{'estado': 'completado', 'total': 10}, ...]
```

### Buscar observaciones por palabra clave

```python
observaciones = ObservacionGenerada.objects.filter(
    observacion__icontains='objetivo'
)
```

---

## ÍNDICES PARA OPTIMIZACIÓN

Django crea automáticamente índices para:
- Primary Keys (`id`)
- Foreign Keys (`usuario_id`, `informe_id`)
- Campos con `unique=True` (`codigo`)

**Índices recomendados adicionales (futuro):**

```python
class Informe(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['-fecha_registro']),  # Ordenamiento frecuente
            models.Index(fields=['estado']),           # Filtrado frecuente
        ]
```

---

## RESUMEN

| Modelo | Tabla | Campos | Relaciones | Propósito |
|--------|-------|--------|------------|-----------|
| Usuario | usuario | 5 | 1→N Informe | Datos de usuarios |
| Informe | informe | 6 | N→1 Usuario, 1→N Observación | Informes subidos |
| Reglamento | reglamento | 4 | Ninguna | Reglamento institucional |
| BancoObservaciones | banco_observaciones | 3 | Ninguna | Observaciones frecuentes |
| ObservacionGenerada | observacion_generada | 5 | N→1 Informe | Observaciones de IA |

**Total:** 5 modelos, 23 campos, 2 relaciones FK

---

**Esta es la CAPA DE DATOS completa.**

**Siguiente:** Lee `CAPA_INFRAESTRUCTURA.md` para entender deployment y configuración.
