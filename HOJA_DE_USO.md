# SISTEMA DE VALIDACIÓN DE INFORMES PPP - UNTELS
## Hoja de Usuarios y Guía de Ejecución

---

## 📥 CÓMO DESCARGAR / CLONAR EL PROYECTO

### OPCIÓN 1: Clonar con Git (Recomendado)

```bash
git clone https://github.com/GIAN2015/T.A-Arquitectura-de-software.git
cd T.A-Arquitectura-de-software
```

### OPCIÓN 2: Descargar ZIP desde GitHub

1. Ir a: https://github.com/GIAN2015/T.A-Arquitectura-de-software
2. Click en el botón verde **"Code"**
3. Click en **"Download ZIP"**
4. Descomprimir el archivo descargado
5. Abrir terminal en la carpeta descomprimida

### OPCIÓN 3: Si ya tienes el proyecto, actualizar cambios

```bash
cd T.A-Arquitectura-de-software
git pull origin main
```

---

## ⚙️ CONFIGURACIÓN INICIAL (Solo la primera vez)

### PASO 1: Entrar a la carpeta del proyecto Django

```bash
cd proyecto_untels
```

### PASO 2: Crear entorno virtual

```bash
python3 -m venv venv
```

### PASO 3: Activar el entorno virtual

**En Linux/Mac:**
```bash
source venv/bin/activate
```

**En Windows:**
```bash
venv\Scripts\activate
```

> Verás `(venv)` al inicio de la línea, eso significa que está activo.

### PASO 4: Instalar dependencias

```bash
pip install -r requirements.txt
```

### PASO 5: Configurar variables de entorno

Crear un archivo `.env` en la carpeta `proyecto_untels/` con este contenido:

```env
DJANGO_SECRET_KEY=django-insecure-dev-key-change-in-production-12345
DATABASE_URL=sqlite:///db.sqlite3
DEBUG=True
GROQ_API_KEY=
```

> **Nota:** Si dejas `GROQ_API_KEY` vacío, la IA funcionará en modo local (sin internet). Si quieres usar la IA real de GROQ, obtén una clave gratis en https://console.groq.com/ y pégala ahí.

### PASO 6: Aplicar migraciones de base de datos

```bash
python manage.py migrate
```

### PASO 7: Crear los usuarios de prueba

```bash
python manage.py shell -c "
from apps.usuarios.models import Usuario
from apps.reglamento.models import Reglamento
from apps.observaciones.models import BancoObservaciones

# Crear Alumno 1
a1 = Usuario.objects.create(codigo='2213110416', nombre='Andre Mendoza Quispe', tipo_usuario='estudiante')
a1.set_password('alumno123')

# Crear Alumno 2
a2 = Usuario.objects.create(codigo='2213110417', nombre='María Fernández López', tipo_usuario='estudiante')
a2.set_password('alumno123')

# Crear Docente
d = Usuario.objects.create(codigo='DOC001', nombre='Dr. Carlos Ramírez Torres', tipo_usuario='docente')
d.set_password('docente123')

# Reglamento básico
Reglamento.objects.create(nombre='Reglamento PPP 2024', contenido='Reglamento UNTELS para informes', activo=True)

# Observaciones
obs = [
    ('Carátula', 'Falta logo UNTELS'),
    ('Formato', 'Márgenes incorrectos'),
    ('Índice', 'Sin numeración'),
    ('Introducción', 'Muy breve'),
    ('Conclusiones', 'Poco fundamentadas'),
]
for s, d in obs:
    BancoObservaciones.objects.create(seccion=s, descripcion=d)

print('Usuarios y datos creados correctamente')
"
```

---

## 👥 USUARIOS DEL SISTEMA

### 🎓 ALUMNO 1
| Campo | Valor |
|-------|-------|
| **Código** | `2213110416` |
| **Nombre** | Andre Mendoza Quispe |
| **Contraseña** | `alumno123` |
| **Tipo** | Estudiante |
| **Portal** | http://127.0.0.1:8000/ |

---

