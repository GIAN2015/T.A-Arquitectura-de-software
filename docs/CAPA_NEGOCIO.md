# CAPA DE NEGOCIO

Sistema de Validación de Informes - UNTELS

---

## ¿QUÉ ES LA CAPA DE NEGOCIO?

Es **la lógica de la aplicación**. Aquí se procesa todo:

- Validaciones
- Autenticación
- Procesamiento de archivos
- Llamadas a la IA
- Gestión de estados

**NO** contiene HTML ni SQL directo.

---

## ARCHIVOS DE ESTA CAPA

```
proyecto_untels/apps/
├── core/
│   ├── views.py                 # ← 7 vistas (184 líneas)
│   └── urls.py                  # ← 7 rutas
├── usuarios/
│   └── services.py              # ← UserService (41 líneas)
├── informes/
│   └── services.py              # ← DocumentService (15 líneas)
├── reglamento/
│   └── services.py              # ← RegulationService (7 líneas)
└── observaciones/
    └── services.py              # ← AIValidationService (59 líneas)
```

**Total:** 306 líneas de lógica de negocio

---

## 1. VISTAS (apps/core/views.py)

Las vistas son el **punto de entrada** desde la capa de presentación.

**Ubicación:** `/home/chapitec/Documents/chapitec/andre/T.A-Arquitectura-de-software/proyecto_untels/apps/core/views.py`

### Vista 1: login_view() [líneas 11-45]

**Propósito:** Autenticar usuarios

**Ruta:** `/`

**Lógica:**
```python
def login_view(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        password = request.POST.get('password')
        
        # OPCIÓN 1: Con contraseña (nuevo sistema)
        if password:
            usuario = autenticar_usuario(codigo, password)  # ← Llama a UserService
            if usuario:
                # Guardar en sesión
                request.session['usuario_id'] = usuario.id
                request.session['usuario_codigo'] = usuario.codigo
                request.session['usuario_nombre'] = usuario.nombre
                request.session['usuario_tipo'] = usuario.tipo_usuario
                return redirect('upload')
            else:
                messages.error(request, 'Código o contraseña incorrectos.')
        
        # OPCIÓN 2: Sin contraseña (modo legacy)
        else:
            nombre = request.POST.get('nombre')
            usuario = identificar_usuario(codigo, nombre)  # ← Llama a UserService
            # Guardar en sesión
            return redirect('upload')
    
    return render(request, 'login.html')
```

**Servicios que llama:**
- `autenticar_usuario()` → apps/usuarios/services.py
- `identificar_usuario()` → apps/usuarios/services.py

---

### Vista 2: registro_view() [líneas 47-75]

**Propósito:** Registrar nuevos usuarios

**Ruta:** `/registro/`

**Lógica:**
```python
def registro_view(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        tipo_usuario = request.POST.get('tipo_usuario')
        
        # VALIDACIONES
        if not all([codigo, nombre, password, password_confirm]):
            messages.error(request, 'Todos los campos son obligatorios.')
            return render(request, 'registro.html')
        
        if password != password_confirm:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'registro.html')
        
        if len(password) < 6:
            messages.error(request, 'La contraseña debe tener al menos 6 caracteres.')
            return render(request, 'registro.html')
        
        # REGISTRO
        usuario = registrar_usuario(codigo, nombre, password, tipo_usuario)  # ← UserService
        if usuario:
            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect('login')
        else:
            messages.error(request, 'El código ya está registrado.')
            return render(request, 'registro.html')
    
    return render(request, 'registro.html')
```

**Servicios que llama:**
- `registrar_usuario()` → apps/usuarios/services.py

---

### Vista 3: upload_view() [líneas 77-134] ⭐ PRINCIPAL

**Propósito:** Subir informe y validar con IA

**Ruta:** `/upload/`

**Requiere:** Usuario autenticado

