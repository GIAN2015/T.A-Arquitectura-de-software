# 🔄 FLUJO COMPLETO V2.0 - Sistema UNTELS

## ✅ IMPLEMENTADO Y FUNCIONANDO

El sistema ahora sigue el **flujo completo multi-rol** desde que el estudiante envía el informe hasta que recibe el resultado final.

---

## 📊 Diagrama del Flujo

```
ESTUDIANTE (Envía)
    ↓
SECRETARIA (Deriva)
    ↓
PRESIDENTE (Asigna Docente)
    ↓
DOCENTE (Crea Banco + Valida con IA)
    ↓
PRESIDENTE (Aprueba Dictamen)
    ↓
SECRETARIA (Notifica)
    ↓
ESTUDIANTE (Recibe Resultado)
```

---

## 🎯 PASO A PASO COMPLETO

### PASO 1: ESTUDIANTE ENVÍA INFORME

**Usuario:** `2020123456` / `test123`  
**URL:** http://localhost:8000/

**Acciones:**
1. Login como estudiante
2. Ir a "Subir Informe"
3. Seleccionar archivo PDF o DOCX
4. Click en "Subir Informe"

**Resultado:**
- ✅ Informe creado con estado: `ENVIADO`
- ✅ Asignado a la escuela del estudiante (ISI)
- ✅ Mensaje: "Será procesado por la Secretaría Académica"

**Base de Datos:**
```sql
INSERT INTO informe (
    usuario_id,
    nombre_archivo,
    archivo,
    contenido,
    estado,
    escuela_id
) VALUES (
    estudiante_id,
    'mi_informe.pdf',
    '/media/informes/2026/07/mi_informe.pdf',
    'contenido extraído...',
    'enviado',  ← AQUÍ QUEDA
    escuela_id
);
```

---

### PASO 2: SECRETARIA RECIBE Y DERIVA

**Usuario:** `secretaria1` / `test123`  
**URL:** http://localhost:8000/secretaria/login/

**Acciones:**
1. Login como secretaria
2. Ver dashboard → Lista de "Informes Recibidos"
3. Click en "Derivar" en el informe del estudiante
4. Seleccionar escuela: "Ingeniería de Sistemas (ISI)"
5. (Opcional) Agregar comentario
6. Click en "Derivar a Presidente"

**Resultado:**
- ✅ Estado cambia a: `PENDIENTE_PRESIDENTE`
- ✅ Se asigna: `secretaria_asignada`, `escuela`, `presidente_asignado`
- ✅ Se registra: `fecha_asignacion_secretaria`
- ✅ Notificación creada para el presidente

**Base de Datos:**
```sql
UPDATE informe SET
    secretaria_asignada_id = secretaria_id,
    escuela_id = escuela_id,
    presidente_asignado_id = presidente_id,
    comentario_secretaria = 'Derivado...',
    fecha_asignacion_secretaria = NOW(),
    estado = 'pendiente_presidente'  ← CAMBIÓ
WHERE id = informe_id;

INSERT INTO notificacion (
    usuario_id,
    tipo,
    titulo,
    mensaje,
    informe_id
) VALUES (
    presidente_id,
    'derivacion_presidente',
    'Nuevo informe asignado',
    '...',
    informe_id
);
```

---

### PASO 3: PRESIDENTE RECIBE Y ASIGNA DOCENTE

**Usuario:** `presidente_isi` / `test123`  
**URL:** http://localhost:8000/presidente/login/

**Acciones:**
1. Login como presidente
2. Ver dashboard → Lista de "Pendientes de Asignar Docente"
3. Click en "Designar Docente" en el informe
4. Seleccionar docente: "Ing. Carlos Ramírez (docente_isi_1)"
5. (Opcional) Agregar comentario
6. Click en "Asignar Docente"

**Resultado:**
- ✅ Estado cambia a: `PENDIENTE_DOCENTE`
- ✅ Se asigna: `docente_revisor`
- ✅ Se registra: `fecha_asignacion_docente`
- ✅ Notificación creada para el docente

**Base de Datos:**
```sql
UPDATE informe SET
    docente_revisor_id = docente_id,
    fecha_asignacion_docente = NOW(),
    estado = 'pendiente_docente'  ← CAMBIÓ
WHERE id = informe_id;

INSERT INTO notificacion (
    usuario_id,
    tipo,
    titulo,
    mensaje,
    informe_id
) VALUES (
    docente_id,
    'asignacion_docente',
    'Nuevo informe asignado para revisión',
    '...',
    informe_id
);
```

