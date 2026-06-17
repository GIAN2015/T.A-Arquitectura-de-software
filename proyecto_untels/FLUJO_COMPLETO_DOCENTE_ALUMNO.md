# Flujo Completo: Docente ↔ Alumno ↔ IA

## 📋 Descripción General

Este sistema implementa un **flujo completo de revisión de informes** que integra:
- ✅ Validación automática con **IA** (Gemini)
- ✅ Revisión y decisión del **Docente**
- ✅ Feedback bidireccional **Docente ↔ Alumno**
- ✅ Sistema de **versionado** (reenvío de informes corregidos)
- ✅ Estados bien definidos para cada fase del proceso

---

## 🔄 Flujo del Sistema (Diagrama)

```
┌─────────────┐
│   ALUMNO    │
│ Sube .docx  │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│ Estado: ENVIADO     │
│ Sistema recibe file │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Estado: VALIDANDO   │
│ IA procesa informe  │
│ con Gemini + Regla  │
└──────┬──────────────┘
       │
       ▼
  ¿Hay observaciones?
       │
       ├── SÍ ─────────────────────┐
       │                           │
       ▼                           ▼
┌──────────────────┐      ┌────────────────────┐
│ Estado: OBSERVADO│      │ Estado: COMPLETADO │
│ Esperando docente│      │ Sin observaciones  │
└──────┬───────────┘      └────────────────────┘
       │
       ▼
┌───────────────────────┐
│ DOCENTE revisa        │
│ - Confirma/descarta   │
│ - Comenta cada obs    │
│ - Cambia severidad    │
│ - Escribe feedback    │
└──────┬────────────────┘
       │
       ▼
  ¿Decisión Docente?
       │
       ├── APROBAR ────────────────┐
       │                           │
       ├── RECHAZAR                ▼
       │      │              ┌────────────────┐
       │      │              │ Estado: APROBAD│
       │      │              │ ¡Felicitaciones│
       │      ▼              └────────────────┘
       │  ┌──────────────────┐
       │  │ Estado: RECHAZADO│
       │  │ Requiere corrección
       │  └──────┬───────────┘
       │         │
       │         ▼
       │  ┌─────────────────────┐
       │  │ ALUMNO ve feedback  │
       │  │ - Observaciones     │
       │  │ - Comentarios       │
       │  │ - Severidades       │
       │  └──────┬──────────────┘
       │         │
       │         ▼
       │  ┌─────────────────────┐
       │  │ ALUMNO corrige      │
       │  │ y REENVÍA (v2, v3..)│
       │  └──────┬──────────────┘
       │         │
       └─────────┴─── VUELVE AL INICIO
```

---

## 🎯 Estados del Informe

| Estado | Descripción | Quién lo ve | Acciones Disponibles |
|--------|-------------|-------------|----------------------|
| **ENVIADO** | Alumno subió el archivo | Sistema | Iniciar validación |
| **VALIDANDO** | IA está procesando | Sistema | Generar observaciones |
| **OBSERVADO** | IA terminó, hay observaciones | Docente | Revisar observaciones |
| **REVISION_DOCENTE** | Docente está revisando | Docente | Aprobar/Rechazar |
| **RECHAZADO** | Docente rechazó, requiere corrección | Alumno | Reenviar corregido |
| **APROBADO** | Docente aprobó el informe | Alumno | Ver certificado |
| **COMPLETADO** | Sin observaciones o proceso finalizado | Todos | Ninguna |

---

## 🎯 Estados de Observación

Cada observación generada por la IA tiene su propio estado:

| Estado | Descripción | Color |
|--------|-------------|-------|
| **PENDIENTE** | IA la generó, esperando revisión docente | Amarillo ⏳ |
| **CONFIRMADA** | Docente confirma que es válida | Rojo ✓ |
| **DESCARTADA** | Docente dice que no aplica | Gris ✗ |
| **CORREGIDA** | Alumno la corrigió en nueva versión | Verde ✅ |

---

## 🎯 Severidades de Observación

El docente puede ajustar la severidad de cada observación:

| Severidad | Descripción | Badge |
|-----------|-------------|-------|
| **CRÍTICA** | Debe corregirse obligatoriamente | 🔴 Rojo |
| **IMPORTANTE** | Debe corregirse | 🟡 Amarillo |
| **MENOR** | Recomendada | 🔵 Azul |
| **SUGERENCIA** | Opcional, mejora | 💡 Gris |

---

## 📝 Proceso Paso a Paso

### 1️⃣ Alumno Sube Informe

