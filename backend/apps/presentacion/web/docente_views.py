"""
Vistas para Docente
Capa de Presentación - Clean Architecture
Versión 2.0 - Ampliado con banco de observaciones personalizado
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.negocio.servicios.docente import DocenteService
from apps.usuarios.models import Usuario
from apps.informes.models import Informe
from apps.observaciones.models import ObservacionGenerada
from apps.notificaciones.services import NotificacionService


def _verificar_docente(request):
    """Verificar que el usuario sea docente"""
    if 'usuario_id' not in request.session:
        return False
    return request.session.get('usuario_tipo') == 'docente'


def panel_docente_view(request):
    """
    Dashboard principal de docente
    ACTUALIZADO v2.0: Usa DocenteService
    """
    if not _verificar_docente(request):
        messages.error(request, 'Acceso denegado. Solo docentes.')
        return redirect('login_docente')
    
    docente = Usuario.objects.get(id=request.session['usuario_id'])
    
    # Obtener datos usando servicios
    informes_asignados = DocenteService.obtener_informes_asignados(docente)[:10]
    informes_revisados = DocenteService.obtener_informes_revisados(docente)[:10]
    banco_activo = DocenteService.obtener_banco_activo(docente)
    
    # Estadísticas
    stats = DocenteService.obtener_estadisticas(docente)
    
    # Notificaciones
    notificaciones_count = NotificacionService.contar_no_leidas(docente)
    notificaciones = NotificacionService.obtener_no_leidas(docente)[:5]
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'informes_asignados': informes_asignados,
        'informes_revisados': informes_revisados,
        'banco_activo': banco_activo,
        'stats': stats,
        'notificaciones_count': notificaciones_count,
        'notificaciones': notificaciones,
    }
    
    return render(request, 'docente/dashboard.html', context)


def docente_banco_observaciones(request):
    """
    Gestionar bancos de observaciones del docente
    NUEVO v2.0
    """
    if not _verificar_docente(request):
        messages.error(request, 'Acceso denegado.')
        return redirect('login_docente')
    
    docente = Usuario.objects.get(id=request.session['usuario_id'])
    
    # Procesar formulario
    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        if accion == 'crear':
            nombre = request.POST.get('nombre')
            archivo = request.FILES.get('archivo')
            
            if not nombre or not archivo:
                messages.error(request, 'Debe proporcionar nombre y archivo.')
            else:
                success, banco, error = DocenteService.crear_banco_observaciones(
                    docente, nombre, archivo
                )
                if success:
                    messages.success(request, f'Banco "{nombre}" creado y activado exitosamente.')
                    return redirect('docente_banco_observaciones')
                else:
                    messages.error(request, f'Error: {error}')
        
        elif accion == 'activar':
            banco_id = request.POST.get('banco_id')
            success, banco, error = DocenteService.activar_banco(banco_id, docente)
            if success:
                messages.success(request, f'Banco "{banco.nombre}" activado.')
                return redirect('docente_banco_observaciones')
            else:
                messages.error(request, f'Error: {error}')
        
        elif accion == 'eliminar':
            banco_id = request.POST.get('banco_id')
            success, error = DocenteService.eliminar_banco(banco_id, docente)
            if success:
                messages.success(request, 'Banco eliminado exitosamente.')
                return redirect('docente_banco_observaciones')
            else:
                messages.error(request, f'Error: {error}')
    
    # GET: Mostrar lista de bancos
    bancos = DocenteService.obtener_todos_bancos(docente)
    banco_activo = DocenteService.obtener_banco_activo(docente)
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'bancos': bancos,
        'banco_activo': banco_activo,
        'total_bancos': bancos.count(),
    }
    
    return render(request, 'docente/banco_observaciones.html', context)


def docente_revisar_informe(request, informe_id):
    """
    Revisar informe con IA y tabla editable de observaciones
    ACTUALIZADO v2.0: Usa banco personalizado del docente
    """
    if not _verificar_docente(request):
        messages.error(request, 'Acceso denegado.')
        return redirect('login_docente')
    
    docente = Usuario.objects.get(id=request.session['usuario_id'])
    informe = get_object_or_404(Informe, id=informe_id, docente_revisor=docente)
    
    # Si está en estado PENDIENTE_DOCENTE o RECHAZADO_PRESIDENTE, validar con IA
    if informe.estado in [Informe.ESTADO_PENDIENTE_DOCENTE, Informe.ESTADO_RECHAZADO_PRESIDENTE]:
        # Verificar que tenga banco activo
        banco_activo = DocenteService.obtener_banco_activo(docente)
        if not banco_activo:
            messages.warning(request, 'Debe crear un banco de observaciones antes de revisar informes.')
            return redirect('docente_banco_observaciones')
        
        # Si no se ha validado con IA, hacerlo
        if not informe.observaciones.exists():
            success, observaciones, error = DocenteService.validar_informe_con_ia(
                informe_id, docente
            )
            if not success:
                messages.error(request, f'Error al validar con IA: {error}')
                return redirect('panel_docente')
            
            messages.info(request, f'Validación con IA completada. {len(observaciones)} observaciones generadas.')
    
    # Procesar formulario de edición de observaciones
    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        if accion == 'actualizar_observaciones':
            # Actualizar cada observación
            observaciones = informe.observaciones.all()
            for obs in observaciones:
                obs_accion = request.POST.get(f'obs_accion_{obs.id}')
                obs_comentario = request.POST.get(f'obs_comentario_{obs.id}', '')
                obs_severidad = request.POST.get(f'obs_severidad_{obs.id}')
                
                if obs_accion == 'confirmar':
                    obs.estado = ObservacionGenerada.ESTADO_CONFIRMADA
                elif obs_accion == 'descartar':
                    obs.estado = ObservacionGenerada.ESTADO_DESCARTADA
                
                obs.comentario_docente = obs_comentario
                if obs_severidad:
                    obs.severidad = obs_severidad
                obs.save()
            
            messages.success(request, 'Observaciones actualizadas exitosamente.')
        
        elif accion == 'enviar_dictamen':
            comentario_general = request.POST.get('comentario_general')
            recomendar = request.POST.get('recomendar') == 'aprobar'
            
            if not comentario_general or len(comentario_general.strip()) < 20:
                messages.error(request, 'Debe proporcionar un dictamen detallado (mínimo 20 caracteres).')
            else:
                success, informe_actualizado, error = DocenteService.enviar_dictamen_a_presidente(
                    informe_id, docente, comentario_general, recomendar
                )
                
                if success:
                    messages.success(request, 'Dictamen enviado al presidente exitosamente.')
                    return redirect('panel_docente')
                else:
                    messages.error(request, f'Error: {error}')
    
    # Obtener observaciones agrupadas
    observaciones = informe.observaciones.all().order_by('seccion')
    obs_confirmadas = observaciones.filter(estado=ObservacionGenerada.ESTADO_CONFIRMADA)
    obs_pendientes = observaciones.filter(estado=ObservacionGenerada.ESTADO_PENDIENTE)
    obs_descartadas = observaciones.filter(estado=ObservacionGenerada.ESTADO_DESCARTADA)
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'informe': informe,
        'observaciones': observaciones,
        'obs_confirmadas': obs_confirmadas,
        'obs_pendientes': obs_pendientes,
        'obs_descartadas': obs_descartadas,
        'total_observaciones': observaciones.count(),
        'banco_usado': informe.banco_observaciones_usado,
    }
    
    return render(request, 'docente/revisar_informe.html', context)


def docente_ver_informe(request, informe_id):
    """
    Ver detalle de un informe (solo lectura)
    """
    if not _verificar_docente(request):
        messages.error(request, 'Acceso denegado.')
        return redirect('login_docente')
    
    docente = Usuario.objects.get(id=request.session['usuario_id'])
    informe = get_object_or_404(Informe, id=informe_id, docente_revisor=docente)
    
    observaciones = informe.observaciones.all().order_by('seccion')
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'informe': informe,
        'observaciones': observaciones,
        'total_observaciones': observaciones.count(),
    }
    
    return render(request, 'docente/ver_informe.html', context)


def docente_historial(request):
    """
    Ver historial de informes revisados
    """
    if not _verificar_docente(request):
        messages.error(request, 'Acceso denegado.')
        return redirect('login_docente')
    
    docente = Usuario.objects.get(id=request.session['usuario_id'])
    
    # Todos los informes asignados (actuales e históricos)
    informes = Informe.objects.filter(
        docente_revisor=docente
    ).select_related('usuario', 'presidente_asignado').order_by('-fecha_asignacion_docente')[:50]
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'informes': informes,
    }
    
    return render(request, 'docente/historial.html', context)


def docente_notificaciones(request):
    """
    Ver todas las notificaciones
    """
    if not _verificar_docente(request):
        messages.error(request, 'Acceso denegado.')
        return redirect('login_docente')
    
    docente = Usuario.objects.get(id=request.session['usuario_id'])
    
    # Marcar notificación como leída
    if request.method == 'POST':
        notificacion_id = request.POST.get('notificacion_id')
        if notificacion_id:
            NotificacionService.marcar_como_leida(notificacion_id, docente)
            return redirect('docente_notificaciones')
    
    notificaciones = NotificacionService.obtener_todas(docente, limit=50)
    notificaciones_count = NotificacionService.contar_no_leidas(docente)
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'notificaciones': notificaciones,
        'notificaciones_count': notificaciones_count,
    }
    
    return render(request, 'docente/notificaciones.html', context)
