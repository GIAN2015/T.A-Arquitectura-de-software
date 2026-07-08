# 🔄 Flujo del Sistema - Validación de Informes UNTELS

> Documentación detallada de los flujos de trabajo del sistema

---

## 📋 Tabla de Contenidos

1. [Visión General del Flujo](#visión-general-del-flujo)
2. [Flujo Completo Paso a Paso](#flujo-completo-paso-a-paso)
3. [Diagramas de Secuencia](#diagramas-de-secuencia)
4. [Casos de Uso](#casos-de-uso)
5. [Flujos Alternativos](#flujos-alternativos)

---

## 🎯 Visión General del Flujo

### Flujo Principal (Camino Feliz)

```
┌──────────────┐
│  Estudiante  │ Sube informe → estado: enviado
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Secretaria  │ Deriva a escuela → estado: pendiente_presidente
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Presidente  │ Asigna docente → estado: pendiente_docente
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Docente    │ Valida con IA → estado: validando_ia
└──────┬───────┘              → estado: revision_docente
       │                       Confirma observaciones
       │                       Envía dictamen → estado: pendiente_aprobacion_presidente
       ▼
┌──────────────┐
│  Presidente  │ Decide resultado final o devuelve dictamen
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Secretaria  │ Notifica al estudiante → estado: aprobado_final ✅
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Estudiante  │ Recibe notificación de aprobación
└──────────────┘
```

### Estados del Sistema (11 totales)

| # | Estado | Descripción | Responsable |
|---|--------|-------------|-------------|
| 1 | `enviado` | Informe subido | Estudiante |
| 2 | `pendiente_secretaria` | En cola de secretaria | Secretaria |
| 3 | `pendiente_presidente` | Esperando asignación | Presidente |
| 4 | `pendiente_docente` | Asignado a docente | Docente |
| 5 | `validando_ia` | IA procesando | Sistema |
| 6 | `revision_docente` | Docente revisando IA | Docente |
| 7 | `pendiente_aprobacion_presidente` | Dictamen enviado | Presidente |
| 8 | `aprobado_presidente` | Presidente aprobó informe final | Secretaria |
| 9 | `rechazado_presidente` | Presidente rechazó informe final | Secretaria |
| 10 | `aprobado_final` | ✅ APROBADO | - |
| 11 | `rechazado_estudiante` | ❌ Estudiante debe corregir | Estudiante |

**Regla adicional**: si el presidente rechaza el dictamen del docente, el flujo vuelve a `revision_docente` con comentario del presidente para que el docente rehaga la revisión.

---

## 📝 Flujo Completo Paso a Paso

### Paso 1: Estudiante Sube Informe

**Actor**: Estudiante  
**Vista**: `estudiante/enviar_informe.html`  
**Endpoint**: `POST /estudiante/enviar/`

```python
# apps/presentacion/web/estudiante_views.py
@requiere_rol('estudiante')
def enviar_informe_view(request):
    if request.method == 'POST':
        archivo = request.FILES['archivo']
        
        # Crear informe
        informe = Informe.objects.create(
            usuario=estudiante,
            nombre_archivo=archivo.name,
            archivo=archivo,
            contenido=extraer_texto(archivo),
            estado='enviado',  # ESTADO INICIAL
            escuela=estudiante.escuela
        )
        
        # Notificar a secretaria
        NotificacionService.notificar_informe_nuevo(informe)
```

**Estado Resultante**: `enviado`

**Diagrama**:
```
Estudiante → [Formulario] → Backend → BD (nuevo Informe)
                                    → Notificación a Secretaria
```

---

### Paso 2: Secretaria Deriva a Presidente

**Actor**: Secretaria  
**Vista**: `secretaria/dashboard.html`  
**Endpoint**: `POST /secretaria/derivar/{id}/`

```python
# apps/negocio/servicios/secretaria.py
class SecretariaService:
    @staticmethod
    def derivar_a_presidente(informe_id, escuela_id, secretaria, comentario):
        # Obtener informe y presidente
        informe = Informe.objects.get(id=informe_id)
        escuela = Escuela.objects.get(id=escuela_id)
        presidente = escuela.presidente
        
        # Actualizar informe
        informe.secretaria_asignada = secretaria
        informe.presidente_asignado = presidente
        informe.escuela = escuela
        informe.comentario_secretaria = comentario
        
        # Cambiar estado usando State Machine
        informe.transition_to('pendiente_presidente')
        informe.fecha_asignacion_presidente = timezone.now()
        informe.save()
        
        # Notificar presidente
        NotificacionService.notificar_informe_derivado(informe, presidente)
```

**Transición**: `enviado` → `pendiente_presidente`

**Diagrama**:
```
Secretaria → Selecciona Escuela → Backend
                                 → State Machine (validar transición)
                                 → BD (actualizar estado)
                                 → Notificación a Presidente
```

---

### Paso 3: Presidente Asigna Docente

**Actor**: Presidente  
**Vista**: `presidente/revisar.html`  
**Endpoint**: `POST /presidente/asignar/{id}/`

```python
# apps/negocio/servicios/presidente.py
class PresidenteService:
    @staticmethod
    def asignar_docente(informe_id, presidente, docente_id):
        informe = Informe.objects.get(
            id=informe_id,
            presidente_asignado=presidente
        )
        docente = Usuario.objects.get(
            id=docente_id,
            tipo_usuario='docente',
            escuela=informe.escuela
        )
        
        # Asignar docente
        informe.docente_revisor = docente
        
        # Cambiar estado
        informe.transition_to('pendiente_docente')
        informe.fecha_asignacion_docente = timezone.now()
        informe.save()
        
        # Notificar docente
        NotificacionService.notificar_informe_asignado(informe, docente)
```

**Transición**: `pendiente_presidente` → `pendiente_docente`

---

### Paso 4: Docente Valida con IA

**Actor**: Docente  
**Vista**: `docente/revisar.html`  
**Endpoint**: `POST /docente/validar/{id}/`

```python
# apps/negocio/servicios/docente.py
class DocenteService:
    @staticmethod
    def validar_informe_con_ia(informe_id, docente, banco_especifico=None):
        # 1. Obtener informe
        informe = Informe.objects.get(
            id=informe_id,
            docente_revisor=docente
        )
        
        # 2. Cambiar a validando_ia
        informe.transition_to('validando_ia')
        informe.save()
        
        # 3. Obtener banco de observaciones
        banco = banco_especifico or BancoObservacionesDocente.objects.filter(
            docente=docente,
            activo=True
        ).first()
        
        # 4. Llamar servicio de IA
        from apps.observaciones.services import validar_con_groq
        observaciones_data = validar_con_groq(informe, banco)
        
        # 5. Crear observaciones en BD
        for obs in observaciones_data:
            ObservacionGenerada.objects.create(
                informe=informe,
                seccion=obs['seccion'],
                observacion=obs['observacion'],
                ubicacion_error=obs.get('ubicacion', ''),
                severidad=obs.get('severidad', 'menor'),
                estado='pendiente'  # Docente debe confirmar
            )
        
        # 6. Cambiar a revision_docente
        informe.transition_to('revision_docente')
        informe.banco_observaciones_usado = banco
        informe.save()
        
        return True, observaciones_data, None
```

**Transiciones**: 
- `pendiente_docente` → `validando_ia`
- `validando_ia` → `revision_docente`

**Diagrama de Secuencia**:
```
Docente → Backend → State Machine (→ validando_ia)
                  → BD (save)
                  → Servicio IA
                      → API Externa (xAI/Groq)
                      → Parsear JSON
                  → Crear Observaciones en BD
                  → State Machine (→ revision_docente)
                  → BD (save)
                  → Retornar a Docente
```

---

### Paso 5: Docente Confirma Observaciones y Envía Dictamen

**Actor**: Docente  
**Vista**: `docente/revisar.html`  
**Endpoint**: `POST /docente/dictamen/{id}/`

```python
# apps/negocio/servicios/docente.py
class DocenteService:
    @staticmethod
    def enviar_dictamen_a_presidente(informe_id, docente, comentario, recomendar):
        informe = Informe.objects.get(id=informe_id, docente_revisor=docente)
        
        # 1. Validación de negocio
        obs_confirmadas = ObservacionGenerada.objects.filter(
            informe=informe,
            estado='confirmada'
        ).count()
        
        if recomendar == 'rechazar' and obs_confirmadas == 0:
            return False, None, "Debe confirmar al menos 1 observación para rechazar"
        
        # 2. Generar dictamen estructurado
        dictamen = self._generar_dictamen_estructurado(
            informe, comentario, recomendar
        )
        
        # 3. Guardar dictamen
        informe.comentario_docente = dictamen
        
        # 4. Cambiar estado
        informe.transition_to('pendiente_aprobacion_presidente')
        informe.fecha_revision_docente = timezone.now()
        informe.save()
        
        # 5. Notificar presidente
        NotificacionService.notificar_dictamen_enviado(
            informe, informe.presidente_asignado
        )
        
        return True, informe, None
```

**Transición**: `revision_docente` → `pendiente_aprobacion_presidente`

---

### Paso 6: Presidente Revisa Dictamen

**Actor**: Presidente  
**Vista**: `presidente/revisar.html`  
**Endpoint**: `POST /presidente/revisar/{id}/`

```python
# apps/negocio/servicios/presidente.py
class PresidenteService:
    @staticmethod
    def aprobar_dictamen_docente(informe_id, presidente, comentario, aprobar_informe=True):
        informe = Informe.objects.get(
            id=informe_id,
            presidente_asignado=presidente
        )
        
        # Guardar comentario del presidente
        informe.comentario_presidente = comentario
        
        if accion == 'aprobar_final':
            # APRUEBA el informe final y lo envía a secretaría
            informe.transition_to('aprobado_presidente')
            NotificacionService.notificar_aprobacion_presidente_a_secretaria(
                informe, informe.secretaria_asignada
            )
        elif accion == 'rechazar_final':
            # RECHAZA el informe final y lo envía a secretaría
            informe.transition_to('rechazado_presidente')
            NotificacionService.notificar_rechazo_presidente_a_secretaria(
                informe, informe.secretaria_asignada
            )
        else:
            # DEVUELVE el dictamen al docente para rehacer revisión
            informe.estado = 'revision_docente'
            NotificacionService.notificar_rechazo_presidente_a_docente(
                informe, informe.docente_revisor
            )
        
        informe.fecha_aprobacion_presidente = timezone.now()
        informe.save()
```

**Resultados posibles**:
- `pendiente_aprobacion_presidente` → `aprobado_presidente` (aprueba informe final)
- `pendiente_aprobacion_presidente` → `rechazado_presidente` (rechaza informe final)
- `pendiente_aprobacion_presidente` → `revision_docente` (devuelve dictamen al docente)

---

### Paso 7A: Secretaria Notifica Aprobación (Camino Feliz)

**Actor**: Secretaria  
**Vista**: `secretaria/notificar.html`  
**Endpoint**: `POST /secretaria/notificar/{id}/aprobado/`

```python
# apps/negocio/servicios/secretaria.py
class SecretariaService:
    @staticmethod
    def notificar_estudiante_aprobado(informe_id, secretaria):
        informe = Informe.objects.get(id=informe_id)
        
        # ESTADO FINAL: APROBADO
        informe.transition_to('aprobado_final')
        informe.fecha_completado = timezone.now()
        informe.save()
        
        # Notificar estudiante
        NotificacionService.crear_notificacion(
            usuario=informe.usuario,
            tipo='aprobacion_final',
            titulo='✅ Informe APROBADO',
            mensaje='Su informe ha sido aprobado. Puede descargarlo.',
            informe=informe
        )
```

**Transición**: `aprobado_presidente` → `aprobado_final` ✅

---

### Paso 7B: Secretaria Notifica Rechazo (Camino Alternativo)

**Actor**: Secretaria  
**Vista**: `secretaria/notificar.html`  
**Endpoint**: `POST /secretaria/notificar/{id}/rechazado/`

```python
class SecretariaService:
    @staticmethod
    def notificar_estudiante_rechazado(informe_id, secretaria):
        informe = Informe.objects.get(id=informe_id)
        
        # Estado: Estudiante debe corregir
        informe.transition_to('rechazado_estudiante')
        informe.save()
        
        # Notificar estudiante con dictamen completo
        NotificacionService.crear_notificacion(
            usuario=informe.usuario,
            tipo='rechazo_final',
            titulo='❌ Informe RECHAZADO',
            mensaje=f'Su informe requiere correcciones. Ver dictamen.',
            informe=informe
        )
```

**Transición**: 
- Si presidente rechazó → `rechazado_presidente` → `rechazado_estudiante` ❌

---

## 📊 Diagramas de Secuencia

### Secuencia 1: Validación con IA

```
┌─────────┐   ┌─────────┐   ┌──────────┐   ┌─────────┐   ┌────────┐
│ Docente │   │  Vista  │   │ Servicio │   │ IA API  │   │   BD   │
└────┬────┘   └────┬────┘   └────┬─────┘   └────┬────┘   └───┬────┘
     │             │              │              │            │
     │ Click "Validar IA"         │              │            │
     ├────────────>│              │              │            │
     │             │              │              │            │
     │             │ validar_informe_con_ia()    │            │
     │             ├─────────────>│              │            │
     │             │              │              │            │
     │             │              │ estado = validando_ia     │
     │             │              ├──────────────────────────>│
     │             │              │              │            │
     │             │              │ POST /chat/completions    │
     │             │              ├─────────────>│            │
     │             │              │              │            │
     │             │              │ JSON observaciones        │
     │             │              │<─────────────┤            │
     │             │              │              │            │
     │             │              │ crear_observaciones()     │
     │             │              ├──────────────────────────>│
     │             │              │              │            │
     │             │              │ estado = revision_docente │
     │             │              ├──────────────────────────>│
     │             │              │              │            │
     │             │ (True, obs, None)           │            │
     │             │<─────────────┤              │            │
     │             │              │              │            │
     │ Muestra observaciones      │              │            │
     │<────────────┤              │              │            │
     │             │              │              │            │
```

### Secuencia 2: Aprobación Completa

```
┌──────────┐   ┌───────────┐   ┌───────────┐   ┌──────────┐
│Presidente│   │ Servicio  │   │   State   │   │    BD    │
└────┬─────┘   └─────┬─────┘   └─────┬─────┘   └────┬─────┘
     │               │               │              │
     │ Aprobar dictamen              │              │
     ├──────────────>│               │              │
     │               │               │              │
     │               │ transition_to('aprobado_presidente')
     │               ├──────────────>│              │
     │               │               │              │
     │               │               │ validar transición
     │               │               │              │
     │               │               │ estado OK    │
     │               │               ├─────────────>│
     │               │               │              │
     │               │ notificar_secretaria()       │
     │               ├─────────────────────────────>│
     │               │               │              │
     │ OK            │               │              │
     │<──────────────┤               │              │
```

---

## 🎭 Casos de Uso

### CU-01: Subir Informe

**Actor Principal**: Estudiante  
**Precondiciones**: Usuario autenticado como estudiante  
**Postcondiciones**: Informe en estado `enviado`, secretaria notificada

**Flujo Principal**:
1. Estudiante accede a "Enviar Informe"
2. Sistema muestra formulario
3. Estudiante selecciona archivo PDF/DOCX
4. Estudiante hace clic en "Enviar"
5. Sistema valida archivo
6. Sistema extrae texto
7. Sistema guarda informe en estado `enviado`
8. Sistema notifica a secretaria
9. Sistema muestra confirmación

**Flujos Alternativos**:
- 5a. Archivo inválido → mostrar error
- 5b. Archivo muy grande → mostrar error
- 5c. Formato no soportado → mostrar error

---

### CU-02: Validar con IA

**Actor Principal**: Docente  
**Precondiciones**: 
- Informe asignado al docente
- Estado: `pendiente_docente` o `rechazado_presidente`
- Banco de observaciones activo

**Postcondiciones**: 
- Observaciones generadas
- Estado: `revision_docente`

**Flujo Principal**:
1. Docente accede a "Revisar Informe"
2. Sistema muestra detalles del informe
3. Docente hace clic en "Validar con IA"
4. Sistema muestra modal de selección de banco
5. Docente selecciona banco (o usa el activo)
6. Docente confirma
7. Sistema cambia estado a `validando_ia`
8. Sistema muestra barra de progreso
9. Sistema llama API de IA
10. Sistema parsea respuesta JSON
11. Sistema crea observaciones en BD
12. Sistema cambia estado a `revision_docente`
13. Sistema muestra observaciones generadas

**Flujos Alternativos**:
- 9a. API sin créditos → fallback local
- 9b. API error → fallback local
- 9c. Timeout → mostrar error, permitir reintentar

---

### CU-03: Aprobar/Rechazar Dictamen

**Actor Principal**: Presidente  
**Precondiciones**: 
- Informe en estado `pendiente_aprobacion_presidente`
- Dictamen enviado por docente

**Postcondiciones**: 
- Estado: `aprobado_presidente`, `rechazado_presidente` o `revision_docente`
- Notificación enviada a secretaría o docente según la decisión

**Flujo Principal (Aprobar Informe Final)**:
1. Presidente accede a "Revisar Dictamen"
2. Sistema muestra dictamen formateado
3. Presidente lee dictamen
4. Presidente escribe comentario (opcional)
5. Presidente hace clic en "Aprobar y Enviar a Secretaría"
6. Sistema confirma acción
7. Sistema cambia estado a `aprobado_presidente`
8. Sistema notifica a secretaria
9. Sistema muestra confirmación

**Flujo Alternativo A (Rechazar Informe Final)**:
5a. Presidente hace clic en "Rechazar Informe y Enviar a Secretaría"
6a. Sistema solicita comentario obligatorio
7a. Sistema cambia estado a `rechazado_presidente`
8a. Sistema notifica a secretaría
9a. Sistema muestra confirmación

**Flujo Alternativo B (Devolver Dictamen al Docente)**:
5b. Presidente hace clic en "Devolver al Docente"
6b. Sistema solicita comentario obligatorio
7b. Sistema cambia estado a `revision_docente`
8b. Sistema notifica al docente
9b. Sistema muestra confirmación

---

## 🔀 Flujos Alternativos

### Flujo 1: Presidente Devuelve Dictamen al Docente

```
... (desde Paso 6)
Presidente devuelve dictamen
  ↓
Estado: revision_docente
  ↓
Notifica a Docente
  ↓
Docente puede:
  - Re-validar con IA o continuar desde revisión docente
  - Modificar dictamen
  - Enviar nuevo dictamen
  ↓
Vuelve al Paso 5
```

### Flujo 2: Estudiante Reenvía Informe Corregido

```
Estudiante en estado: rechazado_estudiante
  ↓
Ve dictamen completo con observaciones
  ↓
Corrige su informe
  ↓
Sube nuevo archivo (v2)
  ↓
Estado: enviado
  ↓
Se crea NUEVO informe con:
  - version = 2
  - informe_anterior = informe_v1
  - informe_v1 queda cerrado para futuros reenvíos
  ↓
Flujo completo se reinicia desde Paso 1
```

### Flujo 3: Validación Sin Créditos de IA

```
Docente solicita validación con IA
  ↓
Sistema llama API
  ↓
API retorna: 400 (sin créditos)
  ↓
Sistema detecta error
  ↓
Fallback automático a validación local
  ↓
Sistema genera observación básica
  ↓
Estado: revision_docente
  ↓
Docente puede agregar observaciones manualmente
```

---

## 📈 Métricas del Flujo

### Tiempos Estimados

| Etapa | Responsable | Tiempo Estimado |
|-------|-------------|----------------|
| Estudiante sube | Estudiante | 5 min |
| Secretaria deriva | Secretaria | 2 min |
| Presidente asigna | Presidente | 3 min |
| **Docente valida con IA** | **Sistema** | **10-30 seg** |
| Docente confirma | Docente | 10-15 min |
| Presidente revisa | Presidente | 5-10 min |
| Secretaria notifica | Secretaria | 2 min |
| **TOTAL** | - | **~30-40 min** |

**Antes (manual)**: 2-3 días  
**Ahora (con IA)**: ~40 minutos

---

## ✅ Conclusión

El sistema implementa un flujo complejo pero bien estructurado:

- ✅ **11 estados** claramente definidos
- ✅ **7 pasos principales** con responsables claros
- ✅ **3 flujos alternativos** bien manejados
- ✅ **State Machine** garantiza transiciones válidas
- ✅ **Notificaciones** en cada paso
- ✅ **Trazabilidad** completa con fechas

---

**Ver también**: [Arquitectura](ARQUITECTURA.md), [Patrones](PATRONES.md), [Backend](BACKEND.md)
