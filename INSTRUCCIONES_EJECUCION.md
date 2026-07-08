# 🚀 Instrucciones de Ejecución - Sistema UNTELS

## Sistema de Validación de Informes de Prácticas Preprofesionales
**Universidad Nacional Tecnológica de Lima Sur**

---

## ✅ Estado del Sistema

El sistema está **COMPLETAMENTE CONFIGURADO Y LISTO** para usar.

- ✅ Entorno virtual Python creado
- ✅ Dependencias instaladas (Django, Groq, etc.)
- ✅ Base de datos creada y migrada
- ✅ Datos de prueba poblados (4 usuarios, 1 escuela)
- ✅ Configuración `.env` lista

---

## 🎯 Cómo Ejecutar el Sistema

### Opción 1: Usando el script de inicio (Recomendado)

```bash
cd backend
./start_server.sh
```

### Opción 2: Comando directo

```bash
cd backend
./venv/bin/python manage.py runserver
```

### Opción 3: Usar el script original del proyecto

```bash
./INICIAR_SISTEMA.sh
```

---

## 🌐 URLs de Acceso

Una vez iniciado el servidor, accede a:

### Sistema v2.0 (Flujo Multi-Rol Completo)
- **Login General v2:** http://localhost:8000/v2/login/
- **Secretaria:** http://localhost:8000/v2/secretaria/login/
- **Presidente:** http://localhost:8000/v2/presidente/login/
- **Docente:** http://localhost:8000/v2/docente/login/

### Sistema v1.0 (Básico - Compatibilidad)
- **Estudiantes:** http://localhost:8000/login/
- **Docentes v1:** http://localhost:8000/docente/login/

### Administración
- **Admin Django:** http://localhost:8000/admin/

---

## 👥 Credenciales de Prueba

Todos los usuarios tienen la contraseña: **test123**

| Rol | Usuario | Contraseña | URL |
|-----|---------|------------|-----|
| 📋 Secretaria | `secretaria1` | `test123` | `/v2/secretaria/login/` |
| 👔 Presidente ISI | `presidente_isi` | `test123` | `/v2/presidente/login/` |
| 👨‍🏫 Docente ISI | `docente_isi_1` | `test123` | `/v2/docente/login/` |
| 🎓 Estudiante | `2020123456` | `test123` | `/v2/login/` |

---

## 🔄 Flujo Completo del Sistema v2.0

```
1. ESTUDIANTE → Envía informe (PDF/DOCX)
2. SECRETARIA → Deriva a Presidente de Escuela
3. PRESIDENTE → Designa Docente revisor
4. DOCENTE → Valida con IA + Banco personal de observaciones
5. PRESIDENTE → Aprueba o rechaza dictamen
6. SECRETARIA → Notifica al estudiante
7. ESTUDIANTE → Recibe resultado final
```

---

## 📁 Estructura del Proyecto

```
T.A-Arquitectura-de-software/
├── backend/                    ← Backend Django
│   ├── venv/                  ← Entorno virtual (configurado ✅)
│   ├── manage.py
│   ├── start_server.sh        ← Script para iniciar servidor
│   ├── config/                ← Configuración Django
│   ├── apps/                  ← Aplicaciones del sistema
│   │   ├── escuelas/
│   │   ├── usuarios/          ← 5 roles (estudiante, docente, presidente, secretaria, egresado)
│   │   ├── informes/
│   │   ├── observaciones/
│   │   └── notificaciones/
│   └── .env                   ← Variables de entorno (configurado ✅)
│
├── database/
│   └── db.sqlite3             ← Base de datos (creada ✅)
│
└── frontend/
    ├── templates/             ← Templates HTML
    └── static/                ← CSS, JS, imágenes
```

---

## 🐛 Solución de Problemas

### Error: "Address already in use"
El puerto 8000 ya está en uso. Opciones:

```bash
# Opción 1: Usar otro puerto
./venv/bin/python manage.py runserver 8001

# Opción 2: Matar proceso en puerto 8000
lsof -ti:8000 | xargs kill -9
```

### Error: "No module named 'apps'"
Asegúrate de estar en la carpeta `backend`:

```bash
cd backend
./venv/bin/python manage.py runserver
```