### 🎓 ALUMNO 2
| Campo | Valor |
|-------|-------|
| **Código** | `2213110417` |
| **Nombre** | María Fernández López |
| **Contraseña** | `alumno123` |
| **Tipo** | Estudiante |
| **Portal** | http://127.0.0.1:8000/ |

---

### 👨‍🏫 DOCENTE
| Campo | Valor |
|-------|-------|
| **Código** | `DOC001` |
| **Nombre** | Dr. Carlos Ramírez Torres |
| **Contraseña** | `docente123` |
| **Tipo** | Docente |
| **Portal** | http://127.0.0.1:8000/docente/login/ |

---

## 🚀 CÓMO CORRER EL PROGRAMA (Uso diario)

### PASO 1: Abrir terminal en la carpeta del proyecto

```bash
cd T.A-Arquitectura-de-software/proyecto_untels
```

### PASO 2: Activar el entorno virtual

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### PASO 3: Iniciar el servidor

```bash
python manage.py runserver
```

> El servidor estará corriendo en `http://127.0.0.1:8000/`
> Para detener: presiona `Ctrl + C`

### PASO 4: Abrir en el navegador

**Para entrar como ALUMNO:**
```
http://127.0.0.1:8000/
```

**Para entrar como DOCENTE:**
```
http://127.0.0.1:8000/docente/login/
```

---

## 📝 CÓMO USAR EL SISTEMA

### Como ALUMNO:

1. Entrar al portal de estudiantes
2. Iniciar sesión con código y contraseña
3. Click en **"Subir Informe"**
4. Seleccionar archivo `.docx`
5. La IA analizará automáticamente
6. Ver observaciones generadas
7. Esperar revisión del docente
8. Si es **rechazado**, corregir y **reenviar**

### Como DOCENTE:

1. Entrar al portal de docentes
2. Iniciar sesión con código y contraseña
3. Ver lista de informes pendientes
4. Click en **"⚙️ Revisar"** en un informe
5. Para cada observación de la IA:
   - **Confirmar** (si es válida)
   - **Descartar** (si no aplica)
   - Cambiar severidad si es necesario
6. Escribir comentario general
7. **Aprobar** o **Rechazar** el informe

---

## 🔄 CÓMO ACTUALIZAR LOS CAMBIOS DESDE GITHUB

### Si trabajas en equipo y otros hicieron cambios:

```bash
# 1. Entrar al proyecto
cd T.A-Arquitectura-de-software

# 2. Descargar últimos cambios
git pull origin main

# 3. Entrar a la carpeta Django
cd proyecto_untels

# 4. Activar entorno virtual
source venv/bin/activate

# 5. Actualizar dependencias (por si hay nuevas)
pip install -r requirements.txt

# 6. Aplicar nuevas migraciones (por si hay cambios en BD)
python manage.py migrate

# 7. Correr el servidor
python manage.py runserver
```

---

## 📤 CÓMO SUBIR TUS CAMBIOS A GITHUB

```bash
# 1. Ver qué archivos cambiaste
git status

# 2. Agregar todos los cambios
git add .

# 3. Hacer commit con mensaje descriptivo
git commit -m "Descripción de los cambios"

# 4. Subir a GitHub
git push origin main
```

---

## 🔧 COMANDOS ÚTILES

### Detener el servidor
```
Ctrl + C
```

### Ver si el sistema está bien configurado
```bash
python manage.py check
```

### Reiniciar el servidor
```bash
python manage.py runserver
```

### Ver migraciones aplicadas
```bash
python manage.py showmigrations
```

### Crear un superusuario de Django
```bash
python manage.py createsuperuser
```

### Salir del entorno virtual
```bash
deactivate
```

---

## ⚠️ SI ALGO FALLA

### Error: "Address already in use"
Otro servidor está usando el puerto. Usar otro:
```bash
python manage.py runserver 8001
```
Luego abrir: `http://127.0.0.1:8001/`

### Error: "no such table"
Ejecutar migraciones:
```bash
python manage.py migrate
```

### Error: "ModuleNotFoundError"
Faltan dependencias, reinstalar:
```bash
pip install -r requirements.txt
```

