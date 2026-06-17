# Sistema de Validación de Informes PPP - UNTELS

## Sistema COMPLETAMENTE SEPARADO: Alumnos vs Docentes

---

## 1. PORTAL DE ESTUDIANTES

### Login Estudiantes
**URL:** http://127.0.0.1:8000/

```
┌─────────────────────────────────┐
│  🎓 Portal Estudiantes          │
├─────────────────────────────────┤
│  Código: 2021101234             │
│  Contraseña: estudiante123      │
│                                 │
│  [Iniciar Sesión]               │
│                                 │
│  ¿Eres docente? → Accede aquí   │
└─────────────────────────────────┘
```

### Funciones del Estudiante

1. **Subir Informe** → `/upload/`
   - Selecciona archivo .docx
   - Sistema extrae contenido
   - **IA VALIDA AUTOMÁTICAMENTE**
   - Genera observaciones

2. **Ver Resultados** → `/resultado/<id>/`
   - Observaciones de la IA
   - Estado del informe
   - Comentarios del docente (si ya revisó)

3. **Historial** → `/historial/`
   - Todos los informes enviados
   - Versiones anteriores
   - Estados actuales

---

## 2. PORTAL DE DOCENTES

### Login Docentes
**URL:** http://127.0.0.1:8000/docente/login/

```
┌─────────────────────────────────┐
│  👨‍🏫 Portal Docente              │
├─────────────────────────────────┤
│  Código: DOCENTE001             │
│  Contraseña: docente123         │
│                                 │
│  [Iniciar Sesión]               │
│                                 │
│  ¿Eres estudiante? → Inicia aquí│
└─────────────────────────────────┘
```

### Funciones del Docente

1. **Panel Principal** → `/panel-docente/`
   - Lista TODOS los informes de alumnos
   - Filtros por estado
   - Acceso rápido a revisión

2. **Revisar Informe** → `/docente/revisar/<id>/`
   - Ver observaciones generadas por IA
   - **CONFIRMAR o DESCARTAR** cada observación
   - Añadir comentarios
   - Cambiar severidad
   - **APROBAR o RECHAZAR** el informe

3. **Gestión del Sistema** → `/admin/...`
   - Dashboard con estadísticas
   - Gestionar usuarios
   - Actualizar reglamento
   - Editar banco de observaciones
   - Ver reportes

---

## 3. INTEGRACIÓN CON IA (GROQ)

### ¿Dónde está la IA?

**Archivo:** `apps/observaciones/services.py:14`

**Función:** `validar_informe(contenido, reglamento, observaciones)`

### ¿Cómo funciona?

```python
def validar_informe(contenido_informe, reglamento, observaciones):
    # 1. Construye prompt para la IA
    prompt = f"""
    Eres evaluador académico de UNTELS.
    
    REGLAMENTO:
    {reglamento}
    
    BANCO DE OBSERVACIONES:
    {observaciones}
    
    INFORME:
    {contenido_informe}
    
    Devuelve JSON con observaciones encontradas.
    """
    
    # 2. Llama a GROQ API
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    
    # 3. Retorna observaciones en formato JSON
    return json.loads(response.json()["choices"][0]["message"]["content"])
```

### ¿Cuándo se ejecuta?

**Cuando el estudiante sube un informe:**

```
apps/core/views.py:96-127

1. Alumno sube archivo .docx
2. Sistema extrae contenido
3. Obtiene reglamento activo
4. Obtiene banco de observaciones
5. ✨ LLAMA A LA IA: validar_informe()
6. IA retorna lista de observaciones
7. Sistema guarda observaciones en BD
8. Cambia estado a "Observado"
```

---

## 4. FLUJO COMPLETO DEL SISTEMA

```
┌─────────────────────────────────────────────────────┐
│                    FLUJO COMPLETO                   │
└─────────────────────────────────────────────────────┘

1. ALUMNO SUBE INFORME (.docx)
   ↓
   apps/core/views.py:upload_view()
   ↓
   Estado: ENVIADO

2. SISTEMA PROCESA ARCHIVO
   ↓
   apps/informes/services.py:leer_archivo()
   ↓
   Extrae texto completo del .docx
   ↓
   Estado: VALIDANDO

3. IA VALIDA CONTENIDO
   ↓
   apps/observaciones/services.py:validar_informe()
   ↓
   - Obtiene reglamento activo
   - Obtiene banco de observaciones
   - Envía a GROQ API (Llama 3.3 70B)
   - IA analiza y genera observaciones
   ↓
   Estado: OBSERVADO (si hay obs) o COMPLETADO (si no hay)

4. DOCENTE REVISA
   ↓
   apps/core/admin_views.py:admin_revisar_informe()
   ↓
   - Ve observaciones de la IA
   - Confirma/descarta cada una
   - Añade comentarios
   - Define severidad
   ↓
   Estado: EN_REVISION_DOCENTE

5. DECISIÓN DOCENTE
   ↓
   Si APRUEBA → Estado: APROBADO ✓
   Si RECHAZA → Estado: RECHAZADO
   ↓
   Alumno ve resultado

6. SI FUE RECHAZADO
   ↓
   Alumno corrige y REENVÍA
   ↓
   Se crea nueva versión
   ↓
   Vuelve al paso 2
```

