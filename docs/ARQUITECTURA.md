# 📐 Arquitectura del Sistema

> Documentación completa de la arquitectura del Sistema de Validación de Informes UNTELS

---

## 📋 Tabla de Contenidos

1. [Visión General](#visión-general)
2. [Clean Architecture](#clean-architecture)
3. [Capas del Sistema](#capas-del-sistema)
4. [Principios SOLID](#principios-solid)
5. [Separación de Responsabilidades](#separación-de-responsabilidades)
6. [Flujo de Datos](#flujo-de-datos)

---

## 🎯 Visión General

El sistema está construido siguiendo los principios de **Clean Architecture** (Arquitectura Limpia) propuesta por Robert C. Martin (Uncle Bob), con una separación clara de responsabilidades en capas concéntricas.

### Objetivos Arquitectónicos

✅ **Independencia de Frameworks**: La lógica de negocio no depende de Django  
✅ **Testeable**: Cada capa puede probarse independientemente  
✅ **Independencia de UI**: El frontend puede cambiar sin afectar la lógica  
✅ **Independencia de Base de Datos**: Fácil migración a PostgreSQL/MySQL  
✅ **Mantenible**: Código organizado y fácil de entender

---

## 🏛️ Clean Architecture

### Diagrama de Capas

```
┌─────────────────────────────────────────────────────────────┐
│                        🌐 FRONTEND                          │
│          (Templates Django + Bootstrap + JS)                │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                  📱 CAPA DE PRESENTACIÓN                    │
│              (apps/presentacion/web/*_views.py)             │
│                                                              │
│  • EstudianteViews    • DocenteViews                       │
│  • PresidenteViews    • SecretariaViews                    │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                   💼 CAPA DE NEGOCIO                        │
│               (apps/negocio/servicios/*.py)                 │
│                                                              │
│  • EstudianteService  • DocenteService                     │
│  • PresidenteService  • SecretariaService                  │
│  • NotificacionService                                      │
│                                                              │
│  ⭐ CONTIENE TODA LA LÓGICA DE NEGOCIO                     │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                   🗄️ CAPA DE DATOS                         │
│             (apps/datos/repositorios/*.py)                  │
│                                                              │
│  • UsuarioRepository  • InformeRepository                  │
│  • ObservacionRepository  • ReglamentoRepository          │
│                                                              │
│  ⭐ PATRÓN REPOSITORY - Abstracción de BD                  │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                     💾 MODELOS ORM                          │
│                    (apps/*/models.py)                       │
│                                                              │
│  • Usuario    • Informe    • Observacion                   │
│  • Escuela    • Notificacion                               │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                    🗃️ BASE DE DATOS                        │
│                    (SQLite / PostgreSQL)                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 📚 Capas del Sistema

### 1. **Capa de Presentación** (Presentation Layer)

**Ubicación**: `backend/apps/presentacion/web/`

**Responsabilidad**: Manejar las peticiones HTTP y renderizar las vistas

```python
# Ejemplo: apps/presentacion/web/docente_views.py
@requiere_rol('docente')
def panel_docente_view(request):
    """Vista del dashboard del docente"""
    docente = Usuario.objects.get(id=request.session['usuario_id'])
    
    # Delegar la lógica al servicio
    informes = DocenteService.obtener_informes_asignados(docente)
    stats = DocenteService.obtener_estadisticas(docente)
    
    return render(request, 'docente/dashboard.html', {
        'informes': informes,
        'stats': stats
    })
```

**Características**:
- ✅ NO contiene lógica de negocio
- ✅ Solo valida formularios y datos de entrada
- ✅ Delega todo a la capa de servicios
- ✅ Renderiza templates o devuelve JSON

---

### 2. **Capa de Negocio** (Business Logic Layer)

**Ubicación**: `backend/apps/negocio/servicios/`

**Responsabilidad**: Toda la lógica de negocio del sistema

```python
# Ejemplo: apps/negocio/servicios/docente.py
class DocenteService:
    """Servicio de negocio para operaciones de docentes"""
    
    @staticmethod
    def validar_informe_con_ia(informe_id, docente, banco_especifico=None):
        """
        Valida un informe usando IA con el banco de observaciones
        
        LÓGICA DE NEGOCIO:
        1. Verificar que el informe esté en estado correcto
        2. Obtener banco de observaciones
        3. Llamar a la API de IA
        4. Procesar respuesta y crear observaciones
        5. Actualizar estado del informe
        """
        # ... lógica completa ...
        return True, observaciones, None
```

**Características**:
- ✅ Contiene TODA la lógica de negocio
- ✅ Métodos estáticos (stateless)
- ✅ Retorna tuplas `(success, data, error)`
- ✅ Independiente del framework
- ✅ Fácilmente testeable

**Servicios Implementados**:

| Servicio | Archivo | Responsabilidad |
|----------|---------|-----------------|
| `DocenteService` | `docente.py` | Gestión de banco, validación IA, dictámenes |
| `PresidenteService` | `presidente.py` | Asignación de docentes, aprobación/rechazo |
| `SecretariaService` | `secretaria.py` | Derivación, notificaciones finales |
| `NotificacionService` | `apps/notificaciones/services.py` | Sistema de notificaciones |

---

### 3. **Capa de Datos** (Data Access Layer)

**Ubicación**: `backend/apps/datos/repositorios/`

**Responsabilidad**: Abstracción del acceso a la base de datos

```python
# Ejemplo: apps/datos/repositorios/informes.py
class InformeRepository:
    """Repositorio para acceso a datos de Informes"""
    
    @staticmethod
    def obtener_por_estado(estado, limit=None):
        """Obtiene informes filtrados por estado"""
        query = Informe.objects.filter(estado=estado)
        if limit:
            query = query[:limit]
        return query.select_related('usuario', 'escuela')
    
    @staticmethod
    def obtener_con_observaciones(informe_id):
        """Obtiene informe con observaciones precargadas"""
        return Informe.objects.prefetch_related(
            'observaciones'
        ).get(id=informe_id)
```

**Características**:
- ✅ **Patrón Repository**: Abstrae el ORM
- ✅ Queries optimizadas con `select_related` y `prefetch_related`
- ✅ Fácil cambio de ORM o BD
- ✅ Centraliza acceso a datos

---

### 4. **Capa de Modelos** (Domain Models)

**Ubicación**: `backend/apps/*/models.py`

**Responsabilidad**: Representar las entidades del dominio

```python
# Ejemplo: apps/informes/models.py
class Informe(models.Model):
    """Modelo de dominio: Informe de práctica preprofesional"""
    
    # Estados del flujo
    ESTADO_ENVIADO = 'enviado'
    ESTADO_VALIDANDO_IA = 'validando_ia'
    # ... más estados
    
    # Campos
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES)
    
    # Métodos de dominio
    def transition_to(self, next_state):
        """Transición de estado usando State Machine"""
        state = get_state(self.estado)
        state.transition(self, next_state)
```

**Características**:
- ✅ Representan conceptos del negocio
- ✅ Contienen reglas de dominio
- ✅ Validaciones de integridad
- ✅ Métodos de comportamiento

---

## 🔷 Principios SOLID

### 1. **S - Single Responsibility Principle**

Cada clase tiene una única responsabilidad:

```python
# ✅ CORRECTO: Cada servicio tiene una responsabilidad
class DocenteService:
    """Solo operaciones de docentes"""
    pass

class PresidenteService:
    """Solo operaciones de presidentes"""
    pass

# ❌ INCORRECTO: Un servicio que hace todo
class MegaService:
    """Hace docentes, presidentes, secretarias..."""
    pass
```

### 2. **O - Open/Closed Principle**

Abierto para extensión, cerrado para modificación:

```python
# ✅ CORRECTO: Strategy Pattern para APIs de IA
def validar_con_api(contenido, banco):
    if GROQ_API_KEY.startswith('xai-'):
        return validar_con_xai(contenido, banco)
    elif GROQ_API_KEY.startswith('gsk_'):
        return validar_con_groq(contenido, banco)
    else:
        return validacion_local(contenido, banco)
```

### 3. **L - Liskov Substitution Principle**

Los objetos deben ser reemplazables por instancias de sus subtipos:

```python
# ✅ CORRECTO: State Machine con polimorfismo
class BaseInformeState:
    def transition(self, informe, next_state):
        if not self.can_transition_to(next_state):
            raise InformeStateError(...)
        informe.estado = next_state

# Todas las clases hijas pueden reemplazar a la base
class EnviadoState(BaseInformeState):
    allowed_transitions = {'pendiente_secretaria'}
```

### 4. **I - Interface Segregation Principle**

Interfaces específicas en lugar de generales:

```python
# ✅ CORRECTO: Servicios específicos por rol
class DocenteService:
    obtener_informes_asignados()
    validar_informe_con_ia()
    enviar_dictamen_a_presidente()

class PresidenteService:
    obtener_informes_pendientes()
    asignar_docente()
    aprobar_dictamen()
```

### 5. **D - Dependency Inversion Principle**

Depender de abstracciones, no de concreciones:

```python
# ✅ CORRECTO: Servicios no dependen de vistas
# Vistas dependen de servicios (abstracción)

def panel_docente_view(request):
    # La vista depende del servicio (abstracción)
    informes = DocenteService.obtener_informes_asignados(docente)
    # NO hace: Informe.objects.filter(...) directamente
```

---

## 🔀 Separación de Responsabilidades

### Estructura de Directorios

```
apps/
├── core/                   # Núcleo compartido
│   ├── decorators.py      # @requiere_rol
│   ├── admin_views.py     # Vistas admin
│   └── templatetags/      # Filtros custom
│
├── usuarios/              # Dominio: Usuarios
│   ├── models.py         # Usuario (modelo)
│   └── ...
│
├── informes/              # Dominio: Informes
│   ├── models.py         # Informe (modelo)
│   ├── state.py          # State Machine
│   └── ...
│
├── observaciones/         # Dominio: Observaciones
│   ├── models.py         # ObservacionGenerada, BancoObservaciones
│   ├── services.py       # Validación con IA
│   └── ...
│
├── negocio/              # ⭐ LÓGICA DE NEGOCIO
│   └── servicios/
│       ├── docente.py
│       ├── presidente.py
│       ├── secretaria.py
│       └── estudiante.py
│
├── datos/                # ⭐ ACCESO A DATOS
│   └── repositorios/
│       ├── informes.py
│       ├── usuarios.py
│       └── observaciones.py
│
└── presentacion/         # ⭐ CAPA DE PRESENTACIÓN
    └── web/
        ├── estudiante_views.py
        ├── docente_views.py
        ├── presidente_views.py
        └── secretaria_views.py
```

---

## 📊 Flujo de Datos

### Ejemplo Completo: Validar Informe con IA

```
1. Usuario hace clic en "Validar con IA"
   ↓
2. 🌐 FRONTEND: Envía POST a /docente/revisar/123/
   ↓
3. 📱 PRESENTACIÓN: docente_views.py::docente_revisar_informe()
   - Valida sesión y rol
   - Extrae parámetros del request
   ↓
4. 💼 NEGOCIO: DocenteService.validar_informe_con_ia(123, docente, banco)
   - Verifica estado del informe
   - Obtiene banco de observaciones
   - Llama a validar_con_groq()
   ↓
5. 🤖 SERVICIOS: validar_con_groq(informe, banco)
   - Construye prompt
   - Llama API de IA
   - Parsea respuesta JSON
   ↓
6. 🗄️ DATOS: InformeRepository.actualizar_estado(123, 'validando_ia')
   - Ejecuta query
   - Actualiza BD
   ↓
7. 💾 BASE DE DATOS: UPDATE informes SET estado='validando_ia' ...
   ↓
8. ⬅️ Respuesta sube por las capas
   ↓
9. 📱 PRESENTACIÓN: Renderiza template con resultados
   ↓
10. 🌐 FRONTEND: Usuario ve las observaciones generadas
```

---

## ✅ Ventajas de Esta Arquitectura

### 1. **Testabilidad**

```python
# Test unitario de servicio (sin BD, sin Django)
def test_validar_informe():
    # Mock del informe
    informe_mock = Mock()
    informe_mock.contenido = "Texto de prueba"
    
    # Test del servicio
    success, obs, error = DocenteService.validar_informe_con_ia(
        informe_id=1,
        docente=Mock(),
        banco_especifico=Mock()
    )
    
    assert success == True
    assert len(obs) > 0
```

### 2. **Mantenibilidad**

- ✅ Cambios en UI no afectan la lógica
- ✅ Cambios en BD no afectan los servicios
- ✅ Fácil encontrar dónde está cada cosa

### 3. **Escalabilidad**

- ✅ Fácil agregar nuevos roles
- ✅ Fácil agregar nuevas APIs de IA
- ✅ Servicios pueden convertirse en microservicios

### 4. **Reutilización**

```python
# El mismo servicio puede usarse desde:
# - Vistas web (Django views)
# - API REST (Django REST Framework)
# - Comandos de management (manage.py commands)
# - Tasks asíncronos (Celery)
# - CLI (Command Line Interface)
```

---

## 🎓 Conclusión

El Sistema de Validación de Informes UNTELS implementa **Clean Architecture** de forma rigurosa, separando claramente:

- ✅ **Presentación**: Manejo de HTTP y templates
- ✅ **Negocio**: Lógica de dominio
- ✅ **Datos**: Acceso a BD

Esto resulta en un sistema:
- 🎯 Fácil de entender
- 🧪 Fácil de probar
- 🔧 Fácil de mantener
- 🚀 Fácil de escalar

---

**Siguiente**: [Backend](BACKEND.md) →
