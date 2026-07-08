# ✅ PRUEBA DEL FLUJO COMPLETO - PASO A PASO

## 🎯 TODO CORREGIDO Y LISTO

- ✅ Template de secretaria corregido (`username` → `codigo` y `nombre`)
- ✅ Base de datos limpia (solo usuarios y escuela)
- ✅ Flujo v2.0 implementado completo
- ✅ Sesiones múltiples por pestaña funcionando

---

## 🧪 PRUEBA AHORA - SIGUE ESTOS PASOS EXACTOS

### PASO 1: ESTUDIANTE ENVÍA INFORME

**Pestaña 1:**
1. Ir a: http://localhost:8000/
2. Login: `2020123456` / `test123`
3. Click en "Subir Informe"
4. Seleccionar cualquier archivo PDF o DOCX
5. Click "Subir Informe"

**✅ Verás:**
```
Informe "archivo.pdf" enviado correctamente.
Próximos pasos:
1. La Secretaría Académica derivará tu informe al Presidente de Escuela
2. El Presidente asignará un Docente revisor
3. El Docente validará tu informe con IA
4. Recibirás el resultado final
```

6. Ir a "Mis Informes" → Verás el informe con estado "Enviado por Estudiante"

---

### PASO 2: SECRETARIA DERIVA A PRESIDENTE

**Pestaña 2 (NUEVA PESTAÑA):**
1. Ir a: http://localhost:8000/secretaria/login/
2. Login: `secretaria1` / `test123`
3. En el Dashboard verás: "Informes Recibidos (1)"
4. En la tabla verás:
   - Estudiante: **José Gonzales**
   - Código: 2020123456
   - Archivo del informe
5. Click en "Derivar"
6. Seleccionar Escuela: **Ingeniería de Sistemas e Informática (ISI)**
7. (Opcional) Comentario: "Informe recibido, derivando a ISI"
8. Click "Derivar a Presidente"

**✅ Verás:**
```
Informe derivado exitosamente a Ingeniería de Sistemas e Informática
```

---

### PASO 3: PRESIDENTE ASIGNA DOCENTE

**Pestaña 3 (NUEVA PESTAÑA):**
1. Ir a: http://localhost:8000/presidente/login/
2. Login: `presidente_isi` / `test123`
3. En el Dashboard verás: "Pendientes de Asignar Docente (1)"
4. En la tabla verás el informe
5. Click en "Designar Docente"
6. Seleccionar Docente: **Ing. Carlos Ramírez (docente_isi_1)**
7. (Opcional) Comentario: "Asignando al docente especialista"
8. Click "Asignar Docente"

**✅ Verás:**
```
Docente Ing. Carlos Ramírez asignado exitosamente.
```

---

### PASO 4: DOCENTE CREA BANCO (Primera vez)

**Pestaña 4 (NUEVA PESTAÑA):**
1. Ir a: http://localhost:8000/docente/login/
2. Login: `docente_isi_1` / `test123`
3. Ir a "Mi Banco"
4. En "Crear Nuevo Banco":
   - Nombre: `Observaciones Generales 2026`
   - Archivo: Subir un PDF o DOCX con observaciones
     (Puede ser cualquier documento de texto con observaciones comunes)
5. Click "Crear Banco"

**✅ Verás:**
```
Banco "Observaciones Generales 2026" creado y activado exitosamente.
```

**Contenido ejemplo para el banco (puedes crear un .txt y renombrarlo a .docx):**
```
OBSERVACIONES COMUNES PARA INFORMES DE PRÁCTICAS

1. CARÁTULA
- Falta el logo de la UNTELS
- Datos incompletos del estudiante
- Falta el nombre del asesor

2. FORMATO
- Interlineado incorrecto (debe ser 1.5)
- Márgenes no cumplen con el reglamento
- Fuente incorrecta (debe ser Arial 12 o Times 12)

3. CONTENIDO
- Falta índice
- Introducción muy breve
- Falta descripción de la empresa
- Actividades poco detalladas
- Conclusiones insuficientes
- Referencias bibliográficas en formato incorrecto

4. NORMAS APA
- Citas mal formateadas
- Referencias incompletas
- Falta bibliografía
```

---

### PASO 5: DOCENTE VALIDA CON IA

**Misma Pestaña 4:**
1. Volver a "Dashboard"
2. Verás: "Informes Asignados (1)"
3. Click en "Revisar" en el informe
4. El sistema automáticamente:
   - Detecta que tienes banco activo
   - Si tienes GROQ_API_KEY: Usa IA para validar
   - Si NO tienes: Usa validación local
5. Verás tabla de observaciones generadas
6. Para cada observación puedes:
   - ✅ Confirmar
   - ❌ Descartar  
   - ✏️ Editar