---

### PASO 4: DOCENTE CREA BANCO (Si no tiene)

**Usuario:** `docente_isi_1` / `test123`  
**URL:** http://localhost:8000/docente/login/

**Acciones:**
1. Login como docente
2. Ir a "Mi Banco"
3. En "Crear Nuevo Banco":
   - Nombre: "Observaciones 2026-1"
   - Archivo: Subir PDF o DOCX con observaciones
4. Click en "Crear Banco"

**Resultado:**
- ✅ Banco creado y activado automáticamente
- ✅ Contenido extraído del archivo
- ✅ Listo para usar en validación

**Base de Datos:**
```sql
INSERT INTO banco_observaciones_docente (
    docente_id,
    nombre,
    archivo,
    contenido_extraido,
    activo
) VALUES (
    docente_id,
    'Observaciones 2026-1',
    '/media/bancos/2026/07/obs.pdf',
    'contenido extraído...',
    TRUE  ← Activo
);
```

---

### PASO 5: DOCENTE VALIDA CON IA

**Usuario:** `docente_isi_1` / `test123`

**Acciones:**
1. Volver a "Dashboard"
2. Ver lista de "Informes Asignados"
3. Click en "Revisar" en el informe
4. Sistema automáticamente:
   - Detecta que tiene banco activo
   - Usa GROQ API + Llama 3.3 70B
   - Combina: Reglamento + Banco del Docente + Contenido del Informe
   - Genera observaciones (ej: falta índice, formato incorrecto, etc.)
5. Ver tabla de observaciones generadas
6. Opciones por observación:
   - ✅ Confirmar
   - ❌ Descartar
   - ✏️ Editar
7. Al final:
   - Click en "Aprobar Informe" o "Rechazar Informe"
   - Agregar comentario general

**Resultado:**
- ✅ Estado cambia a: `PENDIENTE_APROBACION_PRESIDENTE`
- ✅ Observaciones confirmadas guardadas
- ✅ Dictamen del docente registrado
- ✅ Notificación al presidente

**Base de Datos:**
```sql
-- Cambiar estado del informe
UPDATE informe SET
    estado = 'pendiente_aprobacion_presidente',  ← CAMBIÓ
    comentario_docente = 'El informe presenta...',
    fecha_revision_docente = NOW(),
    banco_observaciones_usado_id = banco_id
WHERE id = informe_id;

-- Guardar observaciones confirmadas
INSERT INTO observacion_generada (
    informe_id,
    seccion,
    observacion,
    ubicacion_error,
    severidad,
    estado
) VALUES
(informe_id, 'Carátula', 'Falta logo UNTELS', 'Página 1', 'critica', 'confirmada'),
(informe_id, 'Formato', 'Interlineado incorrecto', 'General', 'importante', 'confirmada'),
...;

-- Notificar al presidente
INSERT INTO notificacion (...);
```

---

### PASO 6: PRESIDENTE REVISA DICTAMEN

**Usuario:** `presidente_isi` / `test123`

**Acciones:**
1. Volver a dashboard
2. Ver lista de "Dictámenes Pendientes de Aprobar"
3. Click en "Revisar Dictamen"
4. Ver:
   - Comentario del docente
   - Observaciones encontradas
   - Recomendación (aprobar/rechazar)
5. Decidir:
   - ✅ "Aprobar Dictamen" → El informe pasa
   - ❌ "Rechazar Dictamen" → El informe debe corregirse
6. Agregar comentario de presidente
7. Click en confirmar

**Resultado:**
- ✅ Estado cambia a: `APROBADO_PRESIDENTE` o `RECHAZADO_PRESIDENTE`
- ✅ Comentario del presidente guardado
- ✅ Notificación a secretaria

**Base de Datos:**
```sql
UPDATE informe SET
    estado = 'aprobado_presidente',  ← o 'rechazado_presidente'
    comentario_presidente = 'El dictamen es correcto...',
    fecha_aprobacion_presidente = NOW()
WHERE id = informe_id;

INSERT INTO notificacion (
    usuario_id,
    tipo,
    titulo,
    mensaje
) VALUES (
    secretaria_id,
    'dictamen_aprobado',  ← o 'dictamen_rechazado'
    'Dictamen listo para notificar',
    '...'
);
```

---

### PASO 7: SECRETARIA NOTIFICA AL ESTUDIANTE

**Usuario:** `secretaria1` / `test123`

