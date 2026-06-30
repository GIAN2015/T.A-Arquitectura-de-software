# GUÍA DE USO POR ROL - v2.0

**Sistema de Validación de Informes de Prácticas Preprofesionales - UNTELS**

**Versión:** 2.0 - Flujo Completo Multi-Rol  
**Fecha:** 29 de Junio de 2026

---

## ÍNDICE POR ROL

1. [Estudiante / Egresado](#estudiante--egresado)
2. [Secretaria Académica](#secretaria-académica)
3. [Presidente de Escuela](#presidente-de-escuela)
4. [Docente Revisor](#docente-revisor)
5. [Flujo Completo del Sistema](#flujo-completo-del-sistema)

---

## ESTUDIANTE / EGRESADO

### 1. Iniciar Sesión

**URL:** `/` o `/login/`

**Credenciales:**
- Código de estudiante
- Contraseña

### 2. Enviar Informe

**Pasos:**
1. Ir a "Subir Informe" (`/upload/`)
2. Seleccionar archivo PDF o DOCX
3. Hacer clic en "Validar Informe"
4. Esperar procesamiento

**Resultado:**
- El informe queda en estado `ENVIADO`
- La secretaria recibe notificación automática

### 3. Ver Estado del Informe

**URL:** `/historial/`

**Qué ver:**
- Lista de todos tus informes
- Estado actual de cada uno
- Observaciones (si las hay)
- Resultado final

**Estados posibles:**
- `Enviado` - Enviado, esperando secretaría
- `Pendiente - Secretaría` - En proceso de derivación
- `Pendiente - Presidente` - Asignado a tu escuela
- `Pendiente - Docente` - Asignado a docente revisor
- `En Revisión` - Docente está revisando
- `APROBADO` - Tu informe fue aprobado ✅
- `Rechazado` - Debes corregir y reenviar ❌

### 4. Si tu Informe es Rechazado

**Pasos:**
1. Ver las observaciones en el historial
2. Corregir tu informe según las observaciones
3. Volver a enviar el informe corregido (paso 2)

**Nota:** El sistema crea una nueva versión automáticamente

### 5. Si tu Informe es Aprobado

**Resultado:**
- Recibes notificación de aprobación
- El proceso está completado
- Puedes descargar el resultado (cuando templates estén listos)

---

## SECRETARIA ACADÉMICA

### 1. Iniciar Sesión

**URL:** `/secretaria/login/`

**Credenciales:**
- Código de secretaria
- Contraseña

### 2. Dashboard

**URL:** `/secretaria/dashboard/`

**Qué ver:**
- Informes pendientes de derivar
- Informes en proceso (derivados a presidentes)
- Informes aprobados pendientes de notificar
- Estadísticas generales
- Notificaciones

### 3. Derivar Informe a Presidente

**Pasos:**
1. En el dashboard, ver lista de "Informes Pendientes"
2. Hacer clic en "Derivar" junto al informe
3. Seleccionar la escuela correspondiente al estudiante
4. (Opcional) Agregar comentario
5. Hacer clic en "Derivar a Presidente"

**Resultado:**
- El informe cambia a estado `PENDIENTE_PRESIDENTE`
- El presidente de esa escuela recibe notificación

**Validaciones:**
- Solo se puede derivar a escuelas con presidente asignado
- El informe debe estar en estado correcto

### 4. Notificar Estudiante (Aprobación Final)

**Cuándo:** Cuando un presidente aprueba un informe

**Pasos:**
1. En dashboard, ver "Informes Aprobados Pendientes de Notificar"
2. Hacer clic en "Notificar Estudiante"
3. Confirmar la acción
4. El estudiante recibe notificación automática

**Resultado:**
- Estado cambia a `APROBADO_FINAL`
- Proceso completo
- Estudiante notificado

### 5. Ver Detalles de un Informe

**URL:** `/secretaria/ver/<informe_id>/`

**Qué ver:**
- Datos del estudiante
- Escuela asignada
- Presidente asignado
- Docente revisor (si ya fue asignado)
- Estado actual
- Observaciones (si las hay)
- Comentarios de cada rol

### 6. Gestionar Notificaciones

**URL:** `/secretaria/notificaciones/`

**Qué hacer:**
- Ver todas las notificaciones
- Marcar como leídas
- Ver detalles del informe relacionado

---

## PRESIDENTE DE ESCUELA

### 1. Iniciar Sesión

**URL:** `/presidente/login/`

**Credenciales:**
- Código de presidente
- Contraseña

**Nota:** Debes tener una escuela asignada

### 2. Dashboard

**URL:** `/presidente/dashboard/`

**Qué ver:**
- Informes pendientes de asignar docente
- Informes en revisión (por docentes)
- Informes pendientes de tu aprobación
- Estadísticas de tu escuela
- Notificaciones

### 3. Designar Docente Revisor

**Cuándo:** Cuando secretaria deriva un informe a tu escuela

**Pasos:**
1. En dashboard, ver "Informes Pendientes de Asignar"
2. Hacer clic en "Designar Docente"
3. Seleccionar un docente de tu escuela
4. Confirmar asignación

**Resultado:**
- Estado cambia a `PENDIENTE_DOCENTE`
- Docente recibe notificación automática

**Validaciones:**
- Solo puedes asignar docentes de tu escuela
- El docente debe estar activo

### 4. Revisar Dictamen del Docente

**Cuándo:** Cuando un docente completa su revisión y envía dictamen

**URL:** `/presidente/revisar/<informe_id>/`

**Qué ver:**
- Informe del estudiante
- Dictamen del docente
- Observaciones confirmadas
- Observaciones descartadas
- Recomendación del docente

**Pasos:**
1. Leer el dictamen completo
2. Revisar las observaciones
3. Decidir: APROBAR o RECHAZAR

#### 4a. Si APRUEBAS

**Pasos:**
1. (Opcional) Agregar comentario
2. Hacer clic en "Aprobar Dictamen"
3. Confirmar

**Resultado:**
- Estado cambia a `APROBADO_PRESIDENTE`
- Secretaria recibe notificación
- Secretaria notificará al estudiante

#### 4b. Si RECHAZAS

**Cuándo rechazar:**
- El dictamen es insuficiente
- Falta información
- Necesita más revisión

**Pasos:**
1. Escribir motivo del rechazo (OBLIGATORIO, mínimo 10 caracteres)
2. Hacer clic en "Rechazar Dictamen"
3. Confirmar

**Resultado:**
- Estado cambia a `RECHAZADO_PRESIDENTE`
- Docente recibe notificación con el motivo
- Docente debe revisar nuevamente

### 5. Ver Historial de la Escuela

**URL:** `/presidente/historial/`

**Qué ver:**
- Todos los informes de tu escuela
- Estados actuales
- Docentes asignados
- Resultados finales

### 6. Gestionar Notificaciones

**URL:** `/presidente/notificaciones/`

**Tipos de notificaciones que recibes:**
- Informe asignado a tu escuela (por secretaria)
- Docente completó revisión (dictamen listo)

---

## DOCENTE REVISOR

### 1. Iniciar Sesión

**URL:** `/docente/login/`

**Credenciales:**
- Código de docente
- Contraseña

### 2. Dashboard

**URL:** `/panel-docente/`

**Qué ver:**
- Informes asignados a ti (pendientes de revisar)
- Informes revisados (enviados a presidente)
- Tu banco de observaciones activo
- Estadísticas de tu trabajo
- Notificaciones

### 3. Gestionar tu Banco de Observaciones

**URL:** `/docente/banco/`

**¿Qué es?**
Un banco de observaciones es tu conjunto personalizado de criterios y observaciones que usarás para revisar informes.

#### 3a. Crear un Banco Nuevo

**Pasos:**
1. Ir a "Banco de Observaciones"
2. Hacer clic en "Crear Nuevo Banco"
3. Dar un nombre descriptivo (ej: "Observaciones 2026-1")
4. Subir archivo PDF o DOCX con tus observaciones
5. Hacer clic en "Crear"

**Resultado:**
- El sistema extrae el contenido del archivo
- El banco queda ACTIVO automáticamente
- Los demás bancos se desactivan

**Validaciones:**
- Archivo debe ser PDF o DOCX
- Contenido mínimo 50 caracteres
- Nombre único (no puedes tener dos bancos con el mismo nombre)

#### 3b. Activar un Banco Existente

**Pasos:**
1. Ver lista de tus bancos
2. Hacer clic en "Activar" junto al banco deseado

**Resultado:**
- Ese banco se vuelve activo
- Los demás se desactivan
- Solo puedes tener 1 banco activo a la vez

#### 3c. Eliminar un Banco

**Pasos:**
1. Hacer clic en "Eliminar" junto al banco
2. Confirmar

**Validaciones:**
- No puedes eliminar tu único banco activo
- Debes tener al menos un banco

### 4. Revisar Informe con IA

**Cuándo:** Cuando el presidente te asigna un informe

**URL:** `/docente/revisar/<informe_id>/`

**Pasos:**

#### Paso 1: Validación con IA (Automática)

**Qué pasa:**
1. El sistema verifica que tengas un banco activo
2. Si no tienes, te redirige a crear uno
3. Si tienes banco, el sistema valida el informe automáticamente
4. Usa TU banco de observaciones (no el global)
5. La IA genera observaciones basadas en tu banco
6. Las observaciones aparecen en una tabla editable

#### Paso 2: Revisar y Editar Observaciones

**Qué ver:**
- Tabla con todas las observaciones generadas por IA
- Columnas: Sección, Observación, Ubicación, Severidad, Acción

**Para cada observación puedes:**
- **Confirmar:** Esta observación es válida
- **Descartar:** Esta observación no aplica
- **Cambiar Severidad:** Crítica, Importante, Menor, Sugerencia
- **Agregar Comentario:** Explicación adicional

**Pasos:**
1. Leer cada observación
2. Seleccionar acción: Confirmar o Descartar
3. (Opcional) Cambiar severidad
4. (Opcional) Agregar comentario
5. Hacer clic en "Actualizar Observaciones"

#### Paso 3: Generar Dictamen

**Qué es el dictamen:**
Tu informe final con tu recomendación (aprobar o rechazar)

**Pasos:**
1. En la misma página, ir a "Dictamen Final"
2. Escribir tu dictamen (mínimo 20 caracteres)
3. Seleccionar recomendación:
   - ☑ Recomendar APROBAR
   - ☐ Recomendar RECHAZAR
4. Hacer clic en "Enviar Dictamen a Presidente"

**Resultado:**
- Estado cambia a `PENDIENTE_APROBACION_PRESIDENTE`
- Presidente recibe notificación
- Presidente revisará tu dictamen

### 5. Si el Presidente Rechaza tu Dictamen

**Qué pasa:**
- Recibes notificación con el motivo
- El informe vuelve a estado `RECHAZADO_PRESIDENTE`
- Debes revisar nuevamente

**Pasos:**
1. Leer el motivo del rechazo
2. Volver a revisar el informe
3. Ajustar observaciones
4. Generar nuevo dictamen
5. Reenviar

### 6. Ver Historial de tus Revisiones

**URL:** `/docente/historial/`

**Qué ver:**
- Todos los informes asignados a ti
- Estados actuales
- Resultados finales

### 7. Gestionar Notificaciones

**URL:** `/docente/notificaciones/`

**Tipos de notificaciones que recibes:**
- Informe asignado (por presidente)
- Dictamen rechazado (por presidente)

---

## FLUJO COMPLETO DEL SISTEMA

### Diagrama Visual

```
┌────────────┐
│ ESTUDIANTE │ (1) Envía informe PDF/DOCX
└─────┬──────┘
      │
      ↓ Notificación automática
┌────────────┐
│ SECRETARIA │ (2) Deriva a Presidente de Escuela
└─────┬──────┘
      │
      ↓ Notificación automática
┌────────────┐
│ PRESIDENTE │ (3) Designa Docente revisor
└─────┬──────┘
      │
      ↓ Notificación automática
┌────────────┐
│   DOCENTE  │ (4) Gestiona su banco
│            │ (5) Valida con IA usando su banco
│            │ (6) Edita observaciones
│            │ (7) Genera dictamen
│            │ (8) Envía a Presidente
└─────┬──────┘
      │
      ↓ Notificación automática
┌────────────┐
│ PRESIDENTE │ (9) Revisa dictamen
│            │
│ ┌──────────┴──────────┐
│ │ APRUEBA   RECHAZA   │
│ └──────────┬──────────┘
└────────────┤
      │      │
      │      └──→ Vuelve a Docente (paso 4)
      │
      ↓ Notificación automática
┌────────────┐
│ SECRETARIA │ (10) Notifica al Estudiante
└─────┬──────┘
      │
      ↓ Notificación automática
┌────────────┐
│ ESTUDIANTE │ (11) Recibe resultado
└────────────┘
```

### Tiempo Estimado por Etapa

| Etapa | Responsable | Tiempo Estimado |
|-------|-------------|-----------------|
| 1. Envío | Estudiante | 5 minutos |
| 2. Derivación | Secretaria | 5 minutos |
| 3. Designación | Presidente | 5 minutos |
| 4-8. Revisión completa | Docente | 1-3 horas |
| 9. Aprobación | Presidente | 15-30 minutos |
| 10. Notificación | Secretaria | 5 minutos |
| **TOTAL** | | **2-4 horas** |

### Estados del Informe

| # | Estado | Descripción |
|---|--------|-------------|
| 1 | `enviado` | Estudiante envió |
| 2 | `pendiente_secretaria` | En bandeja de secretaria |
| 3 | `pendiente_presidente` | Asignado a presidente de escuela |
| 4 | `pendiente_docente` | Asignado a docente |
| 5 | `validando_ia` | IA procesando con banco del docente |
| 6 | `revision_docente` | Docente editando observaciones |
| 7 | `pendiente_aprobacion_presidente` | Dictamen enviado, esperando presidente |
| 8 | `aprobado_presidente` | Presidente aprobó |
| 9 | `rechazado_presidente` | Presidente rechazó (vuelve a docente) |
| 10 | `aprobado_final` | APROBADO - Proceso completo ✅ |
| 11 | `rechazado_estudiante` | Rechazado - Estudiante debe corregir ❌ |

---

## PREGUNTAS FRECUENTES

### General

**P: ¿Puedo ver informes de otras escuelas?**  
R: No. Presidente y docentes solo ven informes de su escuela asignada.

**P: ¿Las notificaciones son automáticas?**  
R: Sí. El sistema envía notificaciones automáticas en cada transición.

**P: ¿Puedo cambiar mi escuela?**  
R: No. Solo un administrador puede cambiar asignaciones de escuelas.

### Para Docentes

**P: ¿Qué pasa si no tengo banco de observaciones?**  
R: No puedes revisar informes. Debes crear uno primero.

**P: ¿Puedo tener varios bancos activos?**  
R: No. Solo un banco puede estar activo a la vez.

**P: ¿Qué formato debe tener mi banco de observaciones?**  
R: PDF o DOCX. El sistema extrae el texto automáticamente.

**P: ¿La IA usa mi banco o el global?**  
R: Usa TU banco personalizado, no el global.

**P: ¿Puedo editar las observaciones de la IA?**  
R: Sí. Puedes confirmar, descartar, cambiar severidad y agregar comentarios.

### Para Presidentes

**P: ¿Qué hago si rechazo un dictamen?**  
R: El docente recibirá tu motivo y revisará nuevamente.

**P: ¿Puedo asignar docentes de otras escuelas?**  
R: No. Solo puedes asignar docentes de tu escuela.

**P: ¿Debo dar un motivo al rechazar?**  
R: Sí. Es obligatorio (mínimo 10 caracteres).

### Para Secretarias

**P: ¿Qué hago si una escuela no tiene presidente?**  
R: No puedes derivar a esa escuela. Contacta al administrador.

**P: ¿Puedo cambiar la escuela de un informe ya derivado?**  
R: No. Solo puedes derivar informes en estado `pendiente_secretaria`.

---

## CONTACTO Y SOPORTE

**Administrador del Sistema:**
- Para asignación de escuelas
- Para creación de usuarios
- Para problemas técnicos

**Documentación Completa:**
- `docs/PLAN_IMPLEMENTACION_FLUJO_COMPLETO.md` - Plan detallado
- `docs/PROGRESO_IMPLEMENTACION.md` - Estado actual
- `docs/RESUMEN_EJECUTIVO_V2.md` - Resumen ejecutivo

---

**Sistema desarrollado para UNTELS**  
**Versión:** 2.0 - Flujo Completo Multi-Rol  
**Fecha:** 29 de Junio de 2026
