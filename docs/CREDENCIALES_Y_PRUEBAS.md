# HOJA DE CREDENCIALES Y CASOS DE PRUEBA
## Sistema de Validación de Informes PPP - UNTELS

---

## 1. CREDENCIALES DE ACCESO

### ALUMNO 1 (Principal)
```
┌────────────────────────────────────────────────┐
│  Portal:    Estudiantes                        │
│  URL:       http://127.0.0.1:8000/             │
│  Código:    2213110416                         │
│  Nombre:    Andre Mendoza Quispe               │
│  Password:  alumno123                          │
└────────────────────────────────────────────────┘
```

### ALUMNO 2 (Secundario)
```
┌────────────────────────────────────────────────┐
│  Portal:    Estudiantes                        │
│  URL:       http://127.0.0.1:8000/             │
│  Código:    2213110417                         │
│  Nombre:    María Fernández López              │
│  Password:  alumno123                          │
└────────────────────────────────────────────────┘
```

### DOCENTE
```
┌────────────────────────────────────────────────┐
│  Portal:    Docentes                           │
│  URL:       http://127.0.0.1:8000/docente/login/│
│  Código:    DOC001                             │
│  Nombre:    Dr. Carlos Ramírez Torres          │
│  Password:  docente123                         │
└────────────────────────────────────────────────┘
```

---

## 2. FLUJO COMPLETO DE PRUEBA (END-TO-END)

### ESCENARIO 1: Flujo Normal (Alumno → IA → Docente → Aprobación)

#### Paso 1.1 - Alumno sube informe
1. Ir a: `http://127.0.0.1:8000/`
2. Login con: `2213110416` / `alumno123`
3. Aparece pantalla de carga de informe
4. Click en "Seleccionar archivo" y elegir un .docx o .pdf
5. Click en "🤖 Validar Informe con IA"
6. **Sistema:**
   - Extrae texto del .docx o .pdf
   - La IA analiza el contenido
   - Genera observaciones automáticamente
7. **Resultado esperado:** Pantalla con observaciones detectadas

#### Paso 1.2 - Docente revisa el informe
1. Cerrar sesión del alumno
2. Ir a: `http://127.0.0.1:8000/docente/login/`
3. Login con: `DOC001` / `docente123`
4. Panel docente muestra el informe pendiente
5. Click en "⚙️ Revisar" del informe del alumno
6. **Sistema:** Cambia estado a "En Revisión Docente"
7. Para cada observación:
   - Elegir "Confirmar" o "Descartar"
   - Cambiar severidad si es necesario
   - Añadir comentario opcional
8. Escribir comentario general
9. Click en "✓ APROBAR INFORME"
10. **Resultado esperado:** Estado cambia a "Aprobado"

#### Paso 1.3 - Alumno ve aprobación
1. Cerrar sesión del docente
2. Login alumno: `2213110416` / `alumno123`
3. Click en "📋 Mi Historial"
4. **Resultado esperado:** Informe con estado "✅ Aprobado"
5. Click "👁️ Ver Detalle"
6. **Resultado esperado:** Ve mensaje de aprobación + comentarios del docente

---

### ESCENARIO 2: Flujo con Rechazo y Reenvío

#### Paso 2.1 - Alumno 2 sube informe deficiente
1. Login: `2213110417` / `alumno123`
2. Subir informe corto/incompleto
3. **Sistema:** IA detecta muchas observaciones

#### Paso 2.2 - Docente rechaza
1. Login docente: `DOC001` / `docente123`
2. Click en "⚙️ Revisar"
3. Confirmar todas las observaciones críticas
4. Escribir comentario: "Por favor agregar más contenido y secciones faltantes"
5. Click en "✗ RECHAZAR PARA CORRECCIÓN"
6. **Resultado esperado:** Estado "Rechazado"

#### Paso 2.3 - Alumno 2 ve rechazo
1. Login alumno: `2213110417` / `alumno123`
2. Click en "📋 Mi Historial"
3. **Resultado esperado:** Informe con estado "❌ Rechazado"
4. Aparece botón "📤 Reenviar"

#### Paso 2.4 - Alumno 2 reenvía corregido
1. Click en "📤 Reenviar"
2. Subir versión corregida del informe
3. **Sistema:**
   - Detecta que es un reenvío
   - Versión = 2
   - Vincula con informe anterior
4. **Resultado esperado:** Mensaje "Detectado reenvío - Versión 2 del informe"