### El servidor no inicia
Verificar que el entorno virtual esté activo (debe verse `(venv)` en la terminal)

### Olvidé la contraseña de un usuario
Resetear desde el shell:
```bash
python manage.py shell -c "
from apps.usuarios.models import Usuario
u = Usuario.objects.get(codigo='CODIGO_AQUI')
u.set_password('nueva_password')
print('Contraseña actualizada')
"
```

### Quiero borrar todo y empezar de nuevo
```bash
# 1. Borrar base de datos
rm db.sqlite3

# 2. Aplicar migraciones de nuevo
python manage.py migrate

# 3. Volver a crear usuarios (ver Paso 7 de Configuración Inicial)
```

---

## 📦 RESUMEN RÁPIDO (Para usar día a día)

```bash
# 1. Entrar a la carpeta
cd T.A-Arquitectura-de-software/proyecto_untels

# 2. Activar entorno
source venv/bin/activate

# 3. Correr el servidor
python manage.py runserver
```

**Luego abrir en el navegador:**
- Alumnos: http://127.0.0.1:8000/
- Docentes: http://127.0.0.1:8000/docente/login/

---

## 🎯 FLUJO DE PRUEBA RECOMENDADO

1. **Iniciar servidor** (paso 1, 2 y 3 arriba)
2. **Abrir navegador** en `http://127.0.0.1:8000/`
3. **Login como Alumno 1** (`2213110416` / `alumno123`)
4. **Subir un informe** `.docx`
5. **Ver las observaciones** que generó la IA
6. **Cerrar sesión**
7. **Ir al portal docente** `http://127.0.0.1:8000/docente/login/`
8. **Login como Docente** (`DOC001` / `docente123`)
9. **Click en "Revisar"** en el informe del alumno
10. **Aprobar o Rechazar** el informe
11. **Volver al login del alumno** y ver el resultado

---

## 📁 ESTRUCTURA DEL PROYECTO

```
T.A-Arquitectura-de-software/
│
├── HOJA_DE_USO.md              ← Esta guía
├── README.md                    ← Información general del proyecto
│
└── proyecto_untels/             ← Proyecto Django principal
    ├── venv/                    ← Entorno virtual (NO subir a Git)
    ├── manage.py                ← Comandos de Django
    ├── requirements.txt         ← Dependencias del proyecto
    ├── .env                     ← Variables de entorno (NO subir a Git)
    ├── db.sqlite3               ← Base de datos local
    │
    ├── config/                  ← Configuración de Django
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    │
    ├── apps/                    ← Aplicaciones del sistema
    │   ├── usuarios/            ← Gestión de usuarios
    │   ├── informes/            ← Manejo de informes
    │   ├── reglamento/          ← Reglamentos institucionales
    │   ├── observaciones/       ← IA y observaciones generadas
    │   └── core/                ← Vistas principales y navegación
    │
    └── templates/               ← Plantillas HTML
        ├── login.html
        ├── login_docente.html
        ├── upload_report.html
        ├── panel_docente.html
        ├── validation_result.html
        ├── historial.html
        └── admin/               ← Templates del panel administrativo
```

---

## 🔗 ENLACES IMPORTANTES

- **Repositorio GitHub:** https://github.com/GIAN2015/T.A-Arquitectura-de-software
- **GROQ API (para IA):** https://console.groq.com/
- **Documentación Django:** https://docs.djangoproject.com/

---

## 📋 REQUISITOS DEL SISTEMA

- **Python:** 3.10 o superior
- **Sistema operativo:** Linux, Mac o Windows
- **Espacio en disco:** ~200 MB
- **Conexión a internet:** Solo si quieres usar la IA real de GROQ (opcional)

---

## 📦 DEPENDENCIAS PRINCIPALES

```
Django==5.0.6
psycopg2-binary==2.9.9
python-docx==1.1.2
requests==2.32.3
dj-database-url==2.1.0
python-decouple==3.8
whitenoise==6.7.0
gunicorn==22.0.0
```

---

*Sistema desarrollado para UNTELS - Trabajo Académico de Arquitectura de Software*
