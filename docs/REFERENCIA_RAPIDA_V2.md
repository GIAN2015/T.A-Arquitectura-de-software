# REFERENCIA RÁPIDA v2.0

**Sistema de Validación de Informes - UNTELS**

**Versión:** 2.0 - Flujo Completo Multi-Rol  
**Fecha:** 29 de Junio de 2026

---

## 🎯 ESTADO ACTUAL

```
v1.0: ████████████████████████████████████ 100% ✅ FUNCIONAL
v2.0: ████████████████████░░░░░░░░░░░░░░░░  50% 🔄 BACKEND COMPLETO
```

**v2.0 Completado:**
- ✅ Modelos (8 modelos)
- ✅ Servicios (4 servicios, 42 métodos)
- ✅ Vistas (19 vistas)
- ✅ URLs (27 rutas)

**v2.0 Pendiente:**
- ⏳ Templates HTML (~20 archivos)
- ⏳ Migraciones de BD
- ⏳ Testing

---

## 📂 ARCHIVOS CLAVE

### Modelos
```
backend/apps/escuelas/models.py          - Escuela (NUEVO)
backend/apps/usuarios/models.py          - Usuario con 5 roles
backend/apps/informes/models.py          - Informe (11 estados nuevos)
backend/apps/observaciones/models.py     - BancoObservacionesDocente (NUEVO)
backend/apps/notificaciones/models.py    - Notificacion (NUEVO)
```

### Servicios
```
backend/apps/notificaciones/services.py          - NotificacionService (13 métodos)
backend/apps/negocio/servicios/secretaria.py     - SecretariaService (8 métodos)
backend/apps/negocio/servicios/presidente.py     - PresidenteService (10 métodos)
backend/apps/negocio/servicios/docente.py        - DocenteService (13 métodos)
```

### Vistas
```
backend/apps/presentacion/web/auth_views.py          - Login por rol
backend/apps/presentacion/web/secretaria_views.py    - 5 vistas secretaria
backend/apps/presentacion/web/presidente_views.py    - 6 vistas presidente
backend/apps/presentacion/web/docente_views.py       - 6 vistas docente
```

### URLs
```
backend/apps/core/urls.py    - 27 rutas totales
```

### Documentación
```
docs/RESUMEN_EJECUTIVO_V2.md                  - Resumen completo v2.0
docs/PLAN_IMPLEMENTACION_FLUJO_COMPLETO.md    - Plan detallado 6 fases
docs/PROGRESO_IMPLEMENTACION.md               - Seguimiento implementación
docs/GUIA_USO_POR_ROL_V2.md                   - Guía por rol
docs/README_DOCUMENTACION.md                  - Índice de documentación
```

---

## 🔑 COMANDOS ÚTILES

### Desarrollo

#### Activar entorno virtual
```bash
cd backend
source venv/bin/activate
```

#### Ejecutar servidor de desarrollo
```bash
python manage.py runserver
```

#### Crear migraciones (v2.0 - PENDIENTE)
```bash
python manage.py makemigrations escuelas
python manage.py makemigrations usuarios
python manage.py makemigrations observaciones
python manage.py makemigrations informes
python manage.py makemigrations notificaciones
```

#### Aplicar migraciones
```bash
python manage.py migrate
```

#### Crear superusuario
```bash
python manage.py createsuperuser
```

#### Ejecutar tests
```bash
# v1.0 (funcional)
python manage.py test

# v2.0 (pendiente)
# (tests aún no creados)
```

### Datos de Prueba

#### Crear datos de prueba v2.0 (Manualmente)
```python
# En shell de Django
python manage.py shell

# Crear escuela
from apps.escuelas.models import Escuela
from apps.usuarios.models import Usuario

# 1. Crear presidente
presidente = Usuario.objects.create_user(
    username='presidente1',
    password='test123',
    rol='presidente',
    email='presidente@untels.edu.pe',
    activo=True
)

# 2. Crear escuela con presidente
escuela = Escuela.objects.create(
    nombre='Ingeniería de Sistemas e Informática',
    codigo='ISI',
    presidente=presidente,
    activo=True
)

# 3. Asignar escuela al presidente
presidente.escuela = escuela
presidente.save()

# 4. Crear secretaria
secretaria = Usuario.objects.create_user(
    username='secretaria1',
    password='test123',
    rol='secretaria',
    email='secretaria@untels.edu.pe',
    activo=True
)

# 5. Crear docente
docente = Usuario.objects.create_user(
    username='docente1',
    password='test123',
    rol='docente',
    escuela=escuela,
    email='docente@untels.edu.pe',
    activo=True
)

# 6. Crear estudiante
estudiante = Usuario.objects.create_user(
    username='2020123456',
    password='test123',
    rol='estudiante',
    email='estudiante@untels.edu.pe',
    activo=True
)
```