**Lógica (FLUJO COMPLETO CON IA):**
```python
def upload_view(request):
    # 1. VERIFICAR AUTENTICACIÓN
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    # 2. PREPARAR CONTEXTO
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
    }
    
    if request.method == 'POST':
        archivo = request.FILES.get('informe')
        
        # 3. VALIDAR ARCHIVO
        if not archivo:
            messages.error(request, 'Por favor selecciona un archivo .docx o .pdf')
            return render(request, 'upload_report.html', context)
        
        if not archivo.name.endswith('.docx'):
            messages.error(request, 'Solo se permiten archivos .docx')
            return render(request, 'upload_report.html', context)
        
        try:
            # 4. OBTENER USUARIO
            from apps.usuarios.models import Usuario
            usuario = Usuario.objects.get(id=request.session['usuario_id'])
            
            # 5. EXTRAER CONTENIDO DEL .DOCX
            contenido = leer_archivo(archivo)  # ← DocumentService
            
            # 6. CREAR INFORME (ESTADO 1: ENVIADO)
            informe = Informe.objects.create(
                usuario=usuario,
                nombre_archivo=archivo.name,
                contenido=contenido,
                estado=Informe.ESTADO_ENVIADO,
            )
            
            # 7. CAMBIAR A ESTADO 2: EN REVISIÓN
            informe.estado = Informe.ESTADO_EN_REVISION
            informe.save()
            
            # 8. OBTENER REGLAMENTO Y BANCO DE OBSERVACIONES
            reglamento = obtener_reglamento()  # ← RegulationService
            observaciones_banco = obtener_observaciones()  # ← ObservationService
            
            # 9. VALIDAR CON IA (GROQ API - LLAMA 3.3 70B)
            resultado = validar_informe(contenido, reglamento, observaciones_banco)  # ← AIService
            
            # 10. GUARDAR OBSERVACIONES GENERADAS POR LA IA
            for obs in resultado:
                ObservacionGenerada.objects.create(
                    informe=informe,
                    seccion=obs.get('seccion', ''),
                    observacion=obs.get('observacion', ''),
                    ubicacion_error=obs.get('ubicacion', '')
                )
            
            # 11. CAMBIAR A ESTADO 3: COMPLETADO
            informe.estado = Informe.ESTADO_COMPLETADO
            informe.save()
            
            # 12. REDIRIGIR A RESULTADOS
            return redirect('resultado', informe_id=informe.id)
            
        except Exception as e:
            messages.error(request, f'Error al procesar el informe: {str(e)}')
            return render(request, 'upload_report.html', context)
    
    return render(request, 'upload_report.html', context)
```

**Servicios que llama:**
- `leer_archivo()` → apps/informes/services.py
- `obtener_reglamento()` → apps/reglamento/services.py
- `obtener_observaciones()` → apps/observaciones/services.py
- `validar_informe()` → apps/observaciones/services.py (IA)

**Flujo de estados:**
```
ENVIADO → EN_REVISION → COMPLETADO
```

---

### Vista 4: resultado_view() [líneas 136-144]

**Propósito:** Mostrar resultados de validación

**Ruta:** `/resultado/<informe_id>/`

**Lógica:**
```python
def resultado_view(request, informe_id):
    informe = get_object_or_404(Informe, id=informe_id)
    observaciones = ObservacionGenerada.objects.filter(informe=informe)
    
    context = {
        'informe': informe,
        'observaciones': observaciones,
        'usuario': informe.usuario,
    }
    return render(request, 'validation_result.html', context)
```

**Modelos que usa:**
- `Informe`
- `ObservacionGenerada`

---

### Vista 5: historial_view() [líneas 146-160]

**Propósito:** Ver historial de informes del usuario

**Ruta:** `/historial/`

**Requiere:** Usuario autenticado

**Lógica:**
```python
def historial_view(request):
    # 1. VERIFICAR AUTENTICACIÓN
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    # 2. OBTENER USUARIO Y SUS INFORMES
    from apps.usuarios.models import Usuario
    usuario = Usuario.objects.get(id=request.session['usuario_id'])
    informes = Informe.objects.filter(usuario=usuario).order_by('-fecha_registro')
    
    # 3. PREPARAR CONTEXTO
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'informes': informes,
    }
    return render(request, 'historial.html', context)
```

**Modelos que usa:**
- `Usuario`
- `Informe` (filtrado por usuario)

---

### Vista 6: panel_docente_view() [líneas 162-179]

**Propósito:** Panel administrativo para docentes

**Ruta:** `/panel-docente/`

**Requiere:** Usuario autenticado Y tipo = 'docente'