### Error: "ModuleNotFoundError"
Reactiva el entorno virtual:

```bash
cd backend
source venv/bin/activate  # Mac/Linux
# o
venv\Scripts\activate     # Windows
```

### Base de datos corrupta
Resetear base de datos:

```bash
cd backend
rm -f ../database/db.sqlite3
./venv/bin/python manage.py migrate
# Volver a poblar datos (ver sección siguiente)
```

---

## 🔄 Repoblar Datos de Prueba

Si necesitas volver a crear los usuarios de prueba:

```bash
cd backend
./venv/bin/python manage.py shell <<'EOF'
from apps.usuarios.models import Usuario
from apps.escuelas.models import Escuela

# Limpiar
Usuario.objects.all().delete()
Escuela.objects.all().delete()

# Crear escuela
escuela = Escuela.objects.create(
    codigo='ISI',
    nombre='Ingeniería de Sistemas e Informática',
    activo=True
)

# Crear usuarios
secretaria = Usuario.objects.create(
    codigo='secretaria1',
    nombre='Lic. Ana Torres Mendoza',
    tipo_usuario='secretaria',
    email='secretaria@untels.edu.pe',
    activo=True
)
secretaria.set_password('test123')

presidente = Usuario.objects.create(
    codigo='presidente_isi',
    nombre='Dr. Juan Pérez García',
    tipo_usuario='presidente',
    email='presidente.isi@untels.edu.pe',
    escuela=escuela,
    activo=True
)
presidente.set_password('test123')

docente = Usuario.objects.create(
    codigo='docente_isi_1',
    nombre='Ing. Carlos Ramírez',
    tipo_usuario='docente',
    email='cramirez@untels.edu.pe',
    escuela=escuela,
    activo=True
)
docente.set_password('test123')

estudiante = Usuario.objects.create(
    codigo='2020123456',
    nombre='José Gonzales',
    tipo_usuario='estudiante',
    email='2020123456@untels.edu.pe',
    escuela=escuela,
    activo=True
)
estudiante.set_password('test123')

escuela.presidente = presidente
escuela.save()

print("✅ Datos poblados exitosamente")
EOF
```

---

## 🤖 Configuración de IA (Opcional)

El sistema puede funcionar **sin API key** usando validación local con reglas heurísticas.

Para activar la validación con IA (GROQ API):

1. Obtener API key gratuita: https://console.groq.com/
2. Editar `backend/.env`:
   ```bash
   GROQ_API_KEY=gsk_tu_clave_aqui
   ```
3. Reiniciar servidor

---

## 📖 Documentación Adicional

- **README principal:** `README.md`
- **Guía de uso por rol:** `docs/GUIA_USO_POR_ROL_V2.md`
- **Referencia rápida:** `docs/REFERENCIA_RAPIDA_V2.md`
- **Arquitectura:** `docs/ARQUITECTURA_POR_CAPAS.md`

---

## 🎓 Información del Proyecto

**Trabajo Académico de Arquitectura de Software**

- **Universidad:** UNTELS
- **Curso:** Arquitectura de Software
- **Versión:** 2.0 - Flujo Multi-Rol Completo
- **Estado:** ✅ 100% Completado y Operativo

---

## 📞 Ayuda Rápida

**Comandos más usados:**

```bash
# Iniciar servidor
cd backend && ./start_server.sh

# Ver usuarios creados
cd backend
./venv/bin/python manage.py shell -c "from apps.usuarios.models import Usuario; print(Usuario.objects.all())"

# Crear superusuario Django (admin)
cd backend
./venv/bin/python manage.py createsuperuser

# Aplicar migraciones
cd backend
./venv/bin/python manage.py migrate

# Ejecutar tests
cd backend
./venv/bin/python manage.py test
```

---

## ✅ Checklist Pre-Ejecución

- [x] Python 3.9+ instalado
- [x] Entorno virtual creado (`backend/venv/`)
- [x] Dependencias instaladas
- [x] Archivo `.env` configurado
- [x] Migraciones aplicadas
- [x] Datos de prueba poblados
- [x] Puerto 8000 disponible

**¡Todo listo! Ejecuta `cd backend && ./start_server.sh` y comienza a probar el sistema!**

---

**Última actualización:** 7 de Julio de 2026