7. Después de revisar, al final del formulario:
   - Seleccionar: **Aprobar** o **Rechazar**
   - Comentario: "El informe presenta observaciones menores" (o lo que corresponda)
8. Click "Enviar Dictamen"

**✅ Verás:**
```
Dictamen enviado exitosamente al Presidente para su aprobación.
```

---

### PASO 6: PRESIDENTE APRUEBA DICTAMEN

**Volver a Pestaña 3:**
1. Refrescar página o volver a Dashboard
2. Verás: "Dictámenes Pendientes (1)"
3. Click en "Revisar Dictamen"
4. Verás:
   - Comentario del docente
   - Observaciones encontradas
   - Recomendación
5. Decidir: **Aprobar Dictamen** o **Rechazar Dictamen**
6. Comentario: "Dictamen correcto, se aprueba"
7. Click en confirmar

**✅ Verás:**
```
Dictamen aprobado exitosamente.
```

---

### PASO 7: SECRETARIA NOTIFICA A ESTUDIANTE

**Volver a Pestaña 2:**
1. Refrescar página o volver a Dashboard
2. Verás: "Listos para Notificar (1)"
3. Click en "Notificar Estudiante"
4. Revisar información
5. Click "Confirmar Notificación"

**✅ Verás:**
```
Estudiante notificado exitosamente.
```

---

### PASO 8: ESTUDIANTE RECIBE RESULTADO

**Volver a Pestaña 1:**
1. Refrescar página o volver a Dashboard
2. Ir a "Mis Informes"
3. Verás el informe con estado actualizado:
   - **APROBADO FINAL** (si fue aprobado)
   - **Rechazado - Estudiante debe Corregir** (si fue rechazado)
4. Click en el informe para ver detalles
5. Ver:
   - Observaciones (si las hay)
   - Comentarios de cada rol
   - Fechas de cada etapa

**Si fue rechazado:**
- Puede subir nueva versión corregida
- El flujo comienza de nuevo

---

## 🔍 VERIFICAR ESTADO EN BASE DE DATOS

```bash
cd backend
./venv/bin/python manage.py shell <<'EOF'
from apps.informes.models import Informe

informe = Informe.objects.latest('id')

print(f"\n📄 INFORME #{informe.id}")
print(f"   Archivo: {informe.nombre_archivo}")
print(f"   Estado: {informe.get_estado_display()}")
print(f"\n👥 ASIGNACIONES:")
print(f"   Estudiante: {informe.usuario.nombre}")
print(f"   Escuela: {informe.escuela.nombre if informe.escuela else 'N/A'}")
print(f"   Secretaria: {informe.secretaria_asignada.nombre if informe.secretaria_asignada else 'N/A'}")
print(f"   Presidente: {informe.presidente_asignado.nombre if informe.presidente_asignado else 'N/A'}")
print(f"   Docente: {informe.docente_revisor.nombre if informe.docente_revisor else 'N/A'}")
print(f"\n📅 FECHAS:")
print(f"   Enviado: {informe.fecha_registro}")
print(f"   Secretaria: {informe.fecha_asignacion_secretaria or 'Pendiente'}")
print(f"   Presidente: {informe.fecha_asignacion_docente or 'Pendiente'}")
print(f"   Docente: {informe.fecha_revision_docente or 'Pendiente'}")
print(f"   Aprobación: {informe.fecha_aprobacion_presidente or 'Pendiente'}")
print(f"   Completado: {informe.fecha_completado or 'Pendiente'}")
EOF
```

---

## ⚠️ IMPORTANTE

### Sesiones Múltiples
- Cada pestaña mantiene su propia sesión
- Puedes tener los 4 roles logueados simultáneamente
- Navega entre pestañas sin perder sesión

### Si algo falla
1. Ver logs: `tail -f backend/server.log`
2. Verificar usuarios: Ver CREDENCIALES.md
3. Limpiar y empezar de nuevo:
```bash
cd backend
./venv/bin/python manage.py shell <<'EOF'
from apps.informes.models import Informe
Informe.objects.all().delete()
print("✅ Informes eliminados")
EOF
```

---

## ✅ CHECKLIST DE PRUEBA

- [ ] Paso 1: Estudiante envió informe
- [ ] Paso 2: Secretaria derivó a presidente
- [ ] Paso 3: Presidente asignó docente
- [ ] Paso 4: Docente creó banco
- [ ] Paso 5: Docente validó con IA
- [ ] Paso 6: Presidente aprobó dictamen
- [ ] Paso 7: Secretaria notificó
- [ ] Paso 8: Estudiante recibió resultado

---

**¡EL FLUJO COMPLETO ESTÁ FUNCIONANDO! Pruébalo ahora siguiendo los 8 pasos.**

Última actualización: 8 de Julio de 2026, 00:45 hrs
