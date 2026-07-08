# 🔐 TABLA DE LOGINS Y DASHBOARDS

**Fecha:** 8 de Julio de 2026, 01:50 hrs  
**Estado:** CORREGIDO

---

## ✅ CONFIGURACIÓN CORRECTA

| Rol | URL Login | Usuario | Password | Dashboard URL | Nombre URL Dashboard |
|-----|-----------|---------|----------|---------------|---------------------|
| **Estudiante** | `/` | `2020123456` | `test123` | `/upload/` | `upload` |
| **Docente** | `/docente/login/` | `docente_isi_1` | `test123` | `/panel-docente/` | `panel_docente` |
| **Secretaria** | `/secretaria/login/` | `secretaria1` | `test123` | `/secretaria/dashboard/` | `secretaria_dashboard` |
| **Presidente** | `/presidente/login/` | `presidente_isi` | `test123` | `/presidente/dashboard/` | `presidente_dashboard` |

---

## 🔧 PROBLEMA CORREGIDO

### ❌ ANTES (Decorador con URLs incorrectas):

```python
# apps/core/decorators.py
if usuario_tipo == 'estudiante':
    return redirect('estudiante_dashboard')  # ❌ NO EXISTE
elif usuario_tipo == 'docente':
    return redirect('docente_dashboard')     # ❌ NO EXISTE
```

**Resultado:** Cuando un estudiante intentaba acceder a una página de secretaria, el decorador intentaba redirigirlo a `estudiante_dashboard` que NO EXISTE → Error 404 o comportamiento inesperado.

### ✅ AHORA (Corregido):

```python
# apps/core/decorators.py
if usuario_tipo == 'estudiante':
    return redirect('upload')           # ✅ CORRECTO
elif usuario_tipo == 'docente':
    return redirect('panel_docente')    # ✅ CORRECTO
```

---

## 🧪 PRUEBAS DE VERIFICACIÓN

### Test 1: Login como Estudiante
```
1. Ir a http://localhost:8000/
2. Ingresar: 2020123456 / test123
3. ✅ Debe redirigir a /upload/
4. ✅ Ver "Subir Informe de Prácticas"
```

### Test 2: Estudiante intenta acceder a Secretaria
```
1. Estando logueado como estudiante
2. Ir manualmente a http://localhost:8000/secretaria/dashboard/
3. ✅ Debe mostrar: "Acceso denegado. Esta página es solo para secretaria."
4. ✅ Debe redirigir automáticamente a /upload/
```

### Test 3: Login como Secretaria
```
1. Ir a http://localhost:8000/secretaria/login/
2. Ingresar: secretaria1 / test123
3. ✅ Debe redirigir a /secretaria/dashboard/
4. ✅ Ver "Dashboard de Secretaria"
```

### Test 4: Secretaria intenta acceder a Estudiante
```
1. Estando logueada como secretaria
2. Ir manualmente a http://localhost:8000/upload/
3. ✅ Debe mostrar: "Acceso denegado. Esta página es solo para estudiante."
4. ✅ Debe redirigir automáticamente a /secretaria/dashboard/
```

### Test 5: Login como Presidente
```
1. Ir a http://localhost:8000/presidente/login/
2. Ingresar: presidente_isi / test123
3. ✅ Debe redirigir a /presidente/dashboard/
4. ✅ Ver "Dashboard de Presidente"
```

### Test 6: Login como Docente
```
1. Ir a http://localhost:8000/docente/login/
2. Ingresar: docente_isi_1 / test123
3. ✅ Debe redirigir a /panel-docente/
4. ✅ Ver "Dashboard Docente"
```

---

## 📋 FLUJO DE REDIRECCIÓN

### Cuando un usuario YA LOGUEADO intenta acceder a otra área:

```
Usuario Logueado: Estudiante
Intenta acceder: /secretaria/dashboard/

Decorador @requiere_rol('secretaria'):
1. Verifica sesión ✓
2. Verifica tipo: 'estudiante' ≠ 'secretaria' ❌
3. Mensaje: "Acceso denegado. Esta página es solo para secretaria."
4. Detecta que es estudiante
5. Redirige a 'upload' (dashboard de estudiante) ✓
```

```
Usuario Logueado: Secretaria
Intenta acceder: /upload/

Decorador @requiere_rol('estudiante'):
1. Verifica sesión ✓
2. Verifica tipo: 'secretaria' ≠ 'estudiante' ❌
3. Mensaje: "Acceso denegado. Esta página es solo para estudiante."
4. Detecta que es secretaria
5. Redirige a 'secretaria_dashboard' ✓
```

---

## ✅ URLS VERIFICADAS

### Estudiante:
- ✅ `upload` → `/upload/` → `views.upload_view`
- ✅ `resultado` → `/resultado/<id>/`
- ✅ `historial` → `/historial/`

### Docente:
- ✅ `panel_docente` → `/panel-docente/` → `docente_views.panel_docente_view`
- ✅ `docente_banco` → `/docente/banco/`
- ✅ `docente_revisar_informe` → `/docente/revisar/<id>/`

### Secretaria:
- ✅ `secretaria_dashboard` → `/secretaria/dashboard/`
- ✅ `secretaria_derivar` → `/secretaria/derivar/<id>/`
- ✅ `secretaria_notificar` → `/secretaria/notificar/<id>/`

### Presidente:
- ✅ `presidente_dashboard` → `/presidente/dashboard/`
- ✅ `presidente_designar` → `/presidente/designar/<id>/`
- ✅ `presidente_revisar` → `/presidente/revisar/<id>/`

---

## 🎯 RESUMEN

**Problema:** Decorador usaba nombres de URLs inexistentes para redirigir.

**Causa:** 
- `estudiante_dashboard` no existe (debería ser `upload`)
- `docente_dashboard` no existe (debería ser `panel_docente`)

**Solución:** Corregidas las 2 líneas en `apps/core/decorators.py`

**Resultado:**
- ✅ Cada rol se loguea en SU dashboard
- ✅ Si intenta acceder a otro dashboard, lo redirige al SUYO
- ✅ No más confusión entre dashboards
- ✅ Mensajes de error claros

---

**Sistema de logins funcionando correctamente.**

Última actualización: 8 de Julio de 2026, 01:50 hrs