**Lógica:**
```python
def panel_docente_view(request):
    # 1. VERIFICAR AUTENTICACIÓN
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    # 2. VERIFICAR ROL DE DOCENTE
    if request.session.get('usuario_tipo') != 'docente':
        messages.error(request, 'Acceso denegado. Solo docentes pueden acceder a este panel.')
        return redirect('upload')
    
    # 3. OBTENER TODOS LOS INFORMES (DE TODOS LOS USUARIOS)
    informes = Informe.objects.all().select_related('usuario').order_by('-fecha_registro')
    
    # 4. PREPARAR CONTEXTO
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'informes': informes,
    }
    return render(request, 'panel_docente.html', context)
```

**Características:**
- Control de acceso por rol
- Query optimizado con `select_related('usuario')` para evitar N+1 queries
- Vista de TODOS los informes del sistema

---

### Vista 7: logout_view() [líneas 181-184]

**Propósito:** Cerrar sesión

**Ruta:** `/logout/`

**Lógica:**
```python
def logout_view(request):
    request.session.flush()  # Limpia toda la sesión
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('login')
```

---

## 2. RUTAS (apps/core/urls.py)

**Ubicación:** `/home/chapitec/Documents/chapitec/andre/T.A-Arquitectura-de-software/proyecto_untels/apps/core/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('upload/', views.upload_view, name='upload'),
    path('resultado/<int:informe_id>/', views.resultado_view, name='resultado'),
    path('historial/', views.historial_view, name='historial'),
    path('panel-docente/', views.panel_docente_view, name='panel_docente'),
    path('logout/', views.logout_view, name='logout'),
]
```

**7 rutas definidas**

---

## 3. SERVICIOS

Los servicios contienen **lógica reutilizable** que NO depende del request HTTP.

### 3.1 UserService (apps/usuarios/services.py)

**Ubicación:** `/home/chapitec/Documents/chapitec/andre/T.A-Arquitectura-de-software/proyecto_untels/apps/usuarios/services.py`

**41 líneas, 3 funciones**

#### Función 1: identificar_usuario()

**Propósito:** Modo legacy sin contraseña

```python
def identificar_usuario(codigo: str, nombre: str) -> Usuario:
    """Para compatibilidad con el sistema anterior (sin contraseña)"""
    try:
        year = int(codigo[:4])
        tipo = 'egresado' if year < 2020 else 'estudiante'
    except (ValueError, IndexError):
        tipo = 'estudiante'

    usuario, _ = Usuario.objects.get_or_create(
        codigo=codigo,
        defaults={'nombre': nombre, 'tipo_usuario': tipo}
    )
    usuario.nombre = nombre
    usuario.tipo_usuario = tipo
    usuario.save()
    return usuario
```

**Lógica:**
- Si código < 2020 → Egresado
- Si código >= 2020 → Estudiante
- Si existe usuario, actualiza nombre y tipo
- Si no existe, lo crea

---

#### Función 2: autenticar_usuario()

**Propósito:** Autenticación con contraseña

```python
def autenticar_usuario(codigo: str, password: str):
    """Autentica un usuario con contraseña"""
    try:
        usuario = Usuario.objects.get(codigo=codigo)
        if usuario.check_password(password):  # ← Verificación segura
            return usuario
        return None
    except Usuario.DoesNotExist:
        return None
```

**Lógica:**
- Busca usuario por código
- Verifica contraseña con hash (timing-safe)
- Retorna usuario si OK, None si falla

---

#### Función 3: registrar_usuario()

**Propósito:** Registrar nuevo usuario con contraseña

```python
def registrar_usuario(codigo: str, nombre: str, password: str, tipo_usuario: str = 'estudiante'):
    """Registra un nuevo usuario con contraseña"""
    if Usuario.objects.filter(codigo=codigo).exists():
        return None  # Ya existe
    
    usuario = Usuario.objects.create(
        codigo=codigo,
        nombre=nombre,
        tipo_usuario=tipo_usuario
    )
    usuario.set_password(password)  # ← Encriptación automática
    return usuario
```

**Lógica:**
- Verifica que código no esté duplicado
- Crea usuario
- Encripta contraseña con `set_password()` (usa bcrypt/PBKDF2)
- Retorna usuario creado o None si ya existe

---

### 3.2 DocumentService (apps/informes/services.py)

**Ubicación:** `/home/chapitec/Documents/chapitec/andre/T.A-Arquitectura-de-software/proyecto_untels/apps/informes/services.py`

**15 líneas, 2 funciones**

