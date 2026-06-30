"""
Vistas para Presidente de Escuela
Capa de Presentación - Clean Architecture
Versión 2.0
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.negocio.servicios.presidente import PresidenteService
from apps.usuarios.models import Usuario
from apps.informes.models import Informe
from apps.notificaciones.services import NotificacionService


def presidente_dashboard(request):
    """
    Dashboard principal de presidente de escuela
    Muestra informes de su escuela en diferentes estados
    """
    if 'usuario_id' not in request.session:
        return redirect('login_presidente')
    
    if request.session.get('usuario_tipo') != 'presidente':
        messages.error(request, 'Acceso denegado. Solo presidentes pueden acceder.')
        return redirect('login')
    
    presidente = Usuario.objects.get(id=request.session['usuario_id'])
    
    # Validar que tenga escuela asignada
    if not presidente.escuela:
        messages.error(request, 'No tiene una escuela asignada. Contacte al administrador.')
        return redirect('logout')
    
    # Obtener datos
    pendientes_asignar = PresidenteService.obtener_informes_pendientes_asignar(presidente)[:10]
    en_revision = PresidenteService.obtener_informes_en_revision(presidente)[:10]
    pendientes_aprobar = PresidenteService.obtener_informes_pendientes_aprobar(presidente)
    
    # Estadísticas
    stats = PresidenteService.obtener_estadisticas(presidente)
    
    # Notificaciones
    notificaciones_count = NotificacionService.contar_no_leidas(presidente)
    notificaciones = NotificacionService.obtener_no_leidas(presidente)[:5]
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'escuela': presidente.escuela.nombre,
        'pendientes_asignar': pendientes_asignar,
        'en_revision': en_revision,
        'pendientes_aprobar': pendientes_aprobar,
        'stats': stats,
        'notificaciones_count': notificaciones_count,
        'notificaciones': notificaciones,
    }
    
    return render(request, 'presidente/dashboard.html', context)


def presidente_designar_docente(request, informe_id):
    """
    Vista para designar docente revisor a un informe
    GET: Muestra formulario con lista de docentes de la escuela
    POST: Asigna el docente
    """
    if 'usuario_id' not in request.session:
        return redirect('login_presidente')
    
    if request.session.get('usuario_tipo') != 'presidente':
        messages.error(request, 'Acceso denegado.')
        return redirect('login')
    
    presidente = Usuario.objects.get(id=request.session['usuario_id'])
    informe = get_object_or_404(
        Informe, 
        id=informe_id, 
        presidente_asignado=presidente,
        estado=Informe.ESTADO_PENDIENTE_PRESIDENTE
    )
    
    if request.method == 'POST':
        docente_id = request.POST.get('docente_id')
        
        if not docente_id:
            messages.error(request, 'Debe seleccionar un docente.')
        else:
            success, informe_actualizado, error = PresidenteService.designar_docente(
                informe_id, docente_id, presidente
            )
            
            if success:
                messages.success(request, f'Docente {informe_actualizado.docente_revisor.nombre} asignado exitosamente.')
                return redirect('presidente_dashboard')
            else:
                messages.error(request, f'Error: {error}')
    
    # GET: Mostrar formulario
    docentes = PresidenteService.obtener_docentes_disponibles(presidente)
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'escuela': presidente.escuela.nombre,
        'informe': informe,
        'docentes': docentes,
    }
    
    return render(request, 'presidente/designar_docente.html', context)


def presidente_revisar_dictamen(request, informe_id):
    """
    Revisar dictamen del docente y aprobar/rechazar
    Muestra el informe, observaciones y dictamen del docente
    """
    if 'usuario_id' not in request.session:
        return redirect('login_presidente')
    
    if request.session.get('usuario_tipo') != 'presidente':
        messages.error(request, 'Acceso denegado.')
        return redirect('login')
    
    presidente = Usuario.objects.get(id=request.session['usuario_id'])
    informe = get_object_or_404(
        Informe, 
        id=informe_id, 
        presidente_asignado=presidente,
        estado=Informe.ESTADO_PENDIENTE_APROBACION_PRESIDENTE
    )
    
    # Procesar formulario
    if request.method == 'POST':
        accion = request.POST.get('accion')  # 'aprobar' o 'rechazar'
        comentario = request.POST.get('comentario', '')
        
        if accion == 'aprobar':
            success, informe_actualizado, error = PresidenteService.aprobar_dictamen_docente(
                informe_id, presidente, comentario
            )
            if success:
                messages.success(request, 'Dictamen aprobado. Secretaría ha sido notificada.')
                return redirect('presidente_dashboard')
            else:
                messages.error(request, f'Error: {error}')
        
        elif accion == 'rechazar':
            if not comentario or len(comentario.strip()) < 10:
                messages.error(request, 'Debe proporcionar un motivo detallado para rechazar (mínimo 10 caracteres).')
            else:
                success, informe_actualizado, error = PresidenteService.rechazar_dictamen_docente(
                    informe_id, presidente, comentario
                )
                if success:
                    messages.warning(request, 'Dictamen rechazado. El docente ha sido notificado.')
                    return redirect('presidente_dashboard')
                else:
                    messages.error(request, f'Error: {error}')
    
    # Obtener observaciones
    observaciones = informe.observaciones.all().order_by('seccion')
    obs_confirmadas = observaciones.filter(estado='confirmada')
    obs_descartadas = observaciones.filter(estado='descartada')
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'escuela': presidente.escuela.nombre,
        'informe': informe,
        'observaciones': observaciones,
        'obs_confirmadas': obs_confirmadas,
        'obs_descartadas': obs_descartadas,
        'total_observaciones': observaciones.count(),
        'total_confirmadas': obs_confirmadas.count(),
    }
    
    return render(request, 'presidente/revisar_dictamen.html', context)


def presidente_ver_informe(request, informe_id):
    """
    Ver detalle completo de un informe de la escuela
    """
    if 'usuario_id' not in request.session:
        return redirect('login_presidente')
    
    if request.session.get('usuario_tipo') != 'presidente':
        messages.error(request, 'Acceso denegado.')
        return redirect('login')
    
    presidente = Usuario.objects.get(id=request.session['usuario_id'])
    informe = get_object_or_404(Informe, id=informe_id, presidente_asignado=presidente)
    
    observaciones = informe.observaciones.all().order_by('seccion')
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'escuela': presidente.escuela.nombre,
        'informe': informe,
        'observaciones': observaciones,
        'total_observaciones': observaciones.count(),
    }
    
    return render(request, 'presidente/ver_informe.html', context)


def presidente_historial(request):
    """
    Ver historial completo de informes de la escuela
    """
    if 'usuario_id' not in request.session:
        return redirect('login_presidente')
    
    if request.session.get('usuario_tipo') != 'presidente':
        messages.error(request, 'Acceso denegado.')
        return redirect('login')
    
    presidente = Usuario.objects.get(id=request.session['usuario_id'])
    
    # Todos los informes de la escuela
    informes = Informe.objects.filter(
        presidente_asignado=presidente
    ).select_related('usuario', 'docente_revisor').order_by('-fecha_registro')[:50]
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'escuela': presidente.escuela.nombre,
        'informes': informes,
    }
    
    return render(request, 'presidente/historial.html', context)


def presidente_notificaciones(request):
    """
    Ver todas las notificaciones
    """
    if 'usuario_id' not in request.session:
        return redirect('login_presidente')
    
    if request.session.get('usuario_tipo') != 'presidente':
        messages.error(request, 'Acceso denegado.')
        return redirect('login')
    
    presidente = Usuario.objects.get(id=request.session['usuario_id'])
    
    # Marcar notificación como leída
    if request.method == 'POST':
        notificacion_id = request.POST.get('notificacion_id')
        if notificacion_id:
            NotificacionService.marcar_como_leida(notificacion_id, presidente)
            return redirect('presidente_notificaciones')
    
    notificaciones = NotificacionService.obtener_todas(presidente, limit=50)
    notificaciones_count = NotificacionService.contar_no_leidas(presidente)
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'escuela': presidente.escuela.nombre,
        'notificaciones': notificaciones,
        'notificaciones_count': notificaciones_count,
    }
    
    return render(request, 'presidente/notificaciones.html', context)
