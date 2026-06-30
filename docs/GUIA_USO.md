# Sistema de Validación de Informes de Prácticas Preprofesionales - UNTELS

## Descripción del Sistema

Sistema web Django que valida automáticamente informes de prácticas preprofesionales usando IA (GROQ API) y permite la revisión docente posterior.

### Flujo Completo del Sistema

```
ALUMNO → Sube Informe (.docx o .pdf)
   ↓
IA (GROQ) → Valida contra Reglamento y Banco de Observaciones
   ↓
OBSERVACIONES GENERADAS → Enviadas a revisión docente
   ↓
DOCENTE → Revisa y confirma/descarta observaciones
   ↓
DECISIÓN DOCENTE → Aprobar / Rechazar
   ↓
ALUMNO → Recibe resultado (si rechazado, puede reenviar corregido)
```

---

## Configuración Inicial

### 1. Activar entorno virtual y ejecutar servidor

```bash
cd backend
source venv/bin/activate
python manage.py runserver
```

### 2. Configurar API Key de GROQ (para IA)

Edita el archivo `.env`:

```env
GROQ_API_KEY=tu_api_key_aqui
```

**Obtener API Key gratis:**
1. Visita: https://console.groq.com/
2. Crea una cuenta
3. Ve a "API Keys" y genera una nueva
4. Copia y pega en `.env`

### 3. Datos iniciales ya poblados

✓ Reglamento de informes PPP
✓ Banco de 10 observaciones frecuentes
✓ Usuarios de prueba

---

## Credenciales de Acceso

### Portal Estudiantes
- **URL:** http://127.0.0.1:8000/
- **Código:** 2021101234
- **Contraseña:** estudiante123

### Portal Docentes
- **URL:** http://127.0.0.1:8000/docente/login/
- **Código:** DOCENTE001
- **Contraseña:** docente123

### Panel Admin Django
- **URL:** http://127.0.0.1:8000/admin/
- **Usuario:** admin
- **Contraseña:** admin123

---

## Funcionalidades por Rol

### ESTUDIANTES / EGRESADOS

**1. Registro de cuenta**
- Ir a http://127.0.0.1:8000/registro/
- Completar datos: código, nombre, contraseña
- Seleccionar tipo: Estudiante o Egresado

**2. Subir informe**
- Login en portal estudiantes
- Click en "Subir Informe"
- Seleccionar archivo .docx o .pdf
- El sistema automáticamente:
  - Extrae el contenido del documento
  - Lo envía a la IA para validación
  - Genera observaciones basadas en el reglamento
  - Cambia estado a "Con Observaciones" o "Completado"

**3. Ver resultados**
- Ver observaciones generadas por la IA
- Ver estado del informe
- Si es rechazado por docente, puede reenviar versión corregida

**4. Historial**
- Ver todos los informes enviados
- Ver versiones anteriores
- Seguimiento de estados

### DOCENTES

**1. Panel Principal**
- Ver todos los informes de estudiantes
- Filtrar por estado
- Ver estadísticas generales

**2. Revisar Informe**
- Ver observaciones generadas por IA
- Para cada observación:
  - Confirmar (es válida)
  - Descartar (no aplica)
  - Añadir comentario
  - Cambiar severidad (crítica, importante, menor, sugerencia)
- Decisión final:
  - **Aprobar:** Informe pasa
  - **Rechazar:** Estudiante debe corregir y reenviar

**3. Gestión del Sistema**
- **Reglamento:** Actualizar reglas de evaluación
- **Banco de Observaciones:** Agregar/eliminar observaciones frecuentes
- **Usuarios:** Ver listado de estudiantes
- **Reportes:** Estadísticas y métricas del sistema

---

## Estados del Informe

| Estado | Descripción |
|--------|-------------|
| **Enviado** | Alumno subió el archivo, esperando validación IA |
| **Validando** | IA está procesando el documento |
| **Observado** | IA encontró observaciones, esperando revisión docente |
| **En Revisión Docente** | Docente está evaluando |
| **Aprobado** | Docente aprobó el informe ✓ |
| **Rechazado** | Docente rechazó, alumno debe corregir |
| **Completado** | Proceso finalizado exitosamente |

