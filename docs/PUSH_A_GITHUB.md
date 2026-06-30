# Cómo Subir la Rama a GitHub

## Tu rama actual:
```
feature/sistema-completo-alumnos-docentes
```

## Commits que se subirán:
- ✅ Sistema completo con separación alumnos/docentes e IA mejorada
- ✅ Panel de administración personalizado
- ✅ Flujo completo de revisión docente
- ✅ Sistema de versionado de informes
- ✅ Estados y observaciones mejoradas

---

## OPCIÓN 1: Usar Token de GitHub (Recomendado)

### Paso 1: Crear Personal Access Token
1. Ve a: https://github.com/settings/tokens
2. Clic en "Generate new token (classic)"
3. Nombre: "laptop-untels"
4. Permisos: Marca `repo` (todos los sub-permisos)
5. Clic en "Generate token"
6. **COPIA EL TOKEN** (solo lo verás una vez)

### Paso 2: Subir con Token

```bash
cd /home/chapitec/Documents/chapitec/andre/T.A-Arquitectura-de-software/proyecto_untels

# Asegúrate de usar HTTPS
git remote set-url origin https://github.com/GIAN2015/T.A-Arquitectura-de-software.git

# Sube la rama
git push -u origin feature/sistema-completo-alumnos-docentes

# Cuando te pida credenciales:
Username: GIAN2015
Password: [pega tu token aquí, NO tu contraseña]
```

---

## OPCIÓN 2: Configurar SSH Key (Para Futuro)

Si quieres usar SSH en vez de HTTPS:

### Paso 1: Generar SSH Key
```bash
ssh-keygen -t ed25519 -C "tu-email@example.com"
# Presiona Enter 3 veces (sin passphrase)
```

### Paso 2: Copiar la clave pública
```bash
cat ~/.ssh/id_ed25519.pub
# Copia TODO el contenido
```

### Paso 3: Agregar a GitHub
1. Ve a: https://github.com/settings/keys
2. Clic en "New SSH key"
3. Título: "Laptop Ubuntu"
4. Pega la clave pública
5. Clic en "Add SSH key"

### Paso 4: Cambiar remote a SSH
```bash
git remote set-url origin git@github.com:GIAN2015/T.A-Arquitectura-de-software.git
git push -u origin feature/sistema-completo-alumnos-docentes
```

---

## OPCIÓN 3: Usar GitHub CLI (gh)

Si tienes instalado GitHub CLI:

```bash
gh auth login
# Selecciona:
# - GitHub.com
# - HTTPS
# - Login with a web browser

# Luego:
git push -u origin feature/sistema-completo-alumnos-docentes
```

---

## Verificar que se subió correctamente

Después de hacer push, verifica en:
```
https://github.com/GIAN2015/T.A-Arquitectura-de-software/branches
```

Deberías ver tu rama: `feature/sistema-completo-alumnos-docentes`

---

## Crear Pull Request (Opcional)

Si quieres mergear a main:

1. Ve a: https://github.com/GIAN2015/T.A-Arquitectura-de-software
2. Verás un banner amarillo: "Compare & pull request"
3. Clic ahí
4. Título: "Sistema completo de revisión docente-alumno con IA"
5. Descripción:
   ```
   ## Cambios Principales
   - ✅ Flujo completo docente → alumno
   - ✅ Panel de administración personalizado
   - ✅ Sistema de versionado
   - ✅ 7 estados de informe
   - ✅ 4 severidades de observación
   - ✅ Comentarios bidireccionales
   
   ## Archivos Creados
   - Panel admin (7 vistas + 7 templates)
   - Flujo de revisión docente
   - Sistema de versionado
   
   ## Migraciones
   - 2 migraciones aplicadas correctamente
   
   ## Documentación
   - FLUJO_COMPLETO_DOCENTE_ALUMNO.md
   - PANEL_ADMINISTRACION.md
   - ACCESO_PANEL_ADMIN.md
   ```
6. Clic en "Create pull request"

---

## Resumen de Archivos que se Subirán

### Modelos:
- `apps/informes/models.py` (7 estados + versionado)
- `apps/observaciones/models.py` (4 estados + severidad)

### Vistas:
- `apps/core/admin_views.py` (7 funciones nuevas)
- `apps/core/views.py` (actualizadas)

### Templates:
- `templates/admin/` (7 archivos)
- `templates/validation_result.html` (reescrito)
- `templates/panel_docente.html` (actualizado)

### Documentación:
- `FLUJO_COMPLETO_DOCENTE_ALUMNO.md`
- `PANEL_ADMINISTRACION.md`
- `ACCESO_PANEL_ADMIN.md`
- `PUSH_A_GITHUB.md` (este archivo)

### Migraciones:
- `apps/informes/migrations/0002_...`
- `apps/observaciones/migrations/0002_...`

---

## Comandos Útiles

Ver diferencias con main:
```bash
git diff origin/main..HEAD --stat
```

Ver commits que se subirán:
```bash
git log origin/main..HEAD --oneline
```

Ver estado actual:
```bash
git status
git branch -a
git remote -v
```

---

## Problemas Comunes

### "Permission denied"
→ Usa HTTPS con token en vez de SSH

### "Authentication failed"
→ Usa Personal Access Token, NO tu contraseña

### "fatal: refusing to merge unrelated histories"
→ Haz pull primero:
```bash
git pull origin main --allow-unrelated-histories
git push -u origin feature/sistema-completo-alumnos-docentes
```

---

## Contacto

Si tienes problemas, revisa:
- Estado del repo: `git status`
- Remotes: `git remote -v`
- Branches: `git branch -a`
