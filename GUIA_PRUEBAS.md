# 🧪 Guía de Pruebas - Sistema UNTELS v2.0

## ✅ Sistema Operativo

El servidor está corriendo en: **http://localhost:8000/**

---

## 🔧 Errores Corregidos

1. ✅ Template `login_secretaria.html` → `auth/login_secretaria.html`
2. ✅ Template `login_presidente.html` → `auth/login_presidente.html`  
3. ✅ URL `docente_banco_observaciones` → alias `docente_banco`
4. ✅ Contraseñas verificadas y funcionando

---

## 👥 Credenciales de Prueba

**Contraseña para todos:** `test123`

| Rol | Usuario | URL de Login |
|-----|---------|--------------|
| 📋 Secretaria | `secretaria1` | http://localhost:8000/secretaria/login/ |
| 👔 Presidente | `presidente_isi` | http://localhost:8000/presidente/login/ |
| 👨‍🏫 Docente | `docente_isi_1` | http://localhost:8000/docente/login/ |
| 🎓 Estudiante | `2020123456` | http://localhost:8000/ |

---

## 🧪 Pruebas por Rol

### 1️⃣ ESTUDIANTE

**URL:** http://localhost:8000/

**Pasos:**
1. Ingresar código: `2020123456`
2. Ingresar contraseña: `test123`
3. Click en "Iniciar Sesión"

**Resultado esperado:**
- ✅ Redirige a `/upload/`
- ✅ Muestra dashboard del estudiante
- ✅ Puede subir informes (PDF/DOCX)
- ✅ Ver historial de informes
- ✅ Ver resultados de validación

**Funcionalidades disponibles:**
- Subir nuevo informe
- Ver historial de informes enviados
- Ver resultado de cada informe
- Ver observaciones generadas
- Cerrar sesión

---

### 2️⃣ DOCENTE

**URL:** http://localhost:8000/docente/login/

**Pasos:**
1. Ingresar código: `docente_isi_1`
2. Ingresar contraseña: `test123`
3. Click en "Iniciar Sesión"

**Resultado esperado:**
- ✅ Redirige a `/panel-docente/`
- ✅ Muestra dashboard del docente
- ✅ Lista de informes asignados
- ✅ Acceso a banco de observaciones

**Funcionalidades disponibles:**
- Ver informes asignados para revisión
- Subir/gestionar banco de observaciones personalizado
- Revisar informes con IA
- Editar observaciones generadas
- Aprobar o rechazar informes
- Ver historial de revisiones
- Ver notificaciones

**⚠️ Nota:** Si da error en el panel, es porque falta crear el banco de observaciones o hay informes sin asignar correctamente.

---

### 3️⃣ SECRETARIA

**URL:** http://localhost:8000/secretaria/login/

**Pasos:**
1. Ingresar código: `secretaria1`
2. Ingresar contraseña: `test123`
3. Click en "Iniciar Sesión"

**Resultado esperado:**
- ✅ Redirige a `/secretaria/dashboard/`
- ✅ Muestra dashboard de secretaria
- ✅ Lista de informes pendientes de derivar
- ✅ Lista de informes listos para notificar

**Funcionalidades disponibles:**
- Ver informes enviados por estudiantes
- Derivar informes al presidente de escuela
- Notificar resultados a estudiantes
- Ver historial de derivaciones
- Ver notificaciones

---

### 4️⃣ PRESIDENTE

**URL:** http://localhost:8000/presidente/login/

**Pasos:**
1. Ingresar código: `presidente_isi`
2. Ingresar contraseña: `test123`
3. Click en "Iniciar Sesión"

**Resultado esperado:**
- ✅ Redirige a `/presidente/dashboard/`
- ✅ Muestra dashboard del presidente
- ✅ Lista de informes pendientes de asignar docente
- ✅ Lista de dictámenes pendientes de aprobar

**Funcionalidades disponibles:**
- Ver informes derivados por secretaria
- Asignar docente revisor a cada informe
- Revisar dictámenes de docentes
- Aprobar o rechazar dictámenes
- Ver historial de asignaciones y aprobaciones
- Ver notificaciones

---

## 🔄 Flujo Completo de Prueba

### Escenario: Validación completa de un informe

1. **ESTUDIANTE** (`2020123456`)
   - Login en http://localhost:8000/
   - Ir a "Subir Informe"
   - Subir un archivo PDF o DOCX
   - Ver que aparece en "Mis Informes"
   - Estado inicial: "enviado"

2. **SECRETARIA** (`secretaria1`)
   - Login en http://localhost:8000/secretaria/login/
   - Ver el informe nuevo en "Informes Recibidos"
   - Click en "Derivar"
   - Seleccionar presidente de escuela
   - Confirmar derivación
   - Estado nuevo: "pendiente_presidente"