**Vista:** `upload_view` (`/upload/`)

```python
# Lo que sucede:
1. Alumno selecciona archivo .docx
2. Sistema lee el contenido
3. Verifica si hay informe previo rechazado (versionado)
4. Crea Informe con estado ENVIADO
5. Cambia estado a VALIDANDO
6. Llama a la IA (Gemini)
```

**Campos guardados:**
- `usuario`: ForeignKey al alumno
- `nombre_archivo`: "mi_informe.docx"
- `contenido`: Texto extraído del .docx
- `estado`: ENVIADO → VALIDANDO
- `version`: 1 (o 2, 3, 4... si es reenvío)
- `informe_anterior`: Link al informe v1 (si es v2)

---

### 2️⃣ IA Valida el Informe

**Servicio:** `validar_informe()` en `apps/informes/services.py`

```python
# Lo que hace la IA:
1. Lee el reglamento activo
2. Lee el banco de observaciones
3. Envía todo a Gemini con prompt específico
4. Gemini devuelve JSON con observaciones:
   {
     "seccion": "Portada",
     "observacion": "Falta el logo de UNTELS",
     "ubicacion": "Página 1"
   }
```

**Observaciones creadas:**
```python
ObservacionGenerada.objects.create(
    informe=informe,
    seccion="Portada",
    observacion="Falta el logo de UNTELS",
    ubicacion_error="Página 1",
    estado=ESTADO_PENDIENTE,  # ← Pendiente revisión docente
    severidad=SEVERIDAD_IMPORTANTE  # ← Por defecto
)
```

**Estado del informe:**
- Si hay observaciones → **OBSERVADO**
- Si NO hay observaciones → **COMPLETADO**

---

### 3️⃣ Docente Revisa el Informe

**Vista:** `admin_revisar_informe` (`/docente/revisar/<id>/`)

**Lo que ve el docente:**

```
┌──────────────────────────────────────┐
│ REVISAR INFORME: mi_informe.docx    │
├──────────────────────────────────────┤
│ Estudiante: Juan Pérez               │
│ Código: 2021010101                   │
│ Total Observaciones: 5               │
│   ├── Críticas: 1                    │
│   ├── Importantes: 2                 │
│   ├── Menores: 1                     │
│   └── Sugerencias: 1                 │
└──────────────────────────────────────┘

🔴 OBSERVACIONES CRÍTICAS (1)

┌──────────────────────────────────────┐
│ Sección: Portada                     │
│ Observación IA:                      │
│ "Falta el logo de UNTELS"            │
│                                      │
│ Acción: [✓ Confirmar] [✗ Descartar] │
│ Severidad: [Crítica ▼]               │
│ Comentario: [Agregar logo en...]    │
└──────────────────────────────────────┘

💬 COMENTARIO GENERAL:
┌──────────────────────────────────────┐
│ Escribe aquí feedback para el alumno│
│ ...                                  │
└──────────────────────────────────────┘

⚖️ DECISIÓN FINAL:
[✓ APROBAR] [✗ RECHAZAR PARA CORRECCIÓN]
```

**Lo que hace el docente:**

Para cada observación:
1. ✓ **Confirmar** o ✗ **Descartar**
2. Ajustar **severidad** (crítica, importante, menor, sugerencia)
3. Agregar **comentario adicional** (opcional)

Al final:
4. Escribir **comentario general** para el alumno
5. Decidir: **APROBAR** o **RECHAZAR**

---

### 4️⃣ Sistema Procesa la Decisión

**Código en `admin_revisar_informe`:**

```python
# Para cada observación:
for obs in observaciones:
    accion = request.POST.get(f'obs_accion_{obs.id}')
    
    if accion == 'confirmar':
        obs.estado = ESTADO_CONFIRMADA  # ✓
    elif accion == 'descartar':
        obs.estado = ESTADO_DESCARTADA  # ✗
    
    obs.comentario_docente = request.POST.get(f'obs_comentario_{obs.id}')
    obs.severidad = request.POST.get(f'obs_severidad_{obs.id}')
    obs.fecha_revision = timezone.now()
    obs.save()

# Para el informe:
informe.docente_revisor = docente
informe.comentario_docente = comentario_general
informe.fecha_revision_docente = timezone.now()

if accion == 'aprobar':
    informe.estado = ESTADO_APROBADO
elif accion == 'rechazar':
    informe.estado = ESTADO_RECHAZADO

informe.save()
```

---

### 5️⃣ Alumno Ve el Resultado