**Acciones:**
1. Volver a dashboard
2. Ver lista de "Listos para Notificar"
3. Click en "Notificar Estudiante"
4. Revisar resultado final
5. Click en "Confirmar Notificación"

**Resultado:**
- ✅ Estado cambia a: `APROBADO_FINAL` o `RECHAZADO_ESTUDIANTE`
- ✅ Fecha de completado registrada
- ✅ Notificación al estudiante

**Base de Datos:**
```sql
UPDATE informe SET
    estado = 'aprobado_final',  ← o 'rechazado_estudiante'
    fecha_completado = NOW()
WHERE id = informe_id;

INSERT INTO notificacion (
    usuario_id,
    tipo,
    titulo,
    mensaje
) VALUES (
    estudiante_id,
    'resultado_final',
    'Resultado de tu informe',
    '...'
);
```

---

### PASO 8: ESTUDIANTE RECIBE RESULTADO

**Usuario:** `2020123456` / `test123`

**Acciones:**
1. Volver a login estudiante
2. Ver "Mis Informes" → El informe tiene nuevo estado
3. Click en el informe para ver detalles

**Ver:**
- ✅ Estado final: APROBADO o RECHAZADO
- ✅ Observaciones (si las hay)
- ✅ Comentarios de: Secretaria, Presidente, Docente
- ✅ Fechas de cada etapa

**Si fue rechazado:**
- Puede enviar una **nueva versión** corregida
- El flujo comienza de nuevo desde el PASO 1

---

## 📊 Estados del Informe Durante el Flujo

| Paso | Responsable | Estado | Siguiente Acción |
|------|------------|--------|------------------|
| 1 | Estudiante | `enviado` | Secretaria deriva |
| 2 | Secretaria | `pendiente_presidente` | Presidente asigna docente |
| 3 | Presidente | `pendiente_docente` | Docente valida |
| 4-5 | Docente | `validando_ia` → `revision_docente` | Docente aprueba/rechaza |
| 6 | Docente | `pendiente_aprobacion_presidente` | Presidente revisa dictamen |
| 7 | Presidente | `aprobado_presidente` / `rechazado_presidente` | Secretaria notifica |
| 8 | Secretaria | `aprobado_final` / `rechazado_estudiante` | Estudiante ve resultado |

---

## ✅ Verificación del Flujo

Para probar el flujo completo:

```bash
cd backend
./venv/bin/python manage.py shell <<'EOF'
from apps.informes.models import Informe
from apps.usuarios.models import Usuario

# Obtener últimoinforme
informe = Informe.objects.latest('id')

print(f"\n📄 ESTADO DEL INFORME #{informe.id}")
print(f"   Archivo: {informe.nombre_archivo}")
print(f"   Estudiante: {informe.usuario.nombre}")
print(f"   Estado actual: {informe.get_estado_display()}")
print(f"\n📅 HISTORIAL:")
print(f"   Enviado: {informe.fecha_registro}")
if informe.secretaria_asignada:
    print(f"   Secretaria derivó: {informe.fecha_asignacion_secretaria}")
if informe.presidente_asignado:
    print(f"   Presidente asignó: {informe.fecha_asignacion_docente}")
if informe.docente_revisor:
    print(f"   Docente revisó: {informe.fecha_revision_docente or 'Pendiente'}")
if informe.fecha_aprobacion_presidente:
    print(f"   Presidente aprobó: {informe.fecha_aprobacion_presidente}")
if informe.fecha_completado:
    print(f"   Completado: {informe.fecha_completado}")
EOF
```

---

## 🔧 Cambios Implementados

### Archivos Modificados:

1. **apps/presentacion/web/estudiante_views.py**
   - Flujo v1.0 → Flujo v2.0
   - Informe se queda en estado `ENVIADO`
   - Guarda archivo físicamente
   - No valida con IA (lo hace el docente después)

2. **apps/negocio/servicios/secretaria.py**
   - `obtener_informes_pendientes()` ahora incluye estado `ENVIADO`

---

## ✅ TODO FUNCIONANDO

El flujo completo v2.0 está implementado y operativo:

- ✅ Estudiante → Envía informe
- ✅ Secretaria → Deriva a presidente
- ✅ Presidente → Asigna docente
- ✅ Docente → Valida con IA usando su banco
- ✅ Presidente → Aprueba dictamen
- ✅ Secretaria → Notifica
- ✅ Estudiante → Recibe resultado

**Pruébalo siguiendo los 8 pasos de arriba.**

---

Última actualización: 8 de Julio de 2026, 00:15 hrs
