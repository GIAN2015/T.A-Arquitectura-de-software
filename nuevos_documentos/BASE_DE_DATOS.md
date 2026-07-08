# 💾 Base de Datos - Sistema de Validación UNTELS

> Documentación del modelo de datos

## Motor de Base de Datos

- **Desarrollo**: SQLite 3
- **Producción**: PostgreSQL (recomendado)
- **ORM**: Django ORM

## Diagrama ER Simplificado

```
┌─────────────┐       ┌──────────────┐       ┌─────────────────────┐
│   Usuario   │──────<│   Informe    │>──────│  ObservacionGenerada│
└─────────────┘       └──────────────┘       └─────────────────────┘
      │                      │
      │                      │
      ▼                      ▼
┌─────────────┐       ┌────────────────────────┐
│   Escuela   │       │ BancoObservacionesDoc  │
└─────────────┘       └────────────────────────┘
```

## Tablas Principales

### 1. usuarios_usuario

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer PK | ID único |
| codigo | VARCHAR(20) UNIQUE | Código de usuario |
| nombre | VARCHAR(200) | Nombre completo |
| tipo_usuario | VARCHAR(20) | estudiante/docente/presidente/secretaria/admin |
| password | VARCHAR(255) | Contraseña (sin hash en dev) |
| email | VARCHAR(254) | Email opcional |
| escuela_id | FK | Relación con escuela |
| activo | Boolean | Usuario activo |

### 2. informes_informe

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer PK | ID único |
| usuario_id | FK | Estudiante que envió |
| nombre_archivo | VARCHAR(255) | Nombre del archivo |
| archivo | FileField | Ruta del PDF/DOCX |
| contenido | Text | Texto extraído |
| estado | VARCHAR(50) | Estado actual (11 estados) |
| version | Integer | Versión del informe |
| secretaria_asignada_id | FK | Secretaria |
| presidente_asignado_id | FK | Presidente |
| docente_revisor_id | FK | Docente |
| escuela_id | FK | Escuela |
| comentario_docente | Text | Dictamen estructurado |
| comentario_presidente | Text | Comentario presidente |
| banco_observaciones_usado_id | FK | Banco usado |
| informe_anterior_id | FK | Versión anterior |
| fecha_registro | DateTime | Fecha de creación |
| fecha_completado | DateTime | Fecha de finalización |

**Estados posibles** (11):
1. enviado
2. pendiente_secretaria
3. pendiente_presidente
4. pendiente_docente
5. validando_ia
6. revision_docente
7. pendiente_aprobacion_presidente
8. aprobado_presidente
9. rechazado_presidente
10. aprobado_final
11. rechazado_estudiante

**Interpretación operativa de estados finales**:
- `aprobado_presidente`: El presidente aprobó el informe y secretaría aún debe notificar
- `rechazado_presidente`: El presidente rechazó el informe final y secretaría aún debe notificar al estudiante
- `rechazado_estudiante`: El estudiante ya fue notificado y debe corregir
- `revision_docente` con `comentario_presidente`: El presidente devolvió el dictamen al docente para rehacer la revisión

**Versionado de reenvíos**:
- Cada reenvío crea un nuevo registro `Informe`
- `informe_anterior_id` apunta a la versión rechazada previa
- Una versión rechazada que ya tiene `versiones_posteriores` queda cerrada y no debe volver a reenviarse

### 3. observaciones_observaciongenerada

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer PK | ID único |
| informe_id | FK | Informe relacionado |
| seccion | VARCHAR(100) | Sección del informe |
| observacion | Text | Texto de la observación |
| ubicacion_error | VARCHAR(255) | Ubicación |
| severidad | VARCHAR(20) | critica/importante/menor/sugerencia |
| estado | VARCHAR(20) | pendiente/confirmada/descartada/corregida |
| comentario_docente | Text | Comentario adicional |
| fecha_revision | DateTime | Fecha de revisión |

### 4. observaciones_bancoobservacionesdocente

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer PK | ID único |
| docente_id | FK | Docente propietario |
| nombre | VARCHAR(200) | Nombre del banco |
| archivo | FileField | PDF/DOCX del banco |
| contenido_extraido | Text | Texto extraído |
| activo | Boolean | Banco activo |
| fecha_creacion | DateTime | Fecha de creación |

### 5. escuelas_escuela

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer PK | ID único |
| codigo | VARCHAR(10) UNIQUE | Código escuela |
| nombre | VARCHAR(200) | Nombre escuela |
| presidente_id | FK | Usuario presidente |
| activo | Boolean | Escuela activa |

### 6. notificaciones_notificacion

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer PK | ID único |
| usuario_id | FK | Destinatario |
| informe_id | FK | Informe relacionado |
| tipo | VARCHAR(50) | Tipo de notificación |
| titulo | VARCHAR(200) | Título |
| mensaje | Text | Mensaje completo |
| leida | Boolean | Estado de lectura |
| fecha_creacion | DateTime | Fecha de creación |
| fecha_leida | DateTime | Fecha de lectura |

## Relaciones

### Usuario → Informe

```
Usuario (1) ─────< Informe (N)
  • informes_enviados (estudiante)
  • informes_derivados (secretaria)
  • informes_presidente (presidente)
  • informes_revisor (docente)
```

### Informe → ObservacionGenerada

```
Informe (1) ─────< ObservacionGenerada (N)
  • observaciones
```

### Informe → Informe (Versionado)

```
Informe (1) ─────< Informe (N)
  • informe_anterior → versiones_posteriores
```

## Índices

```sql
CREATE INDEX idx_informe_estado ON informes_informe(estado);
CREATE INDEX idx_informe_usuario ON informes_informe(usuario_id);
CREATE INDEX idx_informe_docente ON informes_informe(docente_revisor_id);
CREATE INDEX idx_observacion_estado ON observaciones_observaciongenerada(estado);
CREATE INDEX idx_notificacion_usuario_leida ON notificaciones_notificacion(usuario_id, leida);
```

## Migraciones

```bash
# Crear migración
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Ver SQL
python manage.py sqlmigrate informes 0001
```

## Datos Iniciales

Ver `backend/fixtures/initial_data.json`

---

**Ver también**: [Backend](BACKEND.md), [Patrones](PATRONES.md)
