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
from apps.core.decorators import requiere_rol


@requiere_rol('docente')
def panel_docente_view(request):
    """
    Dashboard principal de docente
    ACTUALIZADO v2.0: Usa DocenteService
    """
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


@requiere_rol('docente')
def docente_banco_observaciones(request):
    """
    Gestionar bancos de observaciones del docente
    NUEVO v2.0
    """
    
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
                    return redirect('docente_banco')
                else:
                    messages.error(request, f'Error: {error}')
        
        elif accion == 'activar':
            banco_id = request.POST.get('banco_id')
            success, banco, error = DocenteService.activar_banco(banco_id, docente)
            if success:
                messages.success(request, f'✅ Banco "{banco.nombre}" activado.')
                return redirect('docente_banco')
            else:
                messages.error(request, f'Error: {error}')
        
        elif accion == 'desactivar':
            banco_id = request.POST.get('banco_id')
            success, banco, error = DocenteService.desactivar_banco(banco_id, docente)
            if success:
                messages.info(request, f'Banco "{banco.nombre}" desactivado.')
                return redirect('docente_banco')
            else:
                messages.error(request, f'Error: {error}')
        
        elif accion == 'eliminar':
            banco_id = request.POST.get('banco_id')
            success, error = DocenteService.eliminar_banco(banco_id, docente)
            if success:
                messages.success(request, 'Banco eliminado exitosamente.')
                return redirect('docente_banco')
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
    
    return render(request, 'docente/banco.html', context)


