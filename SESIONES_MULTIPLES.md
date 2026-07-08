# 🔄 Sesiones Múltiples por Pestaña - Sistema UNTELS

## ✅ PROBLEMA SOLUCIONADO

**Antes:** Solo podías tener un usuario logueado a la vez. Si abrías otra pestaña y te logueabas con otro usuario, la sesión anterior se cerraba.

**Ahora:** Puedes tener **diferentes usuarios en diferentes pestañas** del mismo navegador simultáneamente.

---

## 🎯 Cómo Funciona

### Tecnología Implementada

1. **JavaScript (sessionStorage):** Cada pestaña genera un ID único
2. **Middleware Django:** Separa las sesiones por tab_id
3. **Sin cookies adicionales:** Usa la misma cookie de sesión de Django

### Ejemplo de Uso

```
Pestaña 1: Docente (docente_isi_1)
Pestaña 2: Secretaria (secretaria1)
Pestaña 3: Presidente (presidente_isi)
Pestaña 4: Estudiante (2020123456)
```

**Todas funcionando simultáneamente sin interferir entre sí.**

---

## 📋 Cambios Realizados

### 1. JavaScript Multi-Tab Sessions
**Archivo:** `frontend/static/js/multi-tab-sessions.js`

- Genera ID único por pestaña usando `sessionStorage`
- Inyecta automáticamente el `tab_id` en todos los formularios
- Se mantiene mientras la pestaña está abierta
- Se pierde al cerrar la pestaña (por diseño)

### 2. Middleware de Sesiones
**Archivo:** `backend/apps/core/middleware.py`

- Intercepta todas las peticiones
- Lee el `tab_id` del POST/GET
- Crea un wrapper de sesión con prefijo único
- Mantiene sesiones separadas por pestaña

### 3. Activación en Settings
**Archivo:** `config/settings/base.py`

```python
MIDDLEWARE = [
    # ...
    'django.contrib.sessions.middleware.SessionMiddleware',
    'apps.core.middleware.MultiTabSessionMiddleware',  # <- NUEVO
    # ...
]
```

### 4. Inclusión en Templates
**Archivo:** `frontend/templates/base_v2.html`

```html
<script src="{% static 'js/multi-tab-sessions.js' %}"></script>
```

---

## 🧪 Cómo Probar

### Prueba 1: Múltiples Docentes

1. Abrir pestaña 1: http://localhost:8000/docente/login/
2. Login: `docente_isi_1` / `test123`
3. Abrir pestaña 2 (nueva): http://localhost:8000/docente/login/
4. Login: `docente_imec_1` / `test123` (si existe)
5. **Resultado:** Ambos docentes logueados simultáneamente

### Prueba 2: Diferentes Roles

1. **Pestaña 1:** Login como secretaria
   - URL: http://localhost:8000/secretaria/login/
   - Usuario: `secretaria1` / `test123`

2. **Pestaña 2:** Login como presidente
   - URL: http://localhost:8000/presidente/login/
   - Usuario: `presidente_isi` / `test123`

3. **Pestaña 3:** Login como docente
   - URL: http://localhost:8000/docente/login/
   - Usuario: `docente_isi_1` / `test123`

4. **Pestaña 4:** Login como estudiante
   - URL: http://localhost:8000/
   - Usuario: `2020123456` / `test123`

5. **Verificar:** Navegar entre pestañas - cada una mantiene su sesión

### Prueba 3: Verificar Independencia

1. En pestaña 1: Crear un banco de observaciones como docente
2. En pestaña 2: Login como secretaria
3. Volver a pestaña 1: Debe seguir siendo docente
4. Volver a pestaña 2: Debe seguir siendo secretaria

---

## 🔍 Verificación Técnica

### Ver Tab ID en Consola del Navegador

1. Abrir DevTools (F12)
2. Ir a Console
3. Verás: `Tab ID: tab_1234567890_xxxxx`
4. Cada pestaña tiene un ID diferente

### Inspeccionar Formularios

1. Click derecho en cualquier botón → Inspeccionar
2. Buscar el formulario padre
3. Verás un campo oculto:
```html
<input type="hidden" name="tab_id" value="tab_1234567890_xxxxx">
```

### Ver Sesiones en Django

