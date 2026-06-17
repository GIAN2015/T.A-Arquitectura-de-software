# Sistema de Validación de Informes de Prácticas Preprofesionales - UNTELS

Sistema web Django que valida automáticamente informes de prácticas preprofesionales usando **Inteligencia Artificial** (GROQ API con Llama 3.3 70B) y permite la **revisión docente** posterior.

> 📘 **Trabajo Académico de Arquitectura de Software - UNTELS**

---

## 🎯 Características Principales

- ✅ **Login separado** para Estudiantes y Docentes
- 🤖 **Validación automática con IA** (GROQ API o modo local)
- 📄 **Procesamiento de archivos .docx**
- 👨‍🏫 **Panel de revisión docente** con observaciones agrupadas por severidad
- 🔄 **Sistema de versionado** para reenvío de correcciones
- 📊 **Dashboard administrativo** con estadísticas
- 🔒 **Control de acceso** basado en roles

---

## 🚀 Inicio Rápido

### 1. Clonar el repositorio

```bash
git clone https://github.com/GIAN2015/T.A-Arquitectura-de-software.git
cd T.A-Arquitectura-de-software/proyecto_untels
```

### 2. Configurar entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate    # Linux/Mac
# o
venv\Scripts\activate       # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crear archivo `.env`:

```env
DJANGO_SECRET_KEY=tu_clave_secreta_aqui
DATABASE_URL=sqlite:///db.sqlite3
DEBUG=True
GROQ_API_KEY=  # Opcional, dejar vacío para usar IA local
```

### 5. Aplicar migraciones

```bash
python manage.py migrate
```

### 6. Crear usuarios de prueba

```bash
python manage.py shell -c "
from apps.usuarios.models import Usuario
a1 = Usuario.objects.create(codigo='2213110416', nombre='Andre Mendoza', tipo_usuario='estudiante')
a1.set_password('alumno123')
d = Usuario.objects.create(codigo='DOC001', nombre='Dr. Ramírez', tipo_usuario='docente')
d.set_password('docente123')
print('Usuarios creados')
"
```

### 7. Ejecutar servidor

```bash
python manage.py runserver
```

Abrir en navegador:
- **Estudiantes:** http://127.0.0.1:8000/
- **Docentes:** http://127.0.0.1:8000/docente/login/

---

## 👥 Usuarios de Prueba

| Rol | Código | Contraseña | Portal |
|-----|--------|------------|--------|
| 🎓 Alumno 1 | `2213110416` | `alumno123` | `/` |
| 🎓 Alumno 2 | `2213110417` | `alumno123` | `/` |
| 👨‍🏫 Docente | `DOC001` | `docente123` | `/docente/login/` |

> Ver más detalles en [HOJA_DE_USO.md](HOJA_DE_USO.md)

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐
│     ALUMNO      │
└────────┬────────┘
         │ 1. Sube .docx
         ▼
┌─────────────────┐
│  SISTEMA WEB    │
│   (Django)      │
└────────┬────────┘
         │ 2. Extrae contenido
         ▼
┌─────────────────┐         ┌─────────────────┐
│   IA (GROQ)     │◄────────│  REGLAMENTO     │
│  Llama 3.3 70B  │         │  BANCO OBS.     │
└────────┬────────┘         └─────────────────┘
         │ 3. Genera observaciones
         ▼
┌─────────────────┐
│    DOCENTE      │
└────────┬────────┘
         │ 4. Confirma/descarta
         │    Aprueba/Rechaza
         ▼
    APROBADO o RECHAZADO
         │
         │ Si rechazado:
         ▼
   ALUMNO REENVÍA
   (nueva versión)
```

---

## 📁 Estructura del Proyecto

```
T.A-Arquitectura-de-software/
├── README.md                    ← Este archivo
├── HOJA_DE_USO.md              ← Guía detallada de uso
│
└── proyecto_untels/             ← Proyecto Django
    ├── manage.py
    ├── requirements.txt
    ├── config/                  ← Configuración Django
    ├── apps/                    ← Apps del sistema
    │   ├── usuarios/            ← Gestión usuarios
    │   ├── informes/            ← Manejo informes
    │   ├── reglamento/          ← Reglamentos
    │   ├── observaciones/       ← IA y observaciones
    │   └── core/                ← Vistas principales
    └── templates/               ← HTML
```

---

## 🤖 Integración con IA

El sistema usa **GROQ API** con el modelo **Llama 3.3 70B** para validar informes.

### Configurar IA (Opcional)

1. Obtén API Key gratis en https://console.groq.com/
2. Edita `.env` y añade: `GROQ_API_KEY=tu_clave`
3. Reinicia el servidor

### Modo Local (Sin API Key)

Si no configuras GROQ_API_KEY, el sistema usa **validación local con 10 reglas heurísticas** que detectan:
- Falta de carátula UNTELS
- Falta de índice, introducción, conclusiones
- Contenido muy corto
- Falta de descripción de empresa
- Falta de actividades
- Falta de referencias
- Y más...

---

## 🛠️ Tecnologías Usadas

- **Backend:** Django 5.0.6
- **Base de datos:** SQLite (dev) / PostgreSQL (producción)
- **IA:** GROQ API (Llama 3.3 70B)
- **Procesamiento:** python-docx
- **Frontend:** Bootstrap 5
- **Despliegue:** Gunicorn + Whitenoise

---

## 📋 Estados del Informe

| Estado | Descripción |
|--------|-------------|
| `enviado` | Alumno subió el archivo |
| `validando` | IA está procesando |
| `observado` | IA encontró observaciones |
| `revision_docente` | Docente está revisando |
| `aprobado` | Docente aprobó ✓ |
| `rechazado` | Docente rechazó, debe corregir |
| `completado` | Proceso finalizado |

---

## 🔄 Trabajar con Git

### Descargar cambios del repositorio

```bash
git pull origin main
```

### Subir tus cambios

```bash
git add .
git commit -m "Descripción de cambios"
git push origin main
```

---

## 📦 Dependencias

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

## 🐛 Solución de Problemas

### Error: "no such table"
```bash
python manage.py migrate
```

### Error: "Address already in use"
```bash
python manage.py runserver 8001
```

### Error: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

---

## 📖 Documentación Adicional

- **[HOJA_DE_USO.md](HOJA_DE_USO.md)** - Guía completa con credenciales y casos de uso
- **Documentación Django:** https://docs.djangoproject.com/
- **GROQ API:** https://console.groq.com/docs/

---

## 👨‍💻 Autor

Desarrollado como Trabajo Académico para el curso de **Arquitectura de Software** en la **Universidad Nacional Tecnológica de Lima Sur (UNTELS)**.

---

## 📄 Licencia

Proyecto académico - Uso educativo