#### Paso 2.5 - Docente vuelve a revisar
1. Login docente: `DOC001` / `docente123`
2. **Resultado esperado:** Ve la nueva versión v2
3. Revisa, aprueba o rechaza
4. El historial del alumno muestra ambas versiones

---

### ESCENARIO 3: Validación de Permisos

#### Test 3.1 - Alumno intenta acceder a panel docente
1. Login como alumno
2. Ir a: `http://127.0.0.1:8000/panel-docente/`
3. **Resultado esperado:** Redirige al login con mensaje "Acceso denegado"

#### Test 3.2 - Docente intenta usar login de alumnos
1. Ir a: `http://127.0.0.1:8000/`
2. Intentar login con: `DOC001` / `docente123`
3. **Resultado esperado:** Error "Los docentes deben usar el portal de docentes"

#### Test 3.3 - Alumno intenta ver informe de otro alumno
1. Login como Alumno 1
2. Acceder a URL del informe del Alumno 2
3. **Resultado esperado:** "No tienes permiso para ver este informe"

---

## 3. CHECKLIST DE PRUEBAS

### Autenticación
- [ ] Login alumno con credenciales correctas → Funciona
- [ ] Login docente con credenciales correctas → Funciona
- [ ] Login con password incorrecto → Rechaza
- [ ] Login con código inexistente → Rechaza
- [ ] Alumno NO puede entrar por login docente → Bloquea
- [ ] Docente NO puede entrar por login alumno → Bloquea
- [ ] Cerrar sesión → Vuelve al login correcto

### Funciones del Alumno
- [ ] Ver pantalla de subida de informe
- [ ] Subir archivo .docx o .pdf → IA procesa automáticamente
- [ ] Subir archivo .pdf → Rechaza
- [ ] Subir archivo > 10MB → Rechaza
- [ ] Subir archivo vacío → Rechaza
- [ ] Ver resultado de validación con observaciones
- [ ] Ver mi historial de informes
- [ ] Si está rechazado, puedo reenviar
- [ ] Reenvío incrementa versión correctamente
- [ ] Reenvío vincula con informe anterior

### Funciones del Docente
- [ ] Panel docente muestra estadísticas
- [ ] Filtrar por: Pendientes, Aprobados, Rechazados, Todos
- [ ] Click "Revisar" cambia estado a "En Revisión"
- [ ] Ver observaciones generadas por la IA agrupadas por severidad
- [ ] Confirmar/Descartar cada observación individualmente
- [ ] Cambiar severidad de observación
- [ ] Añadir comentario por observación
- [ ] Añadir comentario general al informe
- [ ] Aprobar informe → Estado "Aprobado"
- [ ] Rechazar informe → Estado "Rechazado"
- [ ] Después de aprobar/rechazar, alumno ve el resultado

### Integración con IA
- [ ] Sin GROQ_API_KEY → Usa validación local (8-10 observaciones)
- [ ] Con GROQ_API_KEY válida → Usa Llama 3.3 70B
- [ ] Si GROQ falla → Fallback a validación local
- [ ] Observaciones tienen: sección, descripción, ubicación, severidad

### Estados del Informe
- [ ] ENVIADO → al subir archivo
- [ ] VALIDANDO → mientras IA procesa
- [ ] OBSERVADO → después de validación con observaciones
- [ ] EN_REVISION_DOCENTE → cuando docente abre revisión
- [ ] APROBADO → docente acepta
- [ ] RECHAZADO → docente rechaza
- [ ] Reenvío: nueva versión, mismo flujo

---

## 4. CASOS DE BORDE Y ERRORES

### Caso 1: Archivo corrupto
**Acción:** Subir .docx o .pdf corrupto
**Esperado:** Mensaje "Archivo dañado o formato incorrecto"

### Caso 2: Archivo casi vacío
**Acción:** Subir .docx o .pdf con < 50 caracteres
**Esperado:** Mensaje "Archivo vacío o tiene muy poco contenido"

### Caso 3: Sin internet (sin GROQ)
**Acción:** Subir informe sin API Key
**Esperado:** IA local procesa con heurísticas

### Caso 4: Sesión expirada
**Acción:** Acceder a página interna sin sesión
**Esperado:** Redirige al login

### Caso 5: Doble envío rápido
**Acción:** Click rápido en submit múltiples veces
**Esperado:** Botón se deshabilita, solo crea 1 informe

---

## 5. ARCHIVOS DE PRUEBA SUGERIDOS

Para probar correctamente, prepara estos archivos .docx o .pdf:

### informe_bueno.docx
- Tiene carátula con "UNTELS"
- Tiene índice, introducción, conclusiones
- Más de 1500 palabras
- Menciona empresa, actividades, objetivos
- **Esperado:** Pocas o ninguna observación

### informe_malo.docx
- Sin carátula
- Sin índice ni conclusiones
- Menos de 500 palabras
- Sin mencionar empresa
- **Esperado:** 8-10 observaciones críticas

### informe_corregido.docx
- Versión mejorada del informe_malo
- Con secciones añadidas
- **Esperado:** Menos observaciones, listo para aprobar

---

## 6. INICIO DEL SERVIDOR

```bash
cd backend
source venv/bin/activate
python manage.py runserver
```

URLs:
- Estudiantes: http://127.0.0.1:8000/
- Docentes: http://127.0.0.1:8000/docente/login/
- Admin Django: http://127.0.0.1:8000/admin/

---

## 7. ARQUITECTURA DEL FLUJO

```
┌─────────────────┐
│     ALUMNO      │
│  2213110416     │
└────────┬────────┘
         │ 1. Sube .docx o .pdf
         ▼
┌─────────────────┐
│  SISTEMA WEB    │
│   (Django)      │
└────────┬────────┘
         │ 2. Extrae contenido
         ▼
┌─────────────────┐         ┌─────────────────┐
│   IA (GROQ)     │◄────────│  REGLAMENTO    │
│  Llama 3.3 70B  │         │  BANCO OBS.    │
└────────┬────────┘         └─────────────────┘
         │ 3. Genera observaciones
         ▼
┌─────────────────┐
│  OBSERVACIONES  │
│   GENERADAS     │
│  (Pendientes)   │
└────────┬────────┘
         │ 4. Esperan revisión
         ▼
┌─────────────────┐
│    DOCENTE      │
│    DOC001       │
└────────┬────────┘
         │ 5. Confirma/descarta
         │    Aprueba/Rechaza
         ▼
┌─────────────────┐
│   DECISIÓN      │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
APROBADO  RECHAZADO
              │
              │ 6. Alumno reenvía
              │    Vuelve al paso 2
              ▼
         Nueva versión
```

---

## 8. PROBLEMAS CONOCIDOS Y SOLUCIONES

### Problema: "no such table: usuario"
**Solución:**
```bash
python manage.py migrate
```

### Problema: La IA no genera observaciones
**Solución:** Verificar que el archivo .env tenga GROQ_API_KEY o aceptar que use IA local

### Problema: Docente no ve el informe nuevo
**Solución:** Verificar filtro "Pendientes" en el panel docente

### Problema: Alumno no puede reenviar
**Solución:** Solo se puede reenviar si el informe está en estado "Rechazado"

---

## 9. RESUMEN DE BUGS CORREGIDOS

| # | Bug | Estado |
|---|-----|--------|
| 1 | `observaciongenerada_set` no existe (es `observaciones`) | ✅ Corregido |
| 2 | Estados de informe desactualizados en historial | ✅ Corregido |
| 3 | IA sin fallback cuando no hay API Key | ✅ Corregido |
| 4 | Informe queda colgado si IA falla | ✅ Corregido |
| 5 | Versionado solo funcionaba con estado RECHAZADO | ✅ Corregido |
| 6 | Panel docente mostraba TODOS los informes | ✅ Corregido |
| 7 | No cambiaba estado a EN_REVISION_DOCENTE | ✅ Corregido |
| 8 | Estudiante veía link a panel docente | ✅ Corregido |
| 9 | Botón "Inicio" llevaba a página incorrecta | ✅ Corregido |
| 10 | Sin control de acceso a informes ajenos | ✅ Corregido |
| 11 | No validaba tamaño de archivo | ✅ Corregido |
| 12 | No detectaba archivo vacío o corrupto | ✅ Corregido |
| 13 | Docente podía registrarse desde formulario público | ✅ Corregido |

---

## 10. EQUIPO Y DOCUMENTACIÓN

**Sistema desarrollado para:** UNTELS - Trabajo Académico
**Tipo:** Aplicación web Django con IA
**Funcionalidad principal:** Validación automática de informes PPP

**Archivos importantes:**
- `apps/observaciones/services.py` → Lógica de IA
- `apps/core/views.py` → Vistas principales
- `apps/core/admin_views.py` → Vistas del docente
- `templates/` → Interfaces

**Estado:** ✅ LISTO PARA USAR