#### Función 1: leer_archivo()

**Propósito:** Leer archivo .docx o .pdf desde memoria

```python
from docx import Document

def leer_archivo(archivo):
    """Lee un archivo .docx o .pdf y extrae su contenido"""
    doc = Document(archivo)  # Lee desde InMemoryUploadedFile
    return extraer_contenido(doc)
```

**Entrada:** `InMemoryUploadedFile` (Django file upload)

**Salida:** String con texto completo

---

#### Función 2: extraer_contenido()

**Propósito:** Extraer texto de documento Word

```python
def extraer_contenido(doc):
    """Extrae el texto de un documento de Word"""
    parrafos = [p.text for p in doc.paragraphs]
    return '\n'.join(parrafos)
```

**Lógica:**
- Itera todos los párrafos del documento
- Une con saltos de línea
- Retorna texto plano

---

### 3.3 RegulationService (apps/reglamento/services.py)

**Ubicación:** `/home/chapitec/Documents/chapitec/andre/T.A-Arquitectura-de-software/proyecto_untels/apps/reglamento/services.py`

**7 líneas, 1 función**

#### Función: obtener_reglamento()

```python
from .models import Reglamento

def obtener_reglamento():
    """Obtiene el reglamento activo"""
    reglamento = Reglamento.objects.filter(activo=True).first()
    if reglamento:
        return reglamento.contenido
    return "Reglamento no disponible."
```

**Lógica:**
- Busca reglamento con `activo=True`
- Retorna contenido si existe
- Retorna texto por defecto si no hay reglamento

---

### 3.4 ObservationService (apps/observaciones/services.py)

**Ubicación:** `/home/chapitec/Documents/chapitec/andre/T.A-Arquitectura-de-software/proyecto_untels/apps/observaciones/services.py`

**59 líneas, 2 funciones**

#### Función 1: obtener_observaciones()

```python
from .models import BancoObservaciones

def obtener_observaciones():
    """Obtiene todas las observaciones del banco"""
    observaciones = BancoObservaciones.objects.all()
    resultado = []
    for obs in observaciones:
        resultado.append(f"- {obs.seccion}: {obs.descripcion}")
    return '\n'.join(resultado)
```

**Lógica:**
- Obtiene todas las observaciones frecuentes de la BD
- Formatea como lista de texto
- Retorna string para incluir en prompt de IA

---

#### Función 2: validar_informe() ⭐ IA

**Propósito:** Validar informe con IA (Groq API - LLaMA 3.3 70B)

```python
import requests
import json
import re
from django.conf import settings

def validar_informe(contenido, reglamento, observaciones_banco):
    """Valida un informe usando IA (Groq API con LLaMA 3.3 70B)"""
    
    GROQ_API_KEY = settings.GROQ_API_KEY
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    # PROMPT ENGINEERING
    prompt = f"""Eres un evaluador académico experto en prácticas preprofesionales.

Tu tarea es analizar un informe de prácticas preprofesionales de la UNTELS (Universidad Nacional Tecnológica de Lima Sur).

INFORME A EVALUAR:
{contenido[:3000]}

REGLAMENTO INSTITUCIONAL UNTELS:
{reglamento[:2000]}

OBSERVACIONES FRECUENTES DETECTADAS ANTERIORMENTE:
{observaciones_banco[:1000]}

INSTRUCCIONES:
1. Analiza cada sección del informe (introducción, objetivos, desarrollo, conclusiones, etc.)
2. Compara el contenido con el reglamento institucional
3. Identifica errores, omisiones, inconsistencias o áreas de mejora
4. Para cada observación, especifica:
   - La sección donde se encuentra el problema
   - Una descripción clara de la observación
   - La ubicación específica dentro de esa sección

IMPORTANTE: Devuelve únicamente un array JSON válido con las observaciones.

FORMATO DE SALIDA (JSON válido):
[
  {{
    "id": 1,
    "seccion": "Introducción",
    "observacion": "Descripción de la observación",
    "ubicacion": "Ubicación específica del error"
  }}
]

Si el informe está correcto o no hay observaciones, devuelve un array vacío: []
"""

    # LLAMADA A GROQ API
    try:
        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",  # Modelo de 70B parámetros
                "messages": [
                    {
                        "role": "system",
                        "content": "Eres un evaluador académico experto..."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.3,  # Baja temperatura = respuestas consistentes
                "max_tokens": 2000,
                "top_p": 0.9
            },
            timeout=60  # Timeout de 60 segundos
        )
        
        # PARSEAR RESPUESTA
        data = response.json()
        content = data['choices'][0]['message']['content'].strip()
        
        # EXTRAER JSON de la respuesta (puede venir con texto adicional)
        json_match = re.search(r'\[.*\]', content, re.DOTALL)
        if json_match:
            observaciones = json.loads(json_match.group())
            return observaciones
        
        return []
        
    except Exception as e:
        print(f"Error en validación con IA: {str(e)}")
        return []
```

