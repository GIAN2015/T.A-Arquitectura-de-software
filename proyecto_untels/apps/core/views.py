"""
Vistas principales del sistema
Separación clara entre flujos de Estudiantes y Docentes
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from apps.usuarios.services import autenticar_usuario, registrar_usuario
from apps.usuarios.models import Usuario
from apps.informes.models import Informe
from apps.informes.services import leer_archivo
from apps.reglamento.services import obtener_reglamento
from apps.observaciones.services import obtener_observaciones, validar_informe
from apps.observaciones.models import ObservacionGenerada


# ============================================
# AUTENTICACIÓN
# ============================================

def login_view(request):
    """Login para estudiantes y egresados"""
    # Si ya está logueado, redirigir
    if 'usuario_id' in request.session:
        if request.session.get('usuario_tipo') == 'docente':
            return redirect('panel_docente')
        return redirect('upload')
    
    if request.method == 'POST':
        codigo = request.POST.get('codigo', '').strip()
        password = request.POST.get('password', '').strip()
        
        if not codigo or not password:
            messages.error(request, 'Por favor ingresa tu código y contraseña.')
            return render(request, 'login.html')
        
        usuario = autenticar_usuario(codigo, password)
        if usuario:
            if usuario.tipo_usuario == 'docente':
                messages.error(request, 'Los docentes deben usar el portal de docentes.')
                return render(request, 'login.html')
            
            request.session['usuario_id'] = usuario.id
            request.session['usuario_codigo'] = usuario.codigo
            request.session['usuario_nombre'] = usuario.nombre
            request.session['usuario_tipo'] = usuario.tipo_usuario
            messages.success(request, f'Bienvenido, {usuario.nombre}')
            return redirect('upload')
        else:
            messages.error(request, 'Código o contraseña incorrectos.')
            return render(request, 'login.html')
    
    return render(request, 'login.html')


def login_docente_view(request):
    """Login exclusivo para docentes"""
    # Si ya está logueado como docente, redirigir
    if 'usuario_id' in request.session and request.session.get('usuario_tipo') == 'docente':
        return redirect('panel_docente')
    
    if request.method == 'POST':
        codigo = request.POST.get('codigo', '').strip()
        password = request.POST.get('password', '').strip()
        
        if not codigo or not password:
            messages.error(request, 'Por favor ingresa tu código y contraseña.')
            return render(request, 'login_docente.html')
        
        usuario = autenticar_usuario(codigo, password)
        if usuario:
            if usuario.tipo_usuario != 'docente':
                messages.error(request, 'Esta área es solo para docentes. Usa el login de estudiantes.')
                return render(request, 'login_docente.html')
            
            request.session['usuario_id'] = usuario.id
            request.session['usuario_codigo'] = usuario.codigo
            request.session['usuario_nombre'] = usuario.nombre
            request.session['usuario_tipo'] = usuario.tipo_usuario
            messages.success(request, f'Bienvenido, {usuario.nombre}')
            return redirect('panel_docente')
        else:
            messages.error(request, 'Código o contraseña incorrectos.')
            return render(request, 'login_docente.html')
    
    return render(request, 'login_docente.html')


def registro_view(request):
    """Registro de nuevos estudiantes/egresados (no docentes)"""
    if request.method == 'POST':
        codigo = request.POST.get('codigo', '').strip()
        nombre = request.POST.get('nombre', '').strip()
        password = request.POST.get('password', '').strip()
        password_confirm = request.POST.get('password_confirm', '').strip()
        tipo_usuario = request.POST.get('tipo_usuario', 'estudiante')
        
        # Bloquear registro de docentes (solo se crean desde admin)
        if tipo_usuario == 'docente':
            messages.error(request, 'Los docentes son registrados por la administración.')
            return render(request, 'registro.html')
        
        if not all([codigo, nombre, password, password_confirm]):
            messages.error(request, 'Todos los campos son obligatorios.')
            return render(request, 'registro.html')
        
        if password != password_confirm:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'registro.html')
        
        if len(password) < 6:
            messages.error(request, 'La contraseña debe tener al menos 6 caracteres.')
            return render(request, 'registro.html')
        
        usuario = registrar_usuario(codigo, nombre, password, tipo_usuario)
        if usuario:
            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect('login')
        else:
            messages.error(request, 'El código ya está registrado.')
            return render(request, 'registro.html')
    
    return render(request, 'registro.html')


def logout_view(request):
    """Cierre de sesión"""
    tipo = request.session.get('usuario_tipo')
    request.session.flush()
    messages.success(request, 'Has cerrado sesión correctamente.')
    
    # Redirigir al login correspondiente
    if tipo == 'docente':
        return redirect('login_docente')
    return redirect('login')


# ============================================
# VISTAS DE ESTUDIANTES
# ============================================

def _verificar_estudiante(request):
    """Helper: verifica que el usuario sea estudiante/egresado"""
    if 'usuario_id' not in request.session:
        return False
    if request.session.get('usuario_tipo') == 'docente':
        return False
    return True


def upload_view(request):
    """Vista para que estudiantes suban informes"""
    if not _verificar_estudiante(request):
        messages.error(request, 'Debes iniciar sesión como estudiante.')
        return redirect('login')

    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
    }

    if request.method == 'POST':
        archivo = request.FILES.get('informe')
        
        # Validaciones
        if not archivo:
            messages.error(request, 'Por favor selecciona un archivo .docx')
            return render(request, 'upload_report.html', context)
        if not archivo.name.endswith('.docx'):
            messages.error(request, 'Solo se permiten archivos .docx')
            return render(request, 'upload_report.html', context)
        if archivo.size > 10 * 1024 * 1024:  # 10MB
            messages.error(request, 'El archivo es demasiado grande. Máximo 10MB.')
            return render(request, 'upload_report.html', context)

        informe = None
        try:
            usuario = Usuario.objects.get(id=request.session['usuario_id'])
            
            # Leer contenido del archivo
            try:
                contenido = leer_archivo(archivo)
            except Exception as e:
                messages.error(request, f'Error al leer el archivo: archivo dañado o formato incorrecto.')
                return render(request, 'upload_report.html', context)
            
            if not contenido or len(contenido.strip()) < 50:
                messages.error(request, 'El archivo está vacío o tiene muy poco contenido.')
                return render(request, 'upload_report.html', context)

            # Detectar si es reenvío (versionado mejorado)
            informe_previo = Informe.objects.filter(
                usuario=usuario,
                estado=Informe.ESTADO_RECHAZADO
            ).order_by('-fecha_registro').first()
            
            version = 1
            if informe_previo:
                version = informe_previo.version + 1
                messages.info(request, f'Detectado reenvío - Versión {version} del informe.')

            # Crear informe en estado ENVIADO
            informe = Informe.objects.create(
                usuario=usuario,
                nombre_archivo=archivo.name,
                contenido=contenido,
                estado=Informe.ESTADO_ENVIADO,
                version=version,
                informe_anterior=informe_previo
            )

            # Cambiar a VALIDANDO
            informe.estado = Informe.ESTADO_VALIDANDO
            informe.save()

            # Llamar a la IA
            try:
                reglamento = obtener_reglamento()
                observaciones_banco = obtener_observaciones()
                resultado = validar_informe(contenido, reglamento, observaciones_banco)
            except Exception as e:
                # Si la IA falla completamente, marcar como observado pero sin observaciones
                print(f"⚠️ Error en validación IA: {e}")
                resultado = []
                messages.warning(request, 'La IA no pudo procesar el informe. Será revisado manualmente por el docente.')

            # Guardar observaciones generadas por IA
            for obs in resultado:
                severidad = obs.get('severidad', 'importante')
                if severidad not in ['critica', 'importante', 'menor', 'sugerencia']:
                    severidad = 'importante'
                
                ObservacionGenerada.objects.create(
                    informe=informe,
                    seccion=obs.get('seccion', 'General'),
                    observacion=obs.get('observacion', ''),
                    ubicacion_error=obs.get('ubicacion', 'No especificada'),
                    estado=ObservacionGenerada.ESTADO_PENDIENTE,
                    severidad=severidad
                )

            # Actualizar estado final del informe
            if resultado:
                informe.estado = Informe.ESTADO_OBSERVADO
                messages.success(request, f'Informe procesado. La IA detectó {len(resultado)} observación(es). Esperando revisión del docente.')
            else:
                informe.estado = Informe.ESTADO_OBSERVADO  # Aún debe revisar el docente
                messages.success(request, 'Informe procesado. No se detectaron observaciones por la IA. Esperando revisión del docente.')
            
            informe.save()
            return redirect('resultado', informe_id=informe.id)
            
        except Exception as e:
            # Si algo falla, marcar el informe como observado para que el docente lo revise
            if informe:
                informe.estado = Informe.ESTADO_OBSERVADO
                informe.save()
            messages.error(request, f'Error al procesar el informe: {str(e)}. El informe fue guardado para revisión manual.')
            return render(request, 'upload_report.html', context)

    return render(request, 'upload_report.html', context)


def resultado_view(request, informe_id):
    """Vista para ver el resultado de un informe específico"""
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    informe = get_object_or_404(Informe, id=informe_id)
    
    # Control de acceso: solo el dueño del informe o docentes pueden verlo
    usuario_id = request.session.get('usuario_id')
    tipo = request.session.get('usuario_tipo')
    
    if tipo != 'docente' and informe.usuario_id != usuario_id:
        messages.error(request, 'No tienes permiso para ver este informe.')
        return redirect('historial')
    
    observaciones = ObservacionGenerada.objects.filter(informe=informe).order_by('severidad', 'id')
    
    context = {
        'informe': informe,
        'observaciones': observaciones,
        'usuario': informe.usuario,
        'es_docente': tipo == 'docente',
    }
    return render(request, 'validation_result.html', context)


def historial_view(request):
    """Historial de informes del estudiante"""
    if not _verificar_estudiante(request):
        messages.error(request, 'Debes iniciar sesión como estudiante.')
        return redirect('login')
    
    usuario = Usuario.objects.get(id=request.session['usuario_id'])
    informes = Informe.objects.filter(usuario=usuario).order_by('-fecha_registro')
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'informes': informes,
    }
    return render(request, 'historial.html', context)


# ============================================
# VISTAS DE DOCENTES
# ============================================

def _verificar_docente(request):
    """Helper: verifica que el usuario sea docente"""
    if 'usuario_id' not in request.session:
        return False
    if request.session.get('usuario_tipo') != 'docente':
        return False
    return True


def panel_docente_view(request):
    """Panel principal del docente - muestra informes que requieren revisión"""
    if not _verificar_docente(request):
        messages.error(request, 'Acceso denegado. Solo docentes.')
        return redirect('login_docente')
    
    # Filtros opcionales
    filtro_estado = request.GET.get('estado', 'pendientes')
    
    # Por defecto, mostrar pendientes de revisión
    if filtro_estado == 'pendientes':
        informes = Informe.objects.filter(
            estado__in=[Informe.ESTADO_OBSERVADO, Informe.ESTADO_EN_REVISION_DOCENTE]
        ).select_related('usuario').order_by('-fecha_registro')
    elif filtro_estado == 'aprobados':
        informes = Informe.objects.filter(
            estado=Informe.ESTADO_APROBADO
        ).select_related('usuario').order_by('-fecha_revision_docente')
    elif filtro_estado == 'rechazados':
        informes = Informe.objects.filter(
            estado=Informe.ESTADO_RECHAZADO
        ).select_related('usuario').order_by('-fecha_revision_docente')
    else:  # todos
        informes = Informe.objects.all().select_related('usuario').order_by('-fecha_registro')
    
    # Estadísticas
    total_pendientes = Informe.objects.filter(
        estado__in=[Informe.ESTADO_OBSERVADO, Informe.ESTADO_EN_REVISION_DOCENTE]
    ).count()
    total_aprobados = Informe.objects.filter(estado=Informe.ESTADO_APROBADO).count()
    total_rechazados = Informe.objects.filter(estado=Informe.ESTADO_RECHAZADO).count()
    total_informes = Informe.objects.count()
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'informes': informes,
        'filtro_estado': filtro_estado,
        'total_pendientes': total_pendientes,
        'total_aprobados': total_aprobados,
        'total_rechazados': total_rechazados,
        'total_informes': total_informes,
    }
    return render(request, 'panel_docente.html', context)