### Verificación

#### Verificar modelos
```bash
python manage.py shell
>>> from apps.escuelas.models import Escuela
>>> from apps.usuarios.models import Usuario
>>> from apps.observaciones.models import BancoObservacionesDocente
>>> from apps.notificaciones.models import Notificacion
>>> from apps.informes.models import Informe
>>> 
>>> # Ver todos los modelos
>>> Escuela.objects.all()
>>> Usuario.objects.filter(rol='presidente')
>>> BancoObservacionesDocente.objects.filter(activo=True)
```

#### Verificar servicios
```bash
python manage.py shell
>>> from apps.notificaciones.services import NotificacionService
>>> from apps.negocio.servicios.secretaria import SecretariaService
>>> from apps.negocio.servicios.presidente import PresidenteService
>>> from apps.negocio.servicios.docente import DocenteService
>>> 
>>> # Probar servicios
>>> NotificacionService.obtener_notificaciones_usuario(usuario_id=1)
```

---

## 🌐 URLS IMPORTANTES

### Autenticación
```
/                              - Redirect según usuario
/login/                        - Login estudiante/egresado
/secretaria/login/             - Login secretaria
/presidente/login/             - Login presidente
/docente/login/                - Login docente
/logout/                       - Cerrar sesión
```

### Secretaria
```
/secretaria/dashboard/              - Dashboard
/secretaria/derivar/<id>/           - Derivar informe a presidente
/secretaria/notificar/<id>/         - Notificar estudiante
/secretaria/ver/<id>/               - Ver informe
/secretaria/notificaciones/         - Gestión de notificaciones
```

### Presidente
```
/presidente/dashboard/              - Dashboard
/presidente/designar/<id>/          - Designar docente
/presidente/revisar/<id>/           - Revisar dictamen (aprobar/rechazar)
/presidente/ver/<id>/               - Ver informe
/presidente/historial/              - Historial de la escuela
/presidente/notificaciones/         - Gestión de notificaciones
```

### Docente
```
/panel-docente/                     - Dashboard
/docente/banco/                     - Gestión de bancos de observaciones
/docente/revisar/<id>/              - Revisar informe con IA
/docente/ver/<id>/                  - Ver informe
/docente/historial/                 - Historial de revisiones
/docente/notificaciones/            - Gestión de notificaciones
```

### Estudiante
```
/upload/                            - Subir informe
/historial/                         - Ver historial de informes
/ver-informe/<id>/                  - Ver detalles de un informe
```

---

## 📊 ESTADOS DEL INFORME

### Estados v2.0 (11 estados nuevos)

| Estado | Código | Descripción | Responsable |
|--------|--------|-------------|-------------|
| 1 | `enviado` | Estudiante envió | Secretaria |
| 2 | `pendiente_secretaria` | En bandeja secretaria | Secretaria |
| 3 | `pendiente_presidente` | Asignado a presidente | Presidente |
| 4 | `pendiente_docente` | Asignado a docente | Docente |
| 5 | `validando_ia` | IA procesando | Sistema |
| 6 | `revision_docente` | Docente revisando | Docente |
| 7 | `pendiente_aprobacion_presidente` | Esperando presidente | Presidente |
| 8 | `aprobado_presidente` | Presidente aprobó | Secretaria |
| 9 | `rechazado_presidente` | Presidente rechazó | Docente |
| 10 | `aprobado_final` | APROBADO (completo) | - |
| 11 | `rechazado_estudiante` | Rechazado, corregir | Estudiante |

### Estados v1.0 (7 estados - deprecados pero funcionales)