**Características:**
- **API:** Groq (inferencia ultra-rápida)
- **Modelo:** LLaMA 3.3 70B (70 mil millones de parámetros)
- **Temperature:** 0.3 (respuestas consistentes)
- **Max tokens:** 2000
- **Timeout:** 60 segundos
- **Prompt engineering:** Detallado con contexto académico
- **Parsing robusto:** Regex para extraer JSON
- **Error handling:** Try/except con fallback a array vacío
- **Truncado:** Limita contenido para no exceder tokens

**Entrada:**
- `contenido`: Texto del informe (hasta 3000 chars)
- `reglamento`: Reglamento UNTELS (hasta 2000 chars)
- `observaciones_banco`: Observaciones frecuentes (hasta 1000 chars)

**Salida:**
```json
[
  {
    "id": 1,
    "seccion": "Introducción",
    "observacion": "Falta objetivo general",
    "ubicacion": "Introducción"
  },
  {
    "id": 2,
    "seccion": "Desarrollo",
    "observacion": "No menciona competencias adquiridas",
    "ubicacion": "Capítulo 2"
  }
]
```

---

## 4. FLUJO COMPLETO DE UNA VALIDACIÓN

```
1. Usuario hace login
   ↓
   login_view() → autenticar_usuario()
   
2. Usuario sube informe.docx
   ↓
   upload_view() recibe archivo
   
3. Extraer contenido del .docx
   ↓
   leer_archivo() → extraer_contenido()
   
4. Crear registro en BD (ESTADO: ENVIADO)
   ↓
   Informe.objects.create()
   
5. Cambiar estado a EN_REVISION
   ↓
   informe.estado = ESTADO_EN_REVISION
   
6. Obtener reglamento y observaciones
   ↓
   obtener_reglamento()
   obtener_observaciones()
   
7. Llamar a IA para validar
   ↓
   validar_informe() → Groq API (LLaMA 3.3 70B)
   
8. Guardar observaciones de la IA
   ↓
   ObservacionGenerada.objects.create() (loop)
   
9. Cambiar estado a COMPLETADO
   ↓
   informe.estado = ESTADO_COMPLETADO
   
10. Mostrar resultados
    ↓
    redirect → resultado_view()
```

---

## 5. GESTIÓN DE SESIONES

**Las vistas usan sesiones de Django para mantener estado:**

```python
# GUARDAR en sesión (login)
request.session['usuario_id'] = usuario.id
request.session['usuario_codigo'] = usuario.codigo
request.session['usuario_nombre'] = usuario.nombre
request.session['usuario_tipo'] = usuario.tipo_usuario

# LEER de sesión (otras vistas)
if 'usuario_id' not in request.session:
    return redirect('login')

usuario_tipo = request.session.get('usuario_tipo')

# LIMPIAR sesión (logout)
request.session.flush()
```

---

## RESUMEN

| Componente | Archivos | Funciones/Vistas | Líneas |
|------------|----------|------------------|--------|
| **Vistas** | apps/core/views.py | 7 vistas | 184 |
| **URLs** | apps/core/urls.py | 7 rutas | 8 |
| **UserService** | apps/usuarios/services.py | 3 funciones | 41 |
| **DocumentService** | apps/informes/services.py | 2 funciones | 15 |
| **RegulationService** | apps/reglamento/services.py | 1 función | 7 |
| **ObservationService** | apps/observaciones/services.py | 2 funciones | 59 |
| **TOTAL** | 6 archivos | 15 funciones | **314 líneas** |

---

**Esta es la CAPA DE NEGOCIO completa.**

**Siguiente:** Lee `CAPA_DATOS.md` para entender los modelos y base de datos.