---

## Integración con IA (GROQ)

### ¿Cómo funciona?

1. **Modelo usado:** `llama-3.3-70b-versatile`
2. **Proceso:**
   - Extrae texto del .docx o .pdf
   - Compara con el reglamento activo
   - Consulta banco de observaciones frecuentes
   - Genera observaciones en formato JSON
3. **Resultado:** Lista de observaciones con:
   - Sección afectada
   - Descripción del problema
   - Ubicación del error

### Archivo de servicio IA
`apps/observaciones/services.py:14` - Función `validar_informe()`

---

## Arquitectura del Sistema

### Estructura de Apps

```
backend/
├── apps/
│   ├── usuarios/          # Gestión de usuarios (estudiantes, docentes)
│   ├── informes/          # Informes subidos y su contenido
│   ├── reglamento/        # Reglamento institucional
│   ├── observaciones/     # Banco y observaciones generadas
│   └── core/              # Vistas principales y navegación
├── templates/             # HTML templates
└── config/                # Configuración Django
```

### Modelos Principales

**Usuario**
- codigo (único)
- nombre
- tipo_usuario (estudiante/egresado/docente)
- password (hasheado)

**Informe**
- usuario (FK)
- nombre_archivo
- contenido (texto extraído)
- estado
- docente_revisor (FK)
- version
- informe_anterior (FK para versionado)

**ObservacionGenerada**
- informe (FK)
- seccion
- observacion
- ubicacion_error
- estado (pendiente/confirmada/descartada)
- severidad
- comentario_docente

**BancoObservaciones**
- seccion
- descripcion

**Reglamento**
- nombre
- contenido
- activo (boolean)

---

## Comandos Útiles

### Crear nuevo usuario docente
```bash
python manage.py shell -c "
from apps.usuarios.models import Usuario
docente = Usuario.objects.create(codigo='DOCENTE002', nombre='Nombre Apellido', tipo_usuario='docente')
docente.set_password('contraseña123')
print('Docente creado')
"
```

### Ver informes en base de datos
```bash
python manage.py shell -c "
from apps.informes.models import Informe
for inf in Informe.objects.all():
    print(f'{inf.id}: {inf.nombre_archivo} - {inf.estado}')
"
```

### Actualizar reglamento
```bash
python manage.py shell -c "
from apps.reglamento.models import Reglamento
Reglamento.objects.all().update(activo=False)
nuevo = Reglamento.objects.create(
    nombre='Reglamento 2025',
    contenido='...',
    activo=True
)
print('Reglamento actualizado')
"
```

---

## Solución de Problemas

### Error: "no such table: usuario"
```bash
python manage.py makemigrations
python manage.py migrate
```

### Error: "GROQ_API_KEY not found"
1. Verifica que `.env` existe
2. Añade: `GROQ_API_KEY=tu_clave_aqui`
3. Reinicia el servidor

### IA no genera observaciones
1. Verifica que GROQ_API_KEY es válida
2. Revisa que hay reglamento activo
3. Revisa que hay observaciones en el banco
4. Verifica conexión a internet

### Login no funciona
1. Verifica que el usuario existe
2. Usa el portal correcto (estudiantes vs docentes)
3. Verifica que la contraseña es correcta

---

## Tecnologías Utilizadas

- **Backend:** Django 5.0.6
- **Base de datos:** SQLite (dev) / PostgreSQL (producción)
- **IA:** GROQ API (Llama 3.3 70B)
- **Procesamiento:** python-docx (lectura de Word)
- **Frontend:** Bootstrap 5 + Templates Django

---

## Próximos Pasos / Mejoras Futuras

- [ ] Exportar observaciones a PDF
- [ ] Notificaciones por email
- [ ] Dashboard con gráficos
- [ ] Comparación de versiones de informes
- [ ] Sistema de calificación numérica
- [ ] Integración con sistema académico UNTELS

---

## Soporte

Para problemas o dudas:
1. Revisa esta guía
2. Verifica logs del servidor
3. Usa `python manage.py check` para validar configuración
