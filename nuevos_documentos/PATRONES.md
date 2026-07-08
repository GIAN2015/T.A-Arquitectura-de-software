# 🧩 Patrones de Diseño - Sistema de Validación UNTELS

> Documentación detallada de todos los patrones de diseño implementados

---

## 📋 Tabla de Contenidos

1. [Repository Pattern](#1-repository-pattern)
2. [Service Layer Pattern](#2-service-layer-pattern)
3. [State Machine Pattern](#3-state-machine-pattern)
4. [Strategy Pattern](#4-strategy-pattern)
5. [Template Method Pattern](#5-template-method-pattern)
6. [Facade Pattern](#6-facade-pattern)
7. [Observer Pattern](#7-observer-pattern)
8. [Decorator Pattern](#8-decorator-pattern)

---

## 1. Repository Pattern

### 📝 Descripción
Abstrae el acceso a la capa de datos, proporcionando una interfaz orientada a colecciones para acceder a objetos del dominio.

### 🎯 Propósito
- Separar la lógica de acceso a datos de la lógica de negocio
- Facilitar el cambio de base de datos o ORM
- Centralizar queries complejas

### 📍 Ubicación
**Directorio**: `backend/apps/datos/repositorios/`

### 💻 Implementación

#### Archivo: `apps/datos/repositorios/informes.py`

```python
class InformeRepository:
    """
    Patrón Repository para Informes
    Abstrae todas las operaciones de acceso a datos
    """
    
    @staticmethod
    def obtener_por_id(informe_id):
        """
        Obtiene un informe por ID con relaciones precargadas
        
        VENTAJA: Centraliza la query, evita N+1 queries
        """
        return Informe.objects.select_related(
            'usuario',
            'escuela',
            'docente_revisor',
            'presidente_asignado',
            'secretaria_asignada'
        ).get(id=informe_id)
    
    @staticmethod
    def obtener_con_observaciones(informe_id):
        """
        Obtiene informe con observaciones precargadas
        
        VENTAJA: Evita múltiples queries a la BD
        """
        return Informe.objects.prefetch_related(
            'observaciones'
        ).get(id=informe_id)
    
    @staticmethod
    def obtener_por_estado_y_docente(estado, docente, limit=None):
        """
        Query compleja centralizada
        """
        query = Informe.objects.filter(
            estado=estado,
            docente_revisor=docente
        ).select_related('usuario', 'escuela')
        
        if limit:
            query = query[:limit]
        
        return query
```

### ✅ Beneficios Aplicados

1. **Testabilidad**: Se puede mockear el repositorio en tests
2. **Mantenibilidad**: Cambios en queries en un solo lugar
3. **Performance**: Queries optimizadas con select_related/prefetch_related
4. **Independencia**: La lógica de negocio no conoce el ORM

### 📦 Dónde se Usa

| Repositorio | Archivo | Usado Por |
|-------------|---------|-----------|
| `InformeRepository` | `informes.py` | DocenteService, PresidenteService |
| `UsuarioRepository` | `usuarios.py` | Todos los servicios |
| `ObservacionRepository` | `observaciones.py` | DocenteService |

---

## 2. Service Layer Pattern

### 📝 Descripción
Encapsula toda la lógica de negocio en servicios reutilizables y testeables.

### 🎯 Propósito
- Centralizar la lógica de negocio
- Reutilizar código entre diferentes capas (web, API, CLI)
- Facilitar testing sin framework

### 📍 Ubicación
**Directorio**: `backend/apps/negocio/servicios/`

### 💻 Implementación

#### Archivo: `apps/negocio/servicios/docente.py`

```python
class DocenteService:
    """
    Servicio de Negocio para Docentes
    
    PATRÓN: Service Layer
    RESPONSABILIDAD: TODA la lógica de negocio de docentes
    """
    
    @staticmethod
    def validar_informe_con_ia(informe_id, docente, banco_especifico=None):
        """
        Validación de informe con IA
        
        LÓGICA DE NEGOCIO:
        1. Verificar permisos del docente
        2. Validar estado del informe
        3. Obtener banco de observaciones
        4. Llamar servicio de IA
        5. Crear observaciones en BD
        6. Actualizar estado del informe
        7. Notificar eventos
        
        Returns:
            tuple: (success: bool, data: any, error: str)
        """
        try:
            # 1. Obtener informe (puede lanzar DoesNotExist)
            informe = Informe.objects.get(
                id=informe_id,
                docente_revisor=docente
            )
            
            # 2. Validar estado de negocio
            if informe.estado not in [
                Informe.ESTADO_PENDIENTE_DOCENTE,
                Informe.ESTADO_RECHAZADO_PRESIDENTE
            ]:
                return False, [], "El informe no está en estado válido"
            
            # 3. Obtener banco
            banco = banco_especifico or self.obtener_banco_activo(docente)
            if not banco:
                return False, [], "No hay banco activo"
            
            # 4. Validar con IA (delega a servicio externo)
            from apps.observaciones.services import validar_informe
            observaciones = validar_informe(informe, banco)
            
            # 5. Persistir observaciones
            for obs_data in observaciones:
                ObservacionGenerada.objects.create(
                    informe=informe,
                    seccion=obs_data['seccion'],
                    observacion=obs_data['observacion'],
                    # ...
                )
            
            # 6. Actualizar estado
            informe.estado = Informe.ESTADO_REVISION_DOCENTE
            informe.banco_observaciones_usado = banco
            informe.save()
            
            # 7. Retornar resultado (patrón de respuesta estándar)
            return True, observaciones, None
            
        except Informe.DoesNotExist:
            return False, [], "Informe no encontrado"
        except Exception as e:
            return False, [], f"Error: {str(e)}"
```

### 🔄 Patrón de Respuesta Estándar

TODOS los métodos de servicios retornan:

```python
(success: bool, data: any, error: str)

# Éxito
return True, resultado, None

# Error
return False, None, "Mensaje de error"
```

### ✅ Beneficios Aplicados

1. **Reusabilidad**: Misma lógica desde web, API, CLI, Celery
2. **Testabilidad**: Test sin Django, sin BD
3. **Mantenibilidad**: Un solo lugar para lógica de negocio
4. **Consistencia**: Patrón de respuesta uniforme

### 📦 Servicios Implementados

| Servicio | Archivo | Métodos Principales |
|----------|---------|-------------------|
| `DocenteService` | `docente.py` | validar_informe_con_ia(), enviar_dictamen_a_presidente(), obtener_estadisticas() |
| `PresidenteService` | `presidente.py` | asignar_docente(), revisar_dictamen(), obtener_informes_pendientes() |
| `SecretariaService` | `secretaria.py` | derivar_a_presidente(), notificar_estudiante_aprobado(), notificar_estudiante_rechazado() |
| `NotificacionService` | `notificaciones/services.py` | crear_notificacion(), notificar_*() |

---

## 3. State Machine Pattern

### 📝 Descripción
Gestiona las transiciones de estado del informe de forma controlada y predecible.

### 🎯 Propósito
- Evitar transiciones de estado inválidas
- Centralizar la lógica de cambios de estado
- Documentar el flujo completo del sistema

### 📍 Ubicación
**Archivo**: `backend/apps/informes/state.py`

### 💻 Implementación

```python
class InformeStateError(Exception):
    """Excepción para transiciones inválidas"""
    pass


class BaseInformeState:
    """Clase base para todos los estados"""
    value = None
    allowed_transitions = set()
    
    def can_transition_to(self, next_state):
        """Verifica si la transición es válida"""
        return next_state in self.allowed_transitions
    
    def transition(self, informe, next_state):
        """
        Ejecuta la transición de estado
        
        VALIDA: Solo permite transiciones permitidas
        """
        if not self.can_transition_to(next_state):
            raise InformeStateError(
                f"No se puede cambiar de '{self.value}' a '{next_state}'"
            )
        informe.estado = next_state
        return informe


class EnviadoState(BaseInformeState):
    """Estado inicial: Informe enviado por estudiante"""
    value = 'enviado'
    allowed_transitions = {'pendiente_secretaria'}


class PendienteSecretariaState(BaseInformeState):
    """Esperando que secretaria lo derive"""
    value = 'pendiente_secretaria'
    allowed_transitions = {'pendiente_presidente'}


class PendientePresidenteState(BaseInformeState):
    """Esperando que presidente asigne docente"""
    value = 'pendiente_presidente'
    allowed_transitions = {'pendiente_docente'}


class PendienteDocenteState(BaseInformeState):
    """Docente debe validar con IA"""
    value = 'pendiente_docente'
    allowed_transitions = {'validando_ia'}


class ValidandoIAState(BaseInformeState):
    """IA está procesando el informe"""
    value = 'validando_ia'
    allowed_transitions = {'revision_docente'}


class RevisionDocenteState(BaseInformeState):
    """Docente revisando observaciones de IA"""
    value = 'revision_docente'
    allowed_transitions = {
        'pendiente_aprobacion_presidente',
        'rechazado_estudiante'
    }


class PendienteAprobacionPresidenteState(BaseInformeState):
    """Presidente debe aprobar/rechazar dictamen"""
    value = 'pendiente_aprobacion_presidente'
    allowed_transitions = {
        'aprobado_presidente',
        'rechazado_presidente'
    }


class AprobadoPresidenteState(BaseInformeState):
    """Presidente aprobó, secretaria debe notificar"""
    value = 'aprobado_presidente'
    allowed_transitions = {'aprobado_final'}


class RechazadoPresidenteState(BaseInformeState):
    """Presidente rechazó, docente debe revisar de nuevo"""
    value = 'rechazado_presidente'
    allowed_transitions = {'validando_ia', 'revision_docente'}


class AprobadoFinalState(BaseInformeState):
    """Estado final: APROBADO"""
    value = 'aprobado_final'
    allowed_transitions = set()  # Final, no hay salida


class RechazadoEstudianteState(BaseInformeState):
    """Estudiante debe corregir y reenviar"""
    value = 'rechazado_estudiante'
    allowed_transitions = {'enviado'}


# Mapa de estados
STATE_MAP = {
    'enviado': EnviadoState(),
    'pendiente_secretaria': PendienteSecretariaState(),
    'pendiente_presidente': PendientePresidenteState(),
    'pendiente_docente': PendienteDocenteState(),
    'validando_ia': ValidandoIAState(),
    'revision_docente': RevisionDocenteState(),
    'pendiente_aprobacion_presidente': PendienteAprobacionPresidenteState(),
    'aprobado_presidente': AprobadoPresidenteState(),
    'rechazado_presidente': RechazadoPresidenteState(),
    'aprobado_final': AprobadoFinalState(),
    'rechazado_estudiante': RechazadoEstudianteState(),
}


def get_state(state_value: str) -> BaseInformeState:
    """Obtiene la instancia del estado"""
    try:
        return STATE_MAP[state_value]
    except KeyError:
        raise InformeStateError(f"Estado desconocido: {state_value}")
```

### 🔄 Uso en el Modelo

```python
# apps/informes/models.py
class Informe(models.Model):
    # ... campos ...
    
    def transition_to(self, next_state):
        """Cambiar estado de forma segura"""
        state = get_state(self.estado)
        state.transition(self, next_state)
        # NO hace save(), el servicio decide cuándo guardar
```

### 📊 Diagrama de Estados

```
enviado
  ↓
pendiente_secretaria
  ↓
pendiente_presidente
  ↓
pendiente_docente
  ↓
validando_ia
  ↓
revision_docente
  ↓         ↘
  ↓          rechazado_estudiante → enviado (reenvío)
  ↓
pendiente_aprobacion_presidente
  ↓         ↘
  ↓          rechazado_presidente → validando_ia (re-validar)
  ↓
aprobado_presidente
  ↓
aprobado_final [FIN]
```

### ✅ Beneficios Aplicados

1. **Seguridad**: Imposible hacer transiciones inválidas
2. **Documentación viva**: El código ES el diagrama
3. **Fácil de extender**: Agregar nuevos estados es simple
4. **Testeable**: Se puede probar cada transición

---

## 4. Strategy Pattern

### 📝 Descripción
Permite seleccionar el algoritmo de validación de IA en tiempo de ejecución.

### 🎯 Propósito
- Soportar múltiples APIs de IA sin modificar código
- Fallback automático si una API falla
- Fácil agregar nuevas APIs

### 📍 Ubicación
**Archivo**: `backend/apps/observaciones/services.py`

### 💻 Implementación

```python
def validar_con_groq(informe, banco_observaciones):
    """
    PATRÓN: Strategy
    
    Selecciona la estrategia de validación según la API key:
    - xai-... → xAI Grok API
    - gsk_... → Groq API (LLaMA)
    - otro    → Validación local
    """
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
    
    # ESTRATEGIA 1: xAI Grok
    if GROQ_API_KEY.startswith('xai-'):
        return _validar_con_xai(informe, banco_observaciones)
    
    # ESTRATEGIA 2: Groq (LLaMA)
    elif GROQ_API_KEY.startswith('gsk_'):
        return _validar_con_groq_api(informe, banco_observaciones)
    
    # ESTRATEGIA 3: Fallback local
    else:
        return _validacion_local(informe, banco_observaciones)


def _validar_con_xai(informe, banco):
    """Estrategia: xAI Grok API"""
    url = 'https://api.x.ai/v1/chat/completions'
    modelo = 'grok-beta'
    
    try:
        response = requests.post(url, json={
            'model': modelo,
            'messages': [{'role': 'user', 'content': construir_prompt(informe, banco)}],
        }, headers={'Authorization': f'Bearer {GROQ_API_KEY}'})
        
        if response.status_code == 400:
            # Sin créditos → Fallback
            return _validacion_local(informe, banco)
        
        return parsear_respuesta_ia(response.json())
    except:
        return _validacion_local(informe, banco)


def _validar_con_groq_api(informe, banco):
    """Estrategia: Groq API (rápido y gratis)"""
    url = 'https://api.groq.com/openai/v1/chat/completions'
    modelo = 'llama-3.3-70b-versatile'
    
    # Similar a xAI pero con endpoint diferente
    # ...


def _validacion_local(informe, banco):
    """Estrategia: Validación local (fallback)"""
    return [{
        'seccion': 'Sistema',
        'observacion': 'Validación básica: API de IA no disponible',
        'severidad': 'importante'
    }]
```

### ✅ Beneficios Aplicados

1. **Flexibilidad**: Cambiar de API sin tocar código
2. **Resilencia**: Fallback automático si falla
3. **Extensibilidad**: Agregar OpenAI, Claude, etc. es fácil

### 📦 Dónde se Usa

**Llamado desde**: `DocenteService.validar_informe_con_ia()`

---

## 5. Template Method Pattern

### 📝 Descripción
Define el esqueleto de un algoritmo, permitiendo que las subclases redefinan ciertos pasos.

### 🎯 Propósito
- Reutilizar estructura común
- Permitir personalización en puntos específicos

### 📍 Ubicación
**Archivo**: `backend/apps/core/templatetags/dictamen_filters.py`

### 💻 Implementación

```python
@register.filter(name='formatear_dictamen')
def formatear_dictamen(texto):
    """
    PATRÓN: Template Method
    
    Algoritmo de parseo y formateo:
    1. Dividir en líneas
    2. Para cada línea:
       - Detectar tipo (encabezado, lista, párrafo)
       - Aplicar formato HTML específico
    3. Unir resultado
    """
    if not texto:
        return '<p class="text-muted">Sin dictamen</p>'
    
    html_parts = []
    lines = texto.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # PASO 1: Detectar tipo de línea
        tipo = _detectar_tipo_linea(line)
        
        # PASO 2: Aplicar formato según tipo
        if tipo == 'encabezado':
            html = _formatear_encabezado(line)
        elif tipo == 'observacion':
            html, lineas_consumidas = _formatear_observacion(lines, i)
            i += lineas_consumidas
        elif tipo == 'lista':
            html = _formatear_lista(line)
        else:
            html = _formatear_parrafo(line)
        
        html_parts.append(html)
        i += 1
    
    # PASO 3: Unir y retornar
    return mark_safe(''.join(html_parts))


def _detectar_tipo_linea(line):
    """Paso customizable: detectar tipo"""
    if line.startswith('===='):
        return 'separador'
    elif line.isupper() and len(line) < 50:
        return 'encabezado'
    elif re.match(r'^\d+\. .*', line):
        return 'lista'
    elif line.startswith('🔴') or line.startswith('🟠'):
        return 'observacion'
    else:
        return 'parrafo'


def _formatear_encabezado(line):
    """Paso customizable: formatear encabezado"""
    return f'<h5 class="fw-bold mt-3">{line}</h5>'


def _formatear_observacion(lines, start_index):
    """Paso customizable: formatear observación con card"""
    line = lines[start_index]
    
    # Detectar severidad por emoji
    if '🔴' in line:
        card_class = 'border-danger'
        badge_class = 'bg-danger'
    elif '🟠' in line:
        card_class = 'border-warning'
        badge_class = 'bg-warning'
    else:
        card_class = 'border-info'
        badge_class = 'bg-info'
    
    html = f'<div class="card {card_class} mb-2"><div class="card-body">{line}</div></div>'
    return html, 0  # líneas consumidas
```

### ✅ Beneficios Aplicados

1. **Reutilización**: Estructura común para parseo
2. **Extensibilidad**: Fácil agregar nuevos tipos de línea
3. **Mantenibilidad**: Lógica de formateo centralizada

---

## 6. Facade Pattern

### 📝 Descripción
Proporciona una interfaz simplificada para un conjunto complejo de operaciones.

### 🎯 Propósito
- Simplificar operaciones complejas
- Ocultar complejidad interna
- Proveer API fácil de usar

### 📍 Ubicación
**Servicios de Negocio**: `apps/negocio/servicios/*.py`

### 💻 Implementación

```python
class DocenteService:
    """
    PATRÓN: Facade
    
    Simplifica operaciones complejas que involucran:
    - Repositorios
    - Servicios externos (IA)
    - State machine
    - Notificaciones
    """
    
    @staticmethod
    def validar_informe_con_ia(informe_id, docente, banco_especifico=None):
        """
        FACADE: Oculta la complejidad de:
        1. Obtener informe (Repository)
        2. Validar estado (State Machine)
        3. Obtener banco (Repository)
        4. Llamar IA (External Service)
        5. Persistir observaciones (Repository)
        6. Actualizar estado (State Machine)
        7. Notificar (Observer)
        
        El usuario solo llama un método simple
        """
        # ... implementación que coordina todo ...
```

### ✅ Dónde se Aplica

Cada servicio es una **Facade** que coordina:
- Repositorios
- State Machine
- APIs externas
- Notificaciones

---

## 7. Observer Pattern

### 📝 Descripción
Define una dependencia uno-a-muchos entre objetos, de manera que cuando un objeto cambia de estado, todos sus dependientes son notificados.

### 🎯 Propósito
- Notificar cambios de estado
- Desacoplar emisor de receptores
- Sistema de eventos

### 📍 Ubicación
**Archivo**: `backend/apps/notificaciones/services.py`

### 💻 Implementación

```python
class NotificacionService:
    """
    PATRÓN: Observer
    
    Observa eventos del sistema y notifica a usuarios
    """
    
    @staticmethod
    def crear_notificacion(usuario, tipo, titulo, mensaje, informe=None):
        """Método base para crear notificaciones"""
        return Notificacion.objects.create(
            usuario=usuario,
            tipo=tipo,
            titulo=titulo,
            mensaje=mensaje,
            informe=informe,
            leida=False
        )
    
    @staticmethod
    def notificar_informe_asignado(informe, docente):
        """
        OBSERVER: Reacciona al evento "informe asignado"
        """
        return NotificacionService.crear_notificacion(
            usuario=docente,
            tipo='asignacion_docente',
            titulo='Nuevo informe asignado',
            mensaje=f'Se le ha asignado el informe de {informe.usuario.nombre}',
            informe=informe
        )
    
    @staticmethod
    def notificar_dictamen_enviado(informe, presidente):
        """
        OBSERVER: Reacciona al evento "dictamen enviado"
        """
        return NotificacionService.crear_notificacion(
            usuario=presidente,
            tipo='dictamen_pendiente',
            titulo='Dictamen pendiente de aprobación',
            mensaje=f'El docente envió dictamen del informe de {informe.usuario.nombre}',
            informe=informe
        )
```

### 🔔 Eventos del Sistema

| Evento | Observadores Notificados |
|--------|-------------------------|
| Informe enviado | Secretaria |
| Informe derivado | Presidente |
| Docente asignado | Docente |
| Dictamen enviado | Presidente |
| Dictamen aprobado | Secretaria |
| Dictamen rechazado | Docente |
| Aprobación final | Estudiante |
| Rechazo final | Estudiante |

### ✅ Beneficios Aplicados

1. **Desacoplamiento**: Servicios no conocen las notificaciones
2. **Extensibilidad**: Fácil agregar nuevos tipos de notificación
3. **Centralización**: Toda la lógica de notificación en un lugar

---

## 8. Decorator Pattern

### 📝 Descripción
Añade funcionalidad a objetos de forma dinámica.

### 🎯 Propósito
- Autorización por rol
- Validación de sesión
- Logging y auditoría

### 📍 Ubicación
**Archivo**: `backend/apps/core/decorators.py`

### 💻 Implementación

```python
def requiere_rol(*roles_permitidos):
    """
    PATRÓN: Decorator
    
    Decora vistas para agregar autorización
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # FUNCIONALIDAD AÑADIDA: Validar sesión
            if 'usuario_id' not in request.session:
                messages.error(request, 'Debe iniciar sesión')
                return redirect('login')
            
            # FUNCIONALIDAD AÑADIDA: Validar rol
            tipo_usuario = request.session.get('usuario_tipo')
            if tipo_usuario not in roles_permitidos:
                messages.error(request, 'No tiene permisos')
                return redirect('login')
            
            # Ejecutar vista original
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator
```

### 📦 Uso en Vistas

```python
# apps/presentacion/web/docente_views.py

@requiere_rol('docente')
def panel_docente_view(request):
    """Vista decorada con autorización"""
    # ... lógica de la vista ...


@requiere_rol('presidente', 'secretaria')
def vista_compartida(request):
    """Permite múltiples roles"""
    # ... lógica de la vista ...
```

### ✅ Beneficios Aplicados

1. **Reutilización**: Mismo decorador en todas las vistas
2. **Declarativo**: Se ve claramente qué rol necesita
3. **DRY**: No repetir código de autorización

---

## 📊 Resumen de Patrones

| Patrón | Ubicación | Propósito | Beneficio Principal |
|--------|-----------|-----------|-------------------|
| **Repository** | `apps/datos/repositorios/` | Abstracción de BD | Independencia de ORM |
| **Service Layer** | `apps/negocio/servicios/` | Lógica de negocio | Reutilización y testing |
| **State Machine** | `apps/informes/state.py` | Gestión de estados | Seguridad en transiciones |
| **Strategy** | `apps/observaciones/services.py` | Selección de API IA | Flexibilidad |
| **Template Method** | `apps/core/templatetags/` | Formateo de dictámenes | Extensibilidad |
| **Facade** | Servicios de negocio | Simplificar complejidad | Usabilidad |
| **Observer** | `apps/notificaciones/` | Sistema de eventos | Desacoplamiento |
| **Decorator** | `apps/core/decorators.py` | Autorización | Declarativo |

---

## 🎓 Conclusión

El sistema implementa **8 patrones de diseño** de forma rigurosa:

✅ **Creacionales**: (Ninguno necesario)  
✅ **Estructurales**: Repository, Facade, Decorator  
✅ **Comportamentales**: State Machine, Strategy, Template Method, Observer, Service Layer

Cada patrón tiene:
- ✅ **Propósito claro**
- ✅ **Ubicación específica**
- ✅ **Implementación documentada**
- ✅ **Beneficios medibles**

---

**Ver también**: [Arquitectura](ARQUITECTURA.md), [Backend](BACKEND.md), [Flujo del Sistema](FLUJO_DEL_SISTEMA.md)