---

## 5. CONFIGURACIÓN DE LA IA

### Obtener API Key de GROQ (GRATIS)

1. Ve a https://console.groq.com/
2. Crea cuenta (GitHub/Google)
3. Click en "API Keys"
4. Click "Create API Key"
5. Copia la clave

### Configurar en el sistema

Edita `.env`:

```env
GROQ_API_KEY=gsk_tu_clave_aqui_123456789
```

**¡IMPORTANTE!** Sin esta clave, la IA NO funcionará y mostrará error al subir informes.

---

## 6. DATOS YA CONFIGURADOS

### Reglamento Activo ✓
- Estructura del informe
- Formato y presentación
- Contenido académico
- Requisitos específicos

### Banco de Observaciones ✓
10 observaciones frecuentes:
- Carátula incompleta
- Formato incorrecto
- Índice sin páginas
- Introducción breve
- Actividades generales
- Conclusiones débiles
- Faltan anexos
- Errores ortográficos
- etc.

### Usuarios de Prueba ✓

**Estudiante:**
- Código: 2021101234
- Password: estudiante123

**Docente:**
- Código: DOCENTE001
- Password: docente123

---

## 7. ARQUITECTURA TÉCNICA

### Clean Architecture - Separación por Capas

```
┌──────────────────────────────────────┐
│         CAPA DE PRESENTACIÓN         │
│  templates/ + apps/core/views.py     │
│  (Vistas para alumnos y docentes)    │
└──────────────────────────────────────┘
                 ↓
┌──────────────────────────────────────┐
│         CAPA DE SERVICIOS            │
│  apps/*/services.py                  │
│  (Lógica de negocio + IA)            │
└──────────────────────────────────────┘
                 ↓
┌──────────────────────────────────────┐
│         CAPA DE DATOS                │
│  apps/*/models.py                    │
│  (Modelos de BD)                     │
└──────────────────────────────────────┘
```

### Modelos Principales

```python
Usuario
├── codigo (único)
├── nombre
├── tipo_usuario (estudiante/egresado/docente)
└── password (hasheado)

Informe
├── usuario (FK)
├── nombre_archivo
├── contenido (texto extraído)
├── estado (enviado/validando/observado/...)
├── docente_revisor (FK)
├── version
└── informe_anterior (FK - versionado)

ObservacionGenerada
├── informe (FK)
├── seccion
├── observacion
├── ubicacion_error
├── estado (pendiente/confirmada/descartada)
├── severidad (critica/importante/menor/sugerencia)
└── comentario_docente

BancoObservaciones
├── seccion
└── descripcion

Reglamento
├── nombre
├── contenido
└── activo (boolean)
```

---

## 8. COMANDOS ÚTILES

### Iniciar el servidor
```bash
cd proyecto_untels
source venv/bin/activate
python manage.py runserver
```

### Ver logs en vivo
```bash
# Terminal abierta con runserver muestra todos los requests
```

### Crear nuevo docente
```bash
python manage.py shell -c "
from apps.usuarios.models import Usuario
d = Usuario.objects.create(codigo='DOCENTE002', nombre='Ana Torres', tipo_usuario='docente')
d.set_password('password123')
print('✓ Docente creado')
"
```

### Verificar sistema
```bash
python manage.py check
```

---

## 9. IMPORTANTE - DIFERENCIAS CLAVE

### ❌ ANTES (Problema)
- Un solo login para todos
- Modo sin contraseña (inseguro)
- Alumnos y docentes veían lo mismo
- Confusión de roles

### ✅ AHORA (Solución)
- **DOS logins separados:**
  - `/` → Portal Estudiantes
  - `/docente/login/` → Portal Docentes
- **Contraseña obligatoria** para todos
- **Funciones completamente separadas:**
  - Alumno: Sube, ve resultados, historial
  - Docente: Revisa, aprueba/rechaza, gestiona sistema
- **Validación de roles:** No puedes entrar donde no corresponde

---

## 10. RESUMEN PARA EJECUTAR

```bash
# 1. Activar entorno
cd proyecto_untels
source venv/bin/activate

# 2. (OPCIONAL) Si quieres usar IA, configura .env
nano .env  # Añade GROQ_API_KEY=tu_clave

# 3. Ejecutar servidor
python manage.py runserver

# 4. Abrir en navegador

ESTUDIANTES:
http://127.0.0.1:8000/
Usuario: 2021101234
Password: estudiante123

DOCENTES:
http://127.0.0.1:8000/docente/login/
Usuario: DOCENTE001
Password: docente123
```

---

## Sistema listo para usar! 🚀
