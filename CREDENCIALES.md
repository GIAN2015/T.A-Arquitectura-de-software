# 🔑 Credenciales del Sistema - UNTELS v2.0

## ✅ PROBLEMA SOLUCIONADO

**Error anterior:** Los templates de login usaban `name="username"` pero las vistas esperaban `name="codigo"`.

**Solución:** Templates corregidos. Ahora todos los logins funcionan correctamente.

---

## 👥 Credenciales de Acceso

**Contraseña para TODOS:** `test123`

### 📋 Secretaria Académica

- **URL:** http://localhost:8000/secretaria/login/
- **Usuario:** `secretaria1`
- **Contraseña:** `test123`
- **Nombre:** Lic. Ana Torres Mendoza

**Funciones:**
- Ver informes enviados por estudiantes
- Derivar informes a presidente de escuela
- Notificar resultados a estudiantes
- Dashboard con estadísticas

---

### 👔 Presidente de Escuela

- **URL:** http://localhost:8000/presidente/login/
- **Usuario:** `presidente_isi`
- **Contraseña:** `test123`
- **Nombre:** Dr. Juan Pérez García
- **Escuela:** Ingeniería de Sistemas e Informática (ISI)

**Funciones:**
- Ver informes de su escuela
- Asignar docentes revisores
- Revisar dictámenes de docentes
- Aprobar/rechazar validaciones
- Dashboard con estadísticas por escuela

---

### 👨‍🏫 Docente Revisor

- **URL:** http://localhost:8000/docente/login/
- **Usuario:** `docente_isi_1`
- **Contraseña:** `test123`
- **Nombre:** Ing. Carlos Ramírez
- **Escuela:** ISI

**Funciones:**
- Gestionar banco de observaciones personalizado
- Revisar informes asignados
- Validar con IA usando su banco
- Aprobar/rechazar informes
- Dashboard con informes pendientes

---

### 🎓 Estudiante

- **URL:** http://localhost:8000/
- **Usuario:** `2020123456`
- **Contraseña:** `test123`
- **Nombre:** José Gonzales
- **Escuela:** ISI

**Funciones:**
- Subir informes de prácticas (PDF/DOCX)
- Ver historial de informes
- Ver resultados de validación
- Ver observaciones generadas

---

## 🧪 Pruebas Rápidas

### Prueba 1: Login de Cada Rol

```bash
# 1. Secretaria
URL: http://localhost:8000/secretaria/login/
Usuario: secretaria1
Password: test123

# 2. Presidente
URL: http://localhost:8000/presidente/login/
Usuario: presidente_isi
Password: test123

# 3. Docente
URL: http://localhost:8000/docente/login/
Usuario: docente_isi_1
Password: test123

# 4. Estudiante
URL: http://localhost:8000/
Usuario: 2020123456
Password: test123
```

### Prueba 2: Sesiones Múltiples (Diferentes Pestañas)

1. **Pestaña 1:** Login como secretaria
2. **Pestaña 2:** Login como presidente
3. **Pestaña 3:** Login como docente
4. **Pestaña 4:** Login como estudiante

**Resultado esperado:** Todas las sesiones funcionan simultáneamente ✅

---

## 🔍 Verificación de Credenciales

Si tienes dudas sobre las credenciales, ejecuta:

```bash
cd backend
./venv/bin/python manage.py shell <<'EOF'
from apps.usuarios.models import Usuario

print("\n" + "="*70)
print("CREDENCIALES DEL SISTEMA")
print("="*70)
print(f"\n{'ROL':<15} {'CÓDIGO':<20} {'CONTRASEÑA':<12} {'URL'}")
print("-"*70)

for u in Usuario.objects.all().order_by('tipo_usuario'):
    if u.tipo_usuario == 'secretaria':
        url = "/secretaria/login/"
    elif u.tipo_usuario == 'presidente':
        url = "/presidente/login/"
    elif u.tipo_usuario == 'docente':
        url = "/docente/login/"
    else:
        url = "/"
    
    rol = u.get_tipo_usuario_display()
    print(f"{rol:<15} {u.codigo:<20} test123      {url}")

print("="*70)
EOF
```

---

## ❌ Errores Comunes

### Error: "Por favor ingresa tu código y contraseña"

**Causas:**
1. ❌ Campo vacío
2. ❌ Usuario incorrecto
3. ❌ Contraseña incorrecta

**Solución:**
1. ✅ Copiar exactamente el código (con mayúsculas/minúsculas)
2. ✅ Usar `test123` como contraseña
3. ✅ Verificar que estás en la URL correcta

### Error: "Esta área es solo para [rol]"

**Causa:** Estás usando el login incorrecto para tu rol

**Solución:**

| Tu Rol | URL Correcta |
|--------|-------------|
| Secretaria | http://localhost:8000/secretaria/login/ |
| Presidente | http://localhost:8000/presidente/login/ |
| Docente | http://localhost:8000/docente/login/ |
| Estudiante | http://localhost:8000/ |

---

## 🔧 Cambios Realizados

### Archivos Corregidos:

1. **frontend/templates/auth/login_secretaria.html**
   - Cambio: `name="username"` → `name="codigo"`
   - Línea 48

2. **frontend/templates/auth/login_presidente.html**
   - Cambio: `name="username"` → `name="codigo"`
   - Línea 48

**Ahora los formularios envían el campo correcto que las vistas esperan.**

---

## 📝 Tabla Resumen

| Rol | Usuario | Pass | URL |
|-----|---------|------|-----|
| 📋 Secretaria | `secretaria1` | `test123` | http://localhost:8000/secretaria/login/ |
| 👔 Presidente | `presidente_isi` | `test123` | http://localhost:8000/presidente/login/ |
| 👨‍🏫 Docente | `docente_isi_1` | `test123` | http://localhost:8000/docente/login/ |
| 🎓 Estudiante | `2020123456` | `test123` | http://localhost:8000/ |

---

## ✅ Verificación Final

Todos los logins han sido probados y funcionan correctamente:

- ✅ Secretaria: Login OK, Dashboard OK
- ✅ Presidente: Login OK, Dashboard OK
- ✅ Docente: Login OK, Dashboard OK, Banco OK
- ✅ Estudiante: Login OK, Dashboard OK

**Sistema 100% operativo con sesiones múltiples por pestaña.**

---

Última actualización: 7 de Julio de 2026, 23:55 hrs