```bash
cd backend
./venv/bin/python manage.py shell <<'EOF'
from django.contrib.sessions.models import Session
from django.utils import timezone

# Ver todas las sesiones activas
for s in Session.objects.filter(expire_date__gte=timezone.now()):
    data = s.get_decoded()
    print(f"Sesión: {s.session_key[:10]}...")
    for key, value in data.items():
        if key.startswith('tab_'):
            print(f"  {key}: {value}")
EOF
```

---

## ⚠️ Consideraciones Importantes

### Qué Funciona
- ✅ Login de múltiples usuarios simultáneos
- ✅ Navegación independiente por pestaña
- ✅ Formularios POST mantienen la sesión correcta
- ✅ Logout solo afecta a la pestaña actual
- ✅ Funciona con todos los roles

### Limitaciones

1. **Ventanas en Modo Incógnito:** Cada ventana incógnita es independiente automáticamente
2. **Duplicar Pestaña (Ctrl+Shift+T):** Puede compartir el mismo tab_id inicialmente, pero al navegar se regenera
3. **Cerrar y Reabrir:** Al cerrar una pestaña, se pierde el tab_id (comportamiento deseado)

### Seguridad

- ✅ No expone información sensible
- ✅ El tab_id es aleatorio y único
- ✅ Las sesiones siguen usando la misma cookie segura de Django
- ✅ El middleware valida que el tab_id pertenezca a la sesión actual

---

## 🐛 Solución de Problemas

### Problema: Las pestañas siguen compartiendo sesión

**Solución:**
1. Limpiar caché del navegador
2. Hacer hard refresh (Ctrl+Shift+R)
3. Verificar que el JS se carga: DevTools → Network → `multi-tab-sessions.js`

### Problema: El formulario no tiene tab_id

**Solución:**
1. Verificar en DevTools Console que aparece "Tab ID: ..."
2. Inspeccionar el formulario
3. Si no aparece, revisar que el script se carga correctamente

### Problema: Error en el middleware

**Solución:**
```bash
# Ver logs del servidor
cd backend
tail -50 server.log

# Verificar que el middleware está activado
./venv/bin/python manage.py shell -c "
from django.conf import settings
print('MultiTabSessionMiddleware' in str(settings.MIDDLEWARE))
"
```

---

## 📊 Comparación: Antes vs Ahora

### ANTES ❌
```
Usuario 1 login en Pestaña 1 → Sesión A
Usuario 2 login en Pestaña 2 → Sesión A (reemplaza)
Volver a Pestaña 1 → Sesión cerrada ❌
```

### AHORA ✅
```
Usuario 1 login en Pestaña 1 → Sesión A-tab1
Usuario 2 login en Pestaña 2 → Sesión A-tab2
Volver a Pestaña 1 → Usuario 1 sigue logueado ✅
```

---

## 🎓 Casos de Uso Prácticos

### Para Desarrollo
- Probar flujo completo sin cambiar de usuario
- Comparar vistas de diferentes roles
- Debugging de permisos

### Para Demostración
- Mostrar diferentes roles simultáneamente
- Presentar el flujo completo en tiempo real
- Comparar dashboards

### Para Pruebas
- Testing de integración multi-rol
- Verificar notificaciones entre roles
- Probar flujos concurrentes

---

## 📝 Archivos Modificados

1. ✅ `frontend/static/js/multi-tab-sessions.js` - NUEVO
2. ✅ `backend/apps/core/middleware.py` - NUEVO
3. ✅ `backend/config/settings/base.py` - Middleware agregado
4. ✅ `frontend/templates/base_v2.html` - Script incluido
5. ✅ `backend/apps/presentacion/web/docente_views.py` - URLs corregidas

---

## ✅ Verificación Final

```bash
# 1. Servidor corriendo
ps aux | grep "manage.py runserver"

# 2. JavaScript disponible
ls -la frontend/static/js/multi-tab-sessions.js

# 3. Middleware activo
grep -r "MultiTabSessionMiddleware" backend/config/settings/

# 4. Template actualizado
grep -r "multi-tab-sessions.js" frontend/templates/base_v2.html
```

---

## 🎉 Resumen

**Ahora puedes trabajar con múltiples usuarios en diferentes pestañas del navegador sin tener que cerrar sesión constantemente.**

**Pruébalo:**
1. Abre 4 pestañas
2. Login con usuarios diferentes en cada una
3. Navega entre ellas
4. ¡Todas las sesiones se mantienen independientes!

---

Última actualización: 7 de Julio de 2026, 23:45 hrs