3. **PRESIDENTE** (`presidente_isi`)
   - Login en http://localhost:8000/presidente/login/
   - Ver el informe en "Pendientes de Asignar"
   - Click en "Designar Docente"
   - Seleccionar docente revisor: `docente_isi_1`
   - Confirmar asignación
   - Estado nuevo: "pendiente_docente"

4. **DOCENTE** (`docente_isi_1`)
   - Login en http://localhost:8000/docente/login/
   - Ver el informe en "Informes Asignados"
   - Click en "Revisar"
   - Iniciar validación con IA (o sin IA si no hay GROQ_API_KEY)
   - Revisar observaciones generadas
   - Editar/confirmar/descartar observaciones
   - Aprobar o Rechazar el informe
   - Estado nuevo: "pendiente_aprobacion_presidente"

5. **PRESIDENTE** (`presidente_isi`)
   - Ver dictamen del docente
   - Click en "Revisar Dictamen"
   - Aprobar o Rechazar el dictamen
   - Agregar comentarios
   - Estado nuevo: "aprobado_presidente" o "rechazado_presidente"

6. **SECRETARIA** (`secretaria1`)
   - Ver informes listos para notificar
   - Click en "Notificar Estudiante"
   - Confirmar notificación
   - Estado final: "aprobado_final" o "rechazado_estudiante"

7. **ESTUDIANTE** (`2020123456`)
   - Ver resultado final en "Mis Informes"
   - Ver observaciones si fue rechazado
   - Ver felicitaciones si fue aprobado

---

## 🐛 Problemas Comunes y Soluciones

### Error: "NoReverseMatch at /panel-docente/"
- ✅ **SOLUCIONADO** - Se agregó alias `docente_banco` en las URLs

### Error: "TemplateDoesNotExist"
- ✅ **SOLUCIONADO** - Se corrigieron las rutas de templates a `auth/`

### Error: Login no funciona
- ✅ **VERIFICADO** - Todas las contraseñas están configuradas correctamente

### Error: CSRF token missing
- **Solución:** Esto es normal en pruebas con curl
- Usar el navegador para probar los logins

### Error: "No se puede acceder a dashboard"
- **Causa:** No hay datos de prueba suficientes
- **Solución:** Ver sección "Poblar más datos" abajo

---

## 📊 Verificar Estado Actual

```bash
cd backend
./venv/bin/python manage.py shell <<'EOF'
from apps.usuarios.models import Usuario
from apps.escuelas.models import Escuela
from apps.informes.models import Informe

print(f"Escuelas: {Escuela.objects.count()}")
print(f"Usuarios: {Usuario.objects.count()}")
print(f"Informes: {Informe.objects.count()}")
print("\nUsuarios por tipo:")
for tipo, nombre in Usuario.TIPO_CHOICES:
    count = Usuario.objects.filter(tipo_usuario=tipo).count()
    if count > 0:
        print(f"  {nombre}: {count}")
EOF
```

---

## 📝 Poblar Más Datos de Prueba

Si necesitas más usuarios o escuelas:

```bash
cd backend
./venv/bin/python manage.py shell <<'EOF'
from apps.usuarios.models import Usuario
from apps.escuelas.models import Escuela

# Crear más escuelas
escuela_imec, _ = Escuela.objects.get_or_create(
    codigo='IMEC',
    defaults={
        'nombre': 'Ingeniería Mecánica',
        'activo': True
    }
)

# Crear más estudiantes
est2 = Usuario.objects.create(
    codigo='2020123457',
    nombre='María Sánchez',
    tipo_usuario='estudiante',
    email='2020123457@untels.edu.pe',
    escuela=Escuela.objects.get(codigo='ISI'),
    activo=True
)
est2.set_password('test123')

print("✅ Datos adicionales creados")
EOF
```

---

## 🔄 Reiniciar Sistema

Si algo no funciona, reiniciar el servidor:

```bash
# Detener servidor
pkill -f "manage.py runserver"

# Iniciar servidor
cd backend
nohup ./venv/bin/python manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &

# Ver logs
tail -f server.log
```

---

## ✅ Checklist de Pruebas

- [ ] Login Estudiante funciona
- [ ] Login Docente funciona
- [ ] Login Secretaria funciona
- [ ] Login Presidente funciona
- [ ] Estudiante puede subir informe
- [ ] Secretaria puede derivar informe
- [ ] Presidente puede asignar docente
- [ ] Docente puede revisar con IA
- [ ] Presidente puede aprobar dictamen
- [ ] Secretaria puede notificar estudiante
- [ ] Estudiante recibe resultado final
- [ ] Sistema de notificaciones funciona
- [ ] Logout funciona para todos

---

**Última actualización:** 7 de Julio de 2026