@requiere_rol('docente')
def docente_revisar_informe(request, informe_id):
    """
    Revisar informe con IA y tabla editable de observaciones
    ACTUALIZADO v2.0: Usa banco personalizado del docente
    FLUJO:
    1. Mostrar info del informe + botón "Iniciar Validación con IA"
    2. Al hacer POST con accion='validar_ia' → Procesar con IA
    3. Mostrar observaciones generadas para editar
    4. Enviar dictamen final
    """
    
    docente = Usuario.objects.get(id=request.session['usuario_id'])
    informe = get_object_or_404(Informe, id=informe_id, docente_revisor=docente)
    
    # Obtener todos los bancos activos del docente (v2.1: múltiples permitidos)
    bancos_disponibles = DocenteService.obtener_todos_bancos(docente).filter(activo=True)
    if not bancos_disponibles.exists():
        messages.warning(request, 'Debe crear y activar un banco de observaciones antes de revisar informes.')
        return redirect('docente_banco')
    
    # Procesar formulario
    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        # ACCIÓN 1: VALIDAR CON IA (v2.1 - Con selección de banco)
        if accion == 'validar_ia':
            banco_id = request.POST.get('banco_id')
            
            if not banco_id:
                messages.error(request, 'Debe seleccionar un banco de observaciones.')
                return redirect('docente_revisar_informe', informe_id=informe_id)
            
            # Verificar que el banco pertenece al docente
            try:
                from apps.observaciones.models import BancoObservacionesDocente
                banco = BancoObservacionesDocente.objects.get(id=banco_id, docente=docente, activo=True)
            except BancoObservacionesDocente.DoesNotExist:
                messages.error(request, 'Banco de observaciones no válido.')
                return redirect('docente_revisar_informe', informe_id=informe_id)
            
            # Verificar que no tenga observaciones ya generadas
            if informe.observaciones.exists():
                messages.warning(request, 'Este informe ya fue validado con IA.')
            else:
                # Validar con el banco seleccionado
                success, observaciones_generadas, error = DocenteService.validar_informe_con_ia(
                    informe_id, docente, banco_especifico=banco
                )
                
                # Solo mostrar resultado final
                if success:
                    messages.success(request, f'✅ Validación completada con banco "{banco.nombre}". Se generaron {len(observaciones_generadas)} observaciones.')
                    messages.info(request, 'Revisa las observaciones y edítalas si es necesario antes de enviar el dictamen.')
                else:
                    messages.error(request, f'❌ Error al validar: {error}')
                
                # Recargar la página para mostrar observaciones
                return redirect('docente_revisar_informe', informe_id=informe_id)
        
        # ACCIÓN NUEVA: RE-VALIDAR (v2.1 - Con selección de banco)
        elif accion == 'revalidar':
            banco_id = request.POST.get('banco_id')
            
            if not banco_id:
                messages.error(request, 'Debe seleccionar un banco de observaciones.')
                return redirect('docente_revisar_informe', informe_id=informe_id)
            
            # Verificar que el banco pertenece al docente
            try:
                from apps.observaciones.models import BancoObservacionesDocente
                banco = BancoObservacionesDocente.objects.get(id=banco_id, docente=docente, activo=True)
            except BancoObservacionesDocente.DoesNotExist:
                messages.error(request, 'Banco de observaciones no válido.')
                return redirect('docente_revisar_informe', informe_id=informe_id)
            
            # Eliminar observaciones anteriores
            obs_count = informe.observaciones.count()
            informe.observaciones.all().delete()
            
            # Validar de nuevo con el banco seleccionado
            success, observaciones_generadas, error = DocenteService.validar_informe_con_ia(
                informe_id, docente, banco_especifico=banco
            )
            
            # Solo mostrar resultado final
            if success:
                messages.success(request, f'✅ Re-validación completada con banco "{banco.nombre}". Se generaron {len(observaciones_generadas)} nuevas observaciones (se eliminaron {obs_count} anteriores).')
            else:
                messages.error(request, f'❌ Error al re-validar: {error}')
            
            return redirect('docente_revisar_informe', informe_id=informe_id)
        
        # ACCIÓN 2: ACTUALIZAR OBSERVACIONES
        elif accion == 'actualizar_observaciones':
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
            recomendar = request.POST.get('recomendar')
            
            # Validaciones
            if not comentario_general or len(comentario_general.strip()) < 20:
                messages.error(request, 'Debe proporcionar un dictamen detallado (mínimo 20 caracteres).')
            elif not recomendar:
                messages.error(request, 'Debe seleccionar una recomendación (Aprobar o Rechazar).')
            else:
                # PRIMERO: Actualizar observaciones con los datos del formulario
                observaciones = informe.observaciones.all()
                count_confirmadas = 0
                
                for obs in observaciones:
                    obs_accion = request.POST.get(f'obs_accion_{obs.id}')
                    obs_comentario = request.POST.get(f'obs_comentario_{obs.id}', '')
                    obs_severidad = request.POST.get(f'obs_severidad_{obs.id}')
                    
                    if obs_accion == 'confirmar':
                        obs.estado = ObservacionGenerada.ESTADO_CONFIRMADA
                        count_confirmadas += 1
                    elif obs_accion == 'descartar':
                        obs.estado = ObservacionGenerada.ESTADO_DESCARTADA
                    
                    obs.comentario_docente = obs_comentario
                    if obs_severidad:
                        obs.severidad = obs_severidad
                    obs.save()
                
                # Validar: Si recomienda rechazar, debe haber al menos 1 observación confirmada
                if recomendar == 'rechazar' and count_confirmadas == 0:
                    messages.warning(request, 
                        '⚠️ Si recomiendas RECHAZAR, debes confirmar al menos 1 observación. '
                        'De lo contrario, considera recomendar APROBAR.'
                    )
                    return redirect('docente_revisar_informe', informe_id=informe_id)
                
                # LUEGO: Enviar dictamen
                success, informe_actualizado, error = DocenteService.enviar_dictamen_a_presidente(
                    informe_id, docente, comentario_general, recomendar == 'aprobar'
                )
                
                if success:
                    obs_texto = f"con {count_confirmadas} observación(es) confirmada(s)" if count_confirmadas > 0 else "sin observaciones"
                    messages.success(request, f'✅ Dictamen enviado al presidente exitosamente {obs_texto}.')
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
        'bancos_disponibles': bancos_disponibles,  # v2.1: Lista de bancos para elegir
    }
    
    return render(request, 'docente/revisar.html', context)


@requiere_rol('docente')
def docente_ver_informe(request, informe_id):
    """
    Ver detalle de un informe (solo lectura)
    """
    
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
    
    return render(request, 'docente/ver.html', context)


@requiere_rol('docente')
def docente_historial(request):
    """
    Ver historial de informes revisados
    """
    
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


@requiere_rol('docente')
def docente_notificaciones(request):
    """
    Ver todas las notificaciones
    """
    
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