| Estado | Código | Descripción |
|--------|--------|-------------|
| 1 | `subido` | Archivo subido |
| 2 | `validando` | IA procesando |
| 3 | `revisando` | Docente revisando |
| 4 | `revision_completada` | Revisión completa |
| 5 | `aprobado` | Aprobado |
| 6 | `rechazado` | Rechazado |
| 7 | `corregido` | Correcciones enviadas |

---

## 👥 ROLES Y PERMISOS

### 5 Roles del Sistema

1. **Estudiante**
   - Subir informes
   - Ver historial
   - Ver observaciones
   - Corregir y reenviar

2. **Egresado**
   - Igual que estudiante

3. **Docente**
   - Gestionar banco de observaciones
   - Revisar informes asignados
   - Validar con IA (usando su banco)
   - Generar dictámenes
   - Reenviar si presidente rechaza

4. **Presidente**
   - Ver informes de su escuela
   - Designar docentes revisores
   - Revisar dictámenes
   - Aprobar o rechazar dictámenes
   - Ver estadísticas de su escuela

5. **Secretaria**
   - Ver todos los informes
   - Derivar a presidentes
   - Notificar estudiantes
   - Ver estadísticas generales

---

## 🔔 TIPOS DE NOTIFICACIONES

### 8 Tipos Implementados

1. **INFORME_ENVIADO** - Estudiante envió informe (→ Secretaria)
2. **INFORME_DERIVADO** - Secretaria derivó (→ Presidente)
3. **DOCENTE_ASIGNADO** - Presidente asignó (→ Docente)
4. **DICTAMEN_ENVIADO** - Docente envió dictamen (→ Presidente)
5. **DICTAMEN_APROBADO** - Presidente aprobó (→ Secretaria)
6. **DICTAMEN_RECHAZADO** - Presidente rechazó (→ Docente)
7. **INFORME_APROBADO** - Aprobado final (→ Estudiante)
8. **INFORME_RECHAZADO** - Rechazado, corregir (→ Estudiante)

---

## 📝 VALIDACIONES IMPORTANTES

### Secretaria
- ✅ Solo puede derivar informes en estado `pendiente_secretaria`
- ✅ Solo puede derivar a escuelas con presidente asignado
- ✅ Solo puede notificar informes en estado `aprobado_presidente`

### Presidente
- ✅ Solo puede designar docentes de su propia escuela
- ✅ Solo puede designar docentes activos
- ✅ Motivo de rechazo mínimo 10 caracteres
- ✅ Solo puede aprobar/rechazar informes en estado `pendiente_aprobacion_presidente`

### Docente
- ✅ Debe tener banco de observaciones activo para revisar
- ✅ Solo un banco activo a la vez
- ✅ Dictamen mínimo 20 caracteres
- ✅ Solo puede revisar informes asignados a él
- ✅ Archivo de banco debe ser PDF o DOCX

### Estudiante
- ✅ Solo puede ver sus propios informes
- ✅ Archivo debe ser PDF o DOCX
- ✅ Tamaño máximo configurable

---

## 🗄️ CAMPOS NUEVOS EN MODELOS

### Usuario
```python
rol = CharField  # estudiante, egresado, docente, presidente, secretaria
escuela = ForeignKey(Escuela)  # NUEVO
email = EmailField  # NUEVO
activo = BooleanField  # NUEVO
```

### Informe
```python
# Campos nuevos
estado = CharField  # 11 estados nuevos
secretaria_asignada = ForeignKey(Usuario)
presidente_asignado = ForeignKey(Usuario)
docente_asignado = ForeignKey(Usuario)
escuela = ForeignKey(Escuela)
banco_observaciones_usado = ForeignKey(BancoObservacionesDocente)
dictamen_docente = TextField
comentario_presidente = TextField
motivo_rechazo_presidente = TextField
recomendacion_docente = CharField  # 'aprobar' o 'rechazar'

# Fechas
fecha_envio = DateTimeField
fecha_derivacion_secretaria = DateTimeField
fecha_asignacion_presidente = DateTimeField
fecha_asignacion_docente = DateTimeField
fecha_revision_docente = DateTimeField
fecha_revision_presidente = DateTimeField
```

### BancoObservacionesDocente (NUEVO)
```python
docente = ForeignKey(Usuario)
nombre = CharField
archivo = FileField
contenido_extraido = TextField
activo = BooleanField
fecha_creacion = DateTimeField
```