**Vista:** `validation_result` (`/resultado/<id>/`)

**Si fue APROBADO:**
```
✅ ¡Informe Aprobado!
Tu informe ha sido revisado y aprobado por el docente Juan Pérez.
Fecha de aprobación: 16/06/2026 14:30
```

**Si fue RECHAZADO:**
```
❌ Informe Rechazado - Requiere Correcciones
El docente Juan Pérez ha revisado tu informe y requiere que corrijas 
las observaciones marcadas.
Fecha de revisión: 16/06/2026 14:30

💬 COMENTARIO DEL DOCENTE:
─────────────────────────────────────
Hola Juan, tu informe tiene buena estructura pero debes corregir:
1. Agregar el logo de UNTELS en la portada
2. Ampliar el marco teórico con más referencias
3. Revisar la bibliografía (formato APA incorrecto)

Por favor, corrige estos puntos y reenvía tu informe.

📝 OBSERVACIONES CONFIRMADAS:

🔴 CRÍTICAS (1)
┌──────────────────────────────────────┐
│ Sección: Portada                     │
│ ✓ Confirmada por Docente             │
│                                      │
│ Observación:                         │
│ "Falta el logo de UNTELS"            │
│                                      │
│ 💬 Comentario del Docente:           │
│ "Agregar logo oficial en esquina     │
│  superior derecha, tamaño 3x3 cm"    │
└──────────────────────────────────────┘

[📤 REENVIAR INFORME CORREGIDO]
```

---

### 6️⃣ Alumno Reenvía Informe Corregido

**Proceso:**
1. Alumno corrige su informe .docx
2. Va a `/upload/`
3. Sube el archivo corregido
4. **Sistema detecta** que tiene un informe rechazado previo
5. Crea **nueva versión**:
   ```python
   version = informe_previo.version + 1  # v2, v3, v4...
   informe_anterior = informe_previo      # Link a v1
   ```
6. **Vuelve al inicio** del flujo (IA valida → Docente revisa → ...)

---

## 📊 Modelo de Datos

### Modelo `Informe`

```python
class Informe(models.Model):
    # Básico
    usuario = ForeignKey(Usuario)
    nombre_archivo = CharField(max_length=255)
    contenido = TextField()
    fecha_registro = DateTimeField(auto_now_add=True)
    
    # Estado y flujo
    estado = CharField(choices=ESTADO_CHOICES, default=ENVIADO)
    
    # Revisión docente (NUEVO)
    docente_revisor = ForeignKey(Usuario, null=True, related_name='informes_revisados')
    comentario_docente = TextField(null=True, blank=True)
    fecha_revision_docente = DateTimeField(null=True, blank=True)
    
    # Versionado (NUEVO)
    version = IntegerField(default=1)
    informe_anterior = ForeignKey('self', null=True, blank=True)
```

### Modelo `ObservacionGenerada`

```python
class ObservacionGenerada(models.Model):
    # Básico
    informe = ForeignKey(Informe, related_name='observaciones')
    seccion = CharField(max_length=100)
    observacion = TextField()
    ubicacion_error = CharField(max_length=255)
    
    # Estado de revisión (NUEVO)
    estado = CharField(choices=[
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada por Docente'),
        ('descartada', 'Descartada'),
        ('corregida', 'Corregida por Alumno')
    ], default='pendiente')
    
    # Feedback docente (NUEVO)
    comentario_docente = TextField(null=True, blank=True)
    fecha_revision = DateTimeField(null=True, blank=True)
    
    # Severidad (NUEVO)
    severidad = CharField(choices=[
        ('critica', 'Crítica'),
        ('importante', 'Importante'),
        ('menor', 'Menor'),
        ('sugerencia', 'Sugerencia')
    ], default='importante')
```

---

## 🖥️ Vistas Principales

| Vista | URL | Rol | Descripción |
|-------|-----|-----|-------------|
| `upload_view` | `/upload/` | Alumno | Subir informe (v1, v2, v3...) |
| `validation_result` | `/resultado/<id>/` | Alumno | Ver resultado + feedback docente |
| `historial_view` | `/historial/` | Alumno | Ver todas las versiones |
| `panel_docente_view` | `/panel-docente/` | Docente | Lista de todos los informes |
| `admin_revisar_informe` | `/docente/revisar/<id>/` | Docente | Revisar y decidir sobre informe |

---

## 🎨 Templates Creados/Actualizados

