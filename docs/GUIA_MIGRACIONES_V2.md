# GUÍA DE MIGRACIONES v2.0

**Sistema de Validación de Informes de Prácticas Preprofesionales - UNTELS**

**Versión:** 2.0 - Flujo Completo Multi-Rol  
**Fecha:** 29 de Junio de 2026

---

## 📋 ÍNDICE

1. [Prerequisitos](#prerequisitos)
2. [Migraciones Paso a Paso](#migraciones-paso-a-paso)
3. [Orden de Migraciones](#orden-de-migraciones)
4. [Resolución de Problemas](#resolución-de-problemas)
5. [Rollback y Recuperación](#rollback-y-recuperación)

---

## PREREQUISITOS

### 1. Entorno de Desarrollo Activo

```bash
# Verificar que Python está instalado
python --version  # Debe ser Python 3.12+

# Verificar que Django está instalado
python -m django --version  # Debe ser Django 4.2+
```

### 2. Base de Datos Configurada

```bash
# Verificar conexión a PostgreSQL
psql -U untels_user -d untels_db -c "SELECT version();"
```

### 3. Variables de Entorno

```bash
# Verificar que .env está configurado
cat backend/.env

# Variables requeridas:
# - DB_NAME
# - DB_USER
# - DB_PASSWORD
# - DB_HOST
# - DB_PORT
```

---

## MIGRACIONES PASO A PASO

### PASO 1: Preparación

```bash
# 1. Activar entorno virtual
cd backend
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# 2. Verificar apps instaladas
python manage.py check

# 3. Ver estado actual de migraciones
python manage.py showmigrations
```

### PASO 2: Crear Migraciones

```bash
# IMPORTANTE: Seguir este orden exacto

# 1. Escuelas (PRIMERO - no tiene dependencias)
python manage.py makemigrations escuelas

# 2. Usuarios (SEGUNDO - depende de Escuelas)
python manage.py makemigrations usuarios

# 3. Observaciones (TERCERO - depende de Usuarios)
python manage.py makemigrations observaciones

# 4. Informes (CUARTO - depende de Usuarios, Escuelas, Observaciones)
python manage.py makemigrations informes

# 5. Notificaciones (QUINTO - depende de Usuarios, Informes)
python manage.py makemigrations notificaciones

# 6. Verificar que se crearon
ls -la apps/*/migrations/
```

### PASO 3: Revisar Migraciones

```bash
# Ver SQL que se ejecutará (sin aplicar)
python manage.py sqlmigrate escuelas 0001

# Ver todas las migraciones pendientes
python manage.py showmigrations

# Debe verse algo como:
# escuelas
#  [ ] 0001_initial
# usuarios
#  [ ] 0001_initial
#  [ ] 0002_add_new_fields_v2
# ...
```

### PASO 4: Aplicar Migraciones

```bash
# Aplicar todas las migraciones
python manage.py migrate

# O aplicar por app (en orden)
python manage.py migrate escuelas
python manage.py migrate usuarios
python manage.py migrate observaciones
python manage.py migrate informes
python manage.py migrate notificaciones
```

### PASO 5: Verificación

```bash
# 1. Verificar que se aplicaron correctamente
python manage.py showmigrations

# Debe verse algo como:
# escuelas
#  [X] 0001_initial
# usuarios
#  [X] 0001_initial
#  [X] 0002_add_new_fields_v2
# ...

# 2. Verificar tablas en PostgreSQL
psql -U untels_user -d untels_db -c "\dt"

# 3. Verificar que los modelos funcionan
python manage.py shell
>>> from apps.escuelas.models import Escuela
>>> from apps.usuarios.models import Usuario
>>> from apps.observaciones.models import BancoObservacionesDocente
>>> from apps.notificaciones.models import Notificacion
>>> # Debe importar sin errores
>>> exit()
```

---

## ORDEN DE MIGRACIONES

### Dependencias de Modelos

```
1. Escuelas
   └─ Sin dependencias

2. Usuarios
   └─ Depende de: Escuelas (ForeignKey escuela)

3. Observaciones (BancoObservacionesDocente)
   └─ Depende de: Usuarios (ForeignKey docente)

4. Informes
   └─ Depende de: Usuarios (usuario, secretaria, presidente, docente)
   └─ Depende de: Escuelas (escuela)
   └─ Depende de: Observaciones (banco_observaciones_usado)

5. Notificaciones
   └─ Depende de: Usuarios (usuario)
   └─ Depende de: Informes (informe, nullable)
```

### Orden Correcto de Ejecución

```bash
# ✓ CORRECTO
makemigrations escuelas
makemigrations usuarios
makemigrations observaciones
makemigrations informes
makemigrations notificaciones

# ✗ INCORRECTO
makemigrations usuarios  # Fallará: Escuela no existe
makemigrations escuelas
```

---

## RESOLUCIÓN DE PROBLEMAS

### Problema 1: "No such table: apps_escuela"

**Causa:** No se aplicaron las migraciones de escuelas

**Solución:**
```bash
python manage.py migrate escuelas
```

### Problema 2: "ForeignKey references nonexistent table"

**Causa:** Intentas migrar un modelo antes que sus dependencias

**Solución:**
```bash
# Migrar en el orden correcto
python manage.py migrate escuelas
python manage.py migrate usuarios
python manage.py migrate observaciones
python manage.py migrate informes
python manage.py migrate notificaciones
```

### Problema 3: "Conflicting migrations detected"

**Causa:** Migraciones se crearon en diferente orden

**Solución:**
```bash
# 1. Eliminar migraciones conflictivas
rm apps/usuarios/migrations/000*.py
rm apps/escuelas/migrations/000*.py
# ... etc

# 2. Mantener solo __init__.py
# 3. Crear migraciones de nuevo en orden correcto
```

### Problema 4: "Column already exists"

**Causa:** La base de datos ya tiene los cambios pero las migraciones no

**Solución:**
```bash
# Opción 1: Marcar migración como aplicada (fake)
python manage.py migrate --fake escuelas

# Opción 2: Resetear base de datos (CUIDADO: borra datos)
python manage.py flush
python manage.py migrate
```

### Problema 5: "IntegrityError: null value"

**Causa:** Campo requerido sin valor default

**Solución:**
```python
# En el modelo, agregar default o null=True
class Usuario(AbstractBaseUser):
    escuela = models.ForeignKey(
        Escuela, 
        on_delete=models.SET_NULL, 
        null=True,  # ← Permite NULL temporalmente
        blank=True
    )
```

---

## ROLLBACK Y RECUPERACIÓN

### Volver a Migración Anterior

```bash
# Ver número de migración actual
python manage.py showmigrations usuarios

# Volver a migración específica
python manage.py migrate usuarios 0001

# Volver a estado inicial (sin migraciones)
python manage.py migrate usuarios zero
```

### Backup Antes de Migrar

```bash
# 1. Backup de base de datos
pg_dump -U untels_user untels_db > backup_pre_migracion.sql

# 2. Aplicar migraciones
python manage.py migrate

# 3. Si algo sale mal, restaurar
psql -U untels_user -d untels_db < backup_pre_migracion.sql
```

### Recuperación de Emergencia

```bash
# Si las migraciones están totalmente rotas:

# 1. Eliminar base de datos
dropdb untels_db

# 2. Crear nueva base de datos
createdb untels_db

# 3. Eliminar archivos de migración (excepto __init__.py)
find apps/*/migrations -name "*.py" ! -name "__init__.py" -delete

# 4. Crear migraciones desde cero
python manage.py makemigrations
python manage.py migrate

# 5. Poblar datos de prueba
python manage.py shell < scripts/poblar_datos_prueba_v2.py
```

---

## MIGRACIONES EN PRODUCCIÓN

### Checklist Pre-Deployment

- [ ] Crear backup completo de base de datos
- [ ] Probar migraciones en entorno de staging
- [ ] Verificar compatibilidad con datos existentes
- [ ] Planificar ventana de mantenimiento
- [ ] Notificar a usuarios
- [ ] Tener plan de rollback

### Aplicar en Producción

```bash
# 1. Activar modo mantenimiento
python manage.py maintenance on

# 2. Crear backup
pg_dump -U untels_user untels_db > backup_$(date +%Y%m%d_%H%M%S).sql

# 3. Aplicar migraciones
python manage.py migrate --noinput

# 4. Verificar
python manage.py check --deploy

# 5. Desactivar modo mantenimiento
python manage.py maintenance off
```

### Migraciones con Docker

```bash
# Si usas Docker Compose:
docker-compose exec web python manage.py migrate

# Ver logs de migraciones
docker-compose logs web | grep migrate
```

---

## COMANDOS ÚTILES

```bash
# Ver estado de migraciones
python manage.py showmigrations

# Ver migraciones pendientes
python manage.py showmigrations --plan

# Crear migraciones con nombre
python manage.py makemigrations --name add_banco_observaciones

# Fusionar migraciones
python manage.py makemigrations --merge

# Ver SQL de migración
python manage.py sqlmigrate escuelas 0001

# Verificar problemas
python manage.py check

# Ver lista de apps
python manage.py showmigrations --list
```

---

## ESTRUCTURA DE ARCHIVOS DE MIGRACIÓN

```
backend/apps/
├── escuelas/
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py          ← Crear Escuela
├── usuarios/
│   └── migrations/
│       ├── __init__.py
│       ├── 0001_initial.py
│       └── 0002_add_v2_fields.py    ← Agregar roles, escuela
├── observaciones/
│   └── migrations/
│       ├── __init__.py
│       ├── 0001_initial.py
│       └── 0002_banco_docente.py    ← BancoObservacionesDocente
├── informes/
│   └── migrations/
│       ├── __init__.py
│       ├── 0001_initial.py
│       └── 0002_add_v2_states.py    ← Estados y campos v2.0
└── notificaciones/
    └── migrations/
        ├── __init__.py
        └── 0001_initial.py          ← Modelo Notificacion
```

---

## TESTING DE MIGRACIONES

```bash
# 1. Crear base de datos de prueba
createdb untels_db_test

# 2. Aplicar migraciones
python manage.py migrate --database=test

# 3. Ejecutar tests
python manage.py test

# 4. Limpiar
dropdb untels_db_test
```

---

## REFERENCIAS

- [Documentación de Migraciones de Django](https://docs.djangoproject.com/en/4.2/topics/migrations/)
- [Guía de Deployment de Django](https://docs.djangoproject.com/en/4.2/howto/deployment/)
- [PostgreSQL Backup](https://www.postgresql.org/docs/current/backup.html)

---

**Sistema desarrollado para UNTELS**  
**Versión:** 2.0 - Flujo Completo Multi-Rol  
**Fecha:** 29 de Junio de 2026