### Escuela (NUEVO)
```python
nombre = CharField
codigo = CharField
presidente = ForeignKey(Usuario)
activo = BooleanField
```

### Notificacion (NUEVO)
```python
usuario = ForeignKey(Usuario)
tipo = CharField  # 8 tipos
titulo = CharField
mensaje = TextField
informe = ForeignKey(Informe, null=True)
leida = BooleanField
fecha_creacion = DateTimeField
fecha_lectura = DateTimeField
```

---

## 🛠️ SERVICIOS DISPONIBLES

### NotificacionService (13 métodos)
```python
crear_notificacion(usuario, tipo, titulo, mensaje, informe=None)
notificar_secretaria_informe_enviado(informe)
notificar_presidente_informe_derivado(informe)
notificar_docente_asignado(informe)
notificar_presidente_dictamen_enviado(informe)
notificar_secretaria_dictamen_aprobado(informe)
notificar_docente_dictamen_rechazado(informe, motivo)
notificar_estudiante_aprobado(informe)
notificar_estudiante_rechazado(informe)
obtener_notificaciones_usuario(usuario_id, solo_no_leidas=False)
marcar_como_leida(notificacion_id)
contar_no_leidas(usuario_id)
obtener_tipos_notificacion()
```

### SecretariaService (8 métodos)
```python
obtener_informes_pendientes()
obtener_informes_derivados()
obtener_informes_aprobados_pendientes_notificar()
derivar_a_presidente(informe_id, escuela_id, usuario_secretaria_id)
notificar_estudiante(informe_id, usuario_secretaria_id)
obtener_informe(informe_id)
obtener_estadisticas()
obtener_escuelas_activas()
```

### PresidenteService (10 métodos)
```python
obtener_informes_pendientes_asignar(escuela_id)
obtener_informes_en_revision(escuela_id)
obtener_informes_pendientes_aprobar(escuela_id)
designar_docente(informe_id, docente_id, usuario_presidente_id)
aprobar_dictamen(informe_id, usuario_presidente_id, comentario="")
rechazar_dictamen(informe_id, usuario_presidente_id, motivo)
obtener_informe(informe_id, escuela_id)
obtener_historial_escuela(escuela_id)
obtener_estadisticas_escuela(escuela_id)
obtener_docentes_escuela(escuela_id)
```

### DocenteService (13 métodos)
```python
obtener_bancos_docente(docente_id)
obtener_banco_activo(docente_id)
crear_banco(docente_id, nombre, archivo)
activar_banco(banco_id, docente_id)
eliminar_banco(banco_id, docente_id)
extraer_contenido_pdf(archivo)
extraer_contenido_docx(archivo)
obtener_informes_asignados(docente_id)
obtener_informes_revisados(docente_id)
validar_informe_con_banco(informe_id, docente_id)
enviar_dictamen(informe_id, docente_id, dictamen, recomendacion)
obtener_informe(informe_id, docente_id)
obtener_estadisticas_docente(docente_id)
```

---

## 🧪 TESTING

### Tests v1.0 (18 tests - PASANDO)
```bash
python manage.py test apps.informes.tests
python manage.py test apps.usuarios.tests
```

### Tests v2.0 (PENDIENTES)
```bash
# Pendiente de crear:
# - tests/test_escuelas.py
# - tests/test_notificaciones.py
# - tests/test_servicios_secretaria.py
# - tests/test_servicios_presidente.py
# - tests/test_servicios_docente.py
# - tests/test_flujo_completo.py
```

---

## 📦 DEPENDENCIAS

### Python Packages
```
Django==4.2.7
psycopg2-binary==2.9.9
python-docx==1.1.0
pypdf==3.17.1
groq==0.4.1
python-dotenv==1.0.0
```

### Nuevas Dependencias v2.0
```
python-docx  # Extracción de texto de DOCX
pypdf        # Extracción de texto de PDF
```

---

## 🐛 TROUBLESHOOTING

### Problema: Migraciones no aplicadas
```bash
# Solución:
python manage.py makemigrations
python manage.py migrate
```

