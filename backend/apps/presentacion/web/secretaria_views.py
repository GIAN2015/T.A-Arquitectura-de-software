"""
Vistas para Secretaria Académica
Capa de Presentación - Clean Architecture
Versión 2.0
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.negocio.servicios.secretaria import SecretariaService
from apps.escuelas.services import EscuelaService
from apps.usuarios.models import Usuario
from apps.informes.models import Informe
from apps.notificaciones.services import NotificacionService
from apps.core.decorators import requiere_rol


@requiere_rol('secretaria')
def secretaria_dashboard(request):
    """
    Dashboard principal de secretaria
    Muestra informes pendientes, en proceso y estadísticas
    """
    secretaria = Usuario.objects.get(id=request.session['usuario_id'])
    
    # Obtener datos
    informes_pendientes = SecretariaService.obtener_informes_pendientes()[:10]
    informes_en_proceso = SecretariaService.obtener_informes_en_proceso(secretaria)[:10]
    informes_aprobados = SecretariaService.obtener_informes_aprobados_pendientes_notificar(secretaria)[:10]
    informes_rechazados = SecretariaService.obtener_informes_rechazados_pendientes_notificar(secretaria)[:10]
    informes_notificados = SecretariaService.obtener_informes_notificados(secretaria)[:10]
    
    # Estadísticas
    stats = SecretariaService.obtener_estadisticas(secretaria)
    
    # Notificaciones no leídas
    notificaciones_count = NotificacionService.contar_no_leidas(secretaria)
    notificaciones = NotificacionService.obtener_no_leidas(secretaria)[:5]
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'informes_pendientes': informes_pendientes,
        'informes_en_proceso': informes_en_proceso,
        'informes_aprobados': informes_aprobados,
        'informes_rechazados': informes_rechazados,
        'informes_notificados': informes_notificados,
        'stats': stats,
        'notificaciones_count': notificaciones_count,
        'notificaciones': notificaciones,
    }
    
    return render(request, 'secretaria/dashboard.html', context)


@requiere_rol('secretaria')
def secretaria_derivar(request, informe_id):
    """
    Vista para derivar informe a presidente de escuela
    GET: Muestra formulario con lista de escuelas
    POST: Deriva el informe
    """
    secretaria = Usuario.objects.get(id=request.session['usuario_id'])
    informe = get_object_or_404(Informe, id=informe_id)
    
    if request.method == 'POST':
        escuela_id = request.POST.get('escuela_id')
        comentario = request.POST.get('comentario', '')
        
        if not escuela_id:
            messages.error(request, 'Debe seleccionar una escuela.')
        else:
            success, informe_actualizado, error = SecretariaService.derivar_a_presidente(
                informe_id, escuela_id, secretaria, comentario
            )
            
            if success:
                messages.success(request, f'Informe derivado exitosamente a {informe_actualizado.escuela.nombre}')
                return redirect('secretaria_dashboard')
            else:
                messages.error(request, f'Error al derivar: {error}')
    
    # GET: Mostrar formulario
    escuelas = EscuelaService.obtener_todas_activas()
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'informe': informe,
        'escuelas': escuelas,
    }
    
    return render(request, 'secretaria/derivar.html', context)


@requiere_rol('secretaria')
def secretaria_notificar_estudiante(request, informe_id):
    """
    Notificar resultado final al estudiante
    Puede ser aprobado o rechazado por presidente
    """
    secretaria = Usuario.objects.get(id=request.session['usuario_id'])
    informe = get_object_or_404(Informe, id=informe_id)
    
    # Validar que está listo para notificar
    if informe.estado not in [Informe.ESTADO_APROBADO_PRESIDENTE, Informe.ESTADO_RECHAZADO_PRESIDENTE]:
        messages.error(request, 'Este informe aún no está listo para notificar al estudiante.')
        return redirect('secretaria_dashboard')
    
    if request.method == 'POST':
        # Determinar si es aprobado o rechazado
        if informe.estado == Informe.ESTADO_APROBADO_PRESIDENTE:
            success, informe_actualizado, error = SecretariaService.notificar_estudiante_aprobado(
                informe_id, secretaria
            )
            mensaje_exito = f'✅ Estudiante {informe.usuario.nombre} notificado - Informe APROBADO'
        else:  # RECHAZADO_PRESIDENTE
            success, informe_actualizado, error = SecretariaService.notificar_estudiante_rechazado(
                informe_id, secretaria
            )
            mensaje_exito = f'📧 Estudiante {informe.usuario.nombre} notificado - Debe corregir su informe'
        
        if success:
            messages.success(request, mensaje_exito)
            return redirect('secretaria_dashboard')
        else:
            messages.error(request, f'Error: {error}')
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'informe': informe,
    }
    
    return render(request, 'secretaria/notificar.html', context)


@requiere_rol('secretaria')
def secretaria_ver_informe(request, informe_id):
    """
    Ver detalle de un informe
    """
    informe = get_object_or_404(Informe, id=informe_id)
    observaciones = informe.observaciones.all().order_by('seccion')
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'informe': informe,
        'observaciones': observaciones,
        'total_observaciones': observaciones.count(),
    }
    
    return render(request, 'secretaria/ver.html', context)


@requiere_rol('secretaria')
def secretaria_notificaciones(request):
    """
    Ver todas las notificaciones
    """
    secretaria = Usuario.objects.get(id=request.session['usuario_id'])
    
    # Marcar una notificación como leída si se envía por POST
    if request.method == 'POST':
        notificacion_id = request.POST.get('notificacion_id')
        if notificacion_id:
            NotificacionService.marcar_como_leida(notificacion_id, secretaria)
            return redirect('secretaria_notificaciones')
    
    notificaciones = NotificacionService.obtener_todas(secretaria, limit=50)
    notificaciones_count = NotificacionService.contar_no_leidas(secretaria)
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'notificaciones': notificaciones,
        'notificaciones_count': notificaciones_count,
    }
    
    return render(request, 'secretaria/notificaciones.html', context)