```
templates/
├── validation_result.html          # ← ACTUALIZADO: Muestra feedback docente
├── panel_docente.html              # ← ACTUALIZADO: Botón "Revisar"
└── admin/
    └── revisar_informe.html        # ← NUEVO: Interfaz revisión docente
```

---

## 🔄 Flujo de Versionado

```
Versión 1 (Original)
├── Estado: RECHAZADO
├── Observaciones: 5
└── Comentario: "Corregir logo y bibliografía"

        ↓ Alumno reenvía corregido

Versión 2 (Primera corrección)
├── Estado: OBSERVADO
├── Observaciones: 2 (solo bibliografía)
├── informe_anterior → v1
└── Comentario: "Mejor, pero falta formato APA"

        ↓ Alumno reenvía nuevamente

Versión 3 (Segunda corrección)
├── Estado: APROBADO ✅
├── Observaciones: 0
├── informe_anterior → v2
└── Comentario: "¡Excelente trabajo!"
```

---

## ✅ Casos de Uso Completos

### Caso 1: Informe Aprobado a la Primera

```
Alumno sube → IA valida → 0 observaciones → COMPLETADO ✅
```

### Caso 2: Informe con Observaciones Menores

```
Alumno sube → IA valida → 3 observaciones menores
→ Docente revisa → Descarta 2, confirma 1 como "sugerencia"
→ Docente APRUEBA → Alumno ve feedback → FIN ✅
```

### Caso 3: Informe Rechazado con Correcciones

```
Alumno sube v1 → IA valida → 5 observaciones críticas
→ Docente revisa → Confirma todas
→ Docente RECHAZA con comentario
→ Alumno ve feedback detallado
→ Alumno corrige y sube v2
→ IA valida v2 → 1 observación
→ Docente revisa v2 → APRUEBA ✅
```

### Caso 4: Múltiples Reenvíos

```
v1 → RECHAZADO (5 obs)
v2 → RECHAZADO (2 obs)
v3 → RECHAZADO (1 obs)
v4 → APROBADO (0 obs) ✅
```

---

## 🎯 Características Implementadas

✅ **Estados bien definidos** (7 estados del informe, 4 de observación)  
✅ **Revisión docente completa** (confirmar/descartar/comentar)  
✅ **Severidades ajustables** (crítica, importante, menor, sugerencia)  
✅ **Feedback bidireccional** (docente → alumno con comentarios)  
✅ **Versionado automático** (v1, v2, v3... con links)  
✅ **Interfaz profesional** para docente (revisar_informe.html)  
✅ **Interfaz clara** para alumno (validation_result.html)  
✅ **Código ordenado** con Clean Architecture  

---

## 🚀 Cómo Probar el Flujo

### Como Alumno:

1. Inicia sesión como estudiante
2. Ve a `/upload/`
3. Sube un archivo `.docx`
4. Espera la validación de IA
5. Ve el resultado en `/resultado/<id>/`
6. Si está rechazado, corrige y reenvía

### Como Docente:

1. Inicia sesión como docente
2. Ve a `/panel-docente/`
3. Busca informes con estado "OBSERVADO"
4. Clic en "⚙️ Revisar"
5. Revisa cada observación:
   - Confirma o descarta
   - Ajusta severidad
   - Agrega comentarios
6. Escribe feedback general
7. Decide: APROBAR o RECHAZAR

---

## 📝 Migraciones Aplicadas

```bash
✅ apps/informes/migrations/0002_...
   - Add field comentario_docente
   - Add field docente_revisor
   - Add field fecha_revision_docente
   - Add field informe_anterior
   - Add field version
   - Alter field estado (7 estados nuevos)

✅ apps/observaciones/migrations/0002_...
   - Add field comentario_docente
   - Add field estado (4 estados)
   - Add field fecha_revision
   - Add field severidad (4 niveles)
```

---

## 🎓 Próximas Mejoras Sugeridas

1. **Notificaciones por email** cuando docente revisa
2. **Dashboard del alumno** con progreso visual
3. **Comparación de versiones** (diff entre v1 y v2)
4. **Exportar feedback a PDF** para entregar físicamente
5. **Sistema de apelaciones** (alumno puede responder al docente)
6. **Métricas de calidad** (tiempo promedio de corrección)

---

## ✅ Resumen

**ANTES:** IA validaba → Alumno veía observaciones → FIN  
**AHORA:** IA valida → **Docente revisa y decide** → Alumno ve feedback → **Puede reenviar** → Flujo completo ✅

**El flujo está 100% implementado y funcional. El docente tiene control total sobre el proceso de revisión.**