### Problema: No puedo crear banco de observaciones
```bash
# Verificar:
1. Usuario es docente
2. Archivo es PDF o DOCX
3. Contenido tiene mínimo 50 caracteres

# Shell:
python manage.py shell
>>> from apps.observaciones.models import BancoObservacionesDocente
>>> banco = BancoObservacionesDocente.objects.get(id=1)
>>> banco.contenido_extraido
```

### Problema: IA no valida con mi banco
```bash
# Verificar:
1. Tienes un banco activo
2. El banco tiene contenido extraído
3. Groq API key está configurada

# Shell:
>>> from apps.negocio.servicios.docente import DocenteService
>>> banco = DocenteService.obtener_banco_activo(docente_id=1)
>>> print(banco.contenido_extraido)
```

### Problema: No recibo notificaciones
```bash
# Verificar en shell:
>>> from apps.notificaciones.models import Notificacion
>>> Notificacion.objects.filter(usuario_id=1)
>>> 
>>> from apps.notificaciones.services import NotificacionService
>>> NotificacionService.contar_no_leidas(usuario_id=1)
```

### Problema: No puedo derivar informe
```bash
# Verificar:
1. El informe está en estado 'pendiente_secretaria'
2. La escuela tiene presidente asignado
3. Eres secretaria

# Shell:
>>> from apps.informes.models import Informe
>>> informe = Informe.objects.get(id=1)
>>> print(informe.estado)
>>> 
>>> from apps.escuelas.models import Escuela
>>> escuela = Escuela.objects.get(id=1)
>>> print(escuela.presidente)
```

---

## 📚 DOCUMENTACIÓN ADICIONAL

### Leer en orden:
1. `RESUMEN_EJECUTIVO_V2.md` - Overview completo (10 min)
2. `GUIA_USO_POR_ROL_V2.md` - Cómo usar el sistema (20 min)
3. `PLAN_IMPLEMENTACION_FLUJO_COMPLETO.md` - Plan detallado (60 min)
4. `PROGRESO_IMPLEMENTACION.md` - Implementación detallada (30 min)

### Documentación v1.0:
- `QUE_FALTA_HACER.md` - Estado v1.0
- `ARQUITECTURA_POR_CAPAS.md` - Arquitectura
- `CAPA_*.md` - Documentación por capa

---

## 🚀 PRÓXIMOS PASOS

### Para completar v2.0:

1. **Crear Templates (6-8h)**
   - 20 templates HTML con Bootstrap
   - Formularios y tablas
   - Navegación y mensajes

2. **Aplicar Migraciones (30 min)**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Poblar Datos de Prueba (1h)**
   - Crear escuelas
   - Crear usuarios por rol
   - Crear bancos de observaciones

4. **Testing (4-5h)**
   - Tests de modelos
   - Tests de servicios
   - Tests de vistas
   - Tests de flujo completo

5. **Deployment (2-3h)**
   - Configurar producción
   - Variables de entorno
   - Docker compose
   - Deploy

**Total estimado:** 13-17 horas

---

## 💡 TIPS Y MEJORES PRÁCTICAS

### Para Docentes
- Mantén tu banco de observaciones actualizado
- Usa formato claro en tu archivo PDF/DOCX
- Solo ten un banco activo a la vez
- Revisa cuidadosamente las observaciones de la IA

### Para Presidentes
- Asigna docentes especializados según el tema
- Da feedback claro al rechazar dictámenes
- Revisa el historial de cada docente

### Para Secretarias
- Verifica la escuela correcta antes de derivar
- Mantén comunicación con presidentes
- Notifica rápidamente a estudiantes

### Para Estudiantes
- Sigue el formato del reglamento UNTELS
- Revisa todas las observaciones antes de corregir
- No reenvíes sin hacer correcciones

---

## 📞 CONTACTO Y SOPORTE

**Documentación completa:**
- `/docs/` - Todos los documentos

**Código fuente:**
- `/backend/apps/` - Código del sistema

**Configuración:**
- `/backend/apps/core/settings.py` - Settings Django
- `/backend/.env` - Variables de entorno

---

**Sistema desarrollado para UNTELS**  
**Versión:** 2.0 - Flujo Completo Multi-Rol  
**Estado:** Backend 100%, Templates 0%  
**Fecha:** 29 de Junio de 2026  

**Referencia rápida actualizada**
