"""
VISTAS DE ADMINISTRACIÓN PERSONALIZADAS
Panel de administración para profesores/administradores del sistema

Clean Architecture: Separación entre panel docente y panel admin
- Panel Docente: Ver informes de estudiantes
- Panel Admin: Gestionar todo el sistema (usuarios, reglamento, estadísticas)
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from apps.usuarios.models import Usuario
from apps.informes.models import Informe
from apps.reglamento.models import Reglamento
from apps.observaciones.models import BancoObservaciones, ObservacionGenerada


def admin_dashboard(request):
    """
    Dashboard principal del administrador
    Muestra estadísticas generales del sistema
    """
    # Verificar que sea docente
    if 'usuario_id' not in request.session:
        return redirect('login_docente')
    
    if request.session.get('usuario_tipo') != 'docente':
        messages.error(request, 'Acceso denegado. Solo docentes pueden acceder al panel de administración.')
        return redirect('upload')
    
    # Estadísticas generales
    total_usuarios = Usuario.objects.count()
    total_estudiantes = Usuario.objects.filter(tipo_usuario='estudiante').count()
    total_egresados = Usuario.objects.filter(tipo_usuario='egresado').count()
    total_docentes = Usuario.objects.filter(tipo_usuario='docente').count()
    
    total_informes = Informe.objects.count()
    informes_enviados = Informe.objects.filter(estado=Informe.ESTADO_ENVIADO).count()
    informes_validando = Informe.objects.filter(estado=Informe.ESTADO_VALIDANDO).count()
    informes_observado = Informe.objects.filter(estado=Informe.ESTADO_OBSERVADO).count()
    informes_revision_docente = Informe.objects.filter(estado=Informe.ESTADO_EN_REVISION_DOCENTE).count()
    informes_rechazado = Informe.objects.filter(estado=Informe.ESTADO_RECHAZADO).count()
    informes_aprobado = Informe.objects.filter(estado=Informe.ESTADO_APROBADO).count()
    informes_completados = Informe.objects.filter(estado=Informe.ESTADO_COMPLETADO).count()
    
    # Informes recientes (últimos 7 días)
    hace_7_dias = timezone.now() - timedelta(days=7)
    informes_recientes = Informe.objects.filter(fecha_registro__gte=hace_7_dias).count()
    
    # Observaciones más frecuentes
    observaciones_frecuentes = ObservacionGenerada.objects.values('seccion').annotate(
        total=Count('id')
    ).order_by('-total')[:5]
    
    # Últimos informes
    ultimos_informes = Informe.objects.select_related('usuario').order_by('-fecha_registro')[:10]
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        
        # Estadísticas de usuarios
        'total_usuarios': total_usuarios,
        'total_estudiantes': total_estudiantes,
        'total_egresados': total_egresados,
        'total_docentes': total_docentes,
        
        # Estadísticas de informes
        'total_informes': total_informes,
        'informes_enviados': informes_enviados,
        'informes_validando': informes_validando,
        'informes_observado': informes_observado,
        'informes_revision_docente': informes_revision_docente,
        'informes_rechazado': informes_rechazado,
        'informes_aprobado': informes_aprobado,
        'informes_completados': informes_completados,
        'informes_recientes': informes_recientes,
        
        # Datos adicionales
        'observaciones_frecuentes': observaciones_frecuentes,
        'ultimos_informes': ultimos_informes,
    }
    
    return render(request, 'admin/dashboard.html', context)


def admin_usuarios(request):
    """
    Gestión de usuarios del sistema
    """
    if 'usuario_id' not in request.session:
        return redirect('login_docente')
    
    if request.session.get('usuario_tipo') != 'docente':
        messages.error(request, 'Acceso denegado.')
        return redirect('upload')
    
    # Filtros
    tipo_filtro = request.GET.get('tipo', '')
    busqueda = request.GET.get('q', '')
    
    usuarios = Usuario.objects.all()
    
    if tipo_filtro:
        usuarios = usuarios.filter(tipo_usuario=tipo_filtro)
    
    if busqueda:
        usuarios = usuarios.filter(
            Q(codigo__icontains=busqueda) | 
            Q(nombre__icontains=busqueda)
        )
    
    usuarios = usuarios.order_by('tipo_usuario', 'codigo')
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'usuarios': usuarios,
        'tipo_filtro': tipo_filtro,
        'busqueda': busqueda,
    }
    
    return render(request, 'admin/usuarios.html', context)


def admin_usuario_detalle(request, usuario_id):
    """
    Detalle de un usuario específico
    """
    if 'usuario_id' not in request.session:
        return redirect('login_docente')
    
    if request.session.get('usuario_tipo') != 'docente':
        messages.error(request, 'Acceso denegado.')
        return redirect('upload')
    
    usuario = get_object_or_404(Usuario, id=usuario_id)
    informes = Informe.objects.filter(usuario=usuario).order_by('-fecha_registro')
    
    # Estadísticas del usuario
    total_informes = informes.count()
    informes_completados = informes.filter(estado=Informe.ESTADO_COMPLETADO).count()
    total_observaciones = ObservacionGenerada.objects.filter(informe__usuario=usuario).count()
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'usuario_detalle': usuario,
        'informes': informes,
        'total_informes': total_informes,
        'informes_completados': informes_completados,
        'total_observaciones': total_observaciones,
    }
    
    return render(request, 'admin/usuario_detalle.html', context)


def admin_reglamento(request):
    """
    Gestión del reglamento institucional
    """
    if 'usuario_id' not in request.session:
        return redirect('login_docente')
    
    if request.session.get('usuario_tipo') != 'docente':
        messages.error(request, 'Acceso denegado.')
        return redirect('upload')
    
    reglamentos = Reglamento.objects.all().order_by('-activo', '-id')
    
    # Actualizar reglamento
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        contenido = request.POST.get('contenido')
        
        if nombre and contenido:
            # Desactivar todos los reglamentos anteriores
            Reglamento.objects.all().update(activo=False)
            
            # Crear nuevo reglamento activo
            Reglamento.objects.create(
                nombre=nombre,
                contenido=contenido,
                activo=True
            )
            
            messages.success(request, 'Reglamento actualizado exitosamente.')
            return redirect('admin_reglamento')
        else:
            messages.error(request, 'Nombre y contenido son obligatorios.')
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'reglamentos': reglamentos,
    }
    
    return render(request, 'admin/reglamento.html', context)


def admin_observaciones(request):
    """
    Gestión del banco de observaciones
    """
    if 'usuario_id' not in request.session:
        return redirect('login_docente')
    
    if request.session.get('usuario_tipo') != 'docente':
        messages.error(request, 'Acceso denegado.')
        return redirect('upload')
    
    observaciones = BancoObservaciones.objects.all().order_by('seccion')
    
    # Agregar nueva observación
    if request.method == 'POST':
        seccion = request.POST.get('seccion')
        descripcion = request.POST.get('descripcion')
        
        if seccion and descripcion:
            BancoObservaciones.objects.create(
                seccion=seccion,
                descripcion=descripcion
            )
            messages.success(request, 'Observación agregada al banco.')
            return redirect('admin_observaciones')
        else:
            messages.error(request, 'Sección y descripción son obligatorios.')
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'observaciones': observaciones,
    }
    
    return render(request, 'admin/observaciones.html', context)


def admin_observacion_eliminar(request, obs_id):
    """
    Eliminar una observación del banco
    """
    if 'usuario_id' not in request.session:
        return redirect('login_docente')
    
    if request.session.get('usuario_tipo') != 'docente':
        messages.error(request, 'Acceso denegado.')
        return redirect('upload')
    
    if request.method != 'POST':
        messages.error(request, 'Método no permitido para eliminar observaciones.')
        return redirect('admin_observaciones')

    observacion = get_object_or_404(BancoObservaciones, id=obs_id)
    observacion.delete()
    
    messages.success(request, 'Observación eliminada del banco.')
    return redirect('admin_observaciones')


def admin_reportes(request):
    """
    Reportes y estadísticas avanzadas
    """
    if 'usuario_id' not in request.session:
        return redirect('login_docente')
    
    if request.session.get('usuario_tipo') != 'docente':
        messages.error(request, 'Acceso denegado.')
        return redirect('upload')
    
    # Informes por estado
    informes_por_estado = {
        'enviado': Informe.objects.filter(estado=Informe.ESTADO_ENVIADO).count(),
        'validando': Informe.objects.filter(estado=Informe.ESTADO_VALIDANDO).count(),
        'observado': Informe.objects.filter(estado=Informe.ESTADO_OBSERVADO).count(),
        'revision_docente': Informe.objects.filter(estado=Informe.ESTADO_EN_REVISION_DOCENTE).count(),
        'rechazado': Informe.objects.filter(estado=Informe.ESTADO_RECHAZADO).count(),
        'aprobado': Informe.objects.filter(estado=Informe.ESTADO_APROBADO).count(),
        'completado': Informe.objects.filter(estado=Informe.ESTADO_COMPLETADO).count(),
    }
    
    # Informes por tipo de usuario
    informes_estudiantes = Informe.objects.filter(usuario__tipo_usuario='estudiante').count()
    informes_egresados = Informe.objects.filter(usuario__tipo_usuario='egresado').count()
    
    # Observaciones más comunes
    observaciones_comunes = ObservacionGenerada.objects.values('seccion', 'observacion').annotate(
        total=Count('id')
    ).order_by('-total')[:10]
    
    # Usuarios más activos
    usuarios_activos = Usuario.objects.annotate(
        num_informes=Count('informe')
    ).filter(num_informes__gt=0).order_by('-num_informes')[:10]
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'informes_por_estado': informes_por_estado,
        'informes_estudiantes': informes_estudiantes,
        'informes_egresados': informes_egresados,
        'observaciones_comunes': observaciones_comunes,
        'usuarios_activos': usuarios_activos,
    }
    
    return render(request, 'admin/reportes.html', context)


def admin_revisar_informe(request, informe_id):
    """
    Vista para que el docente revise un informe y sus observaciones
    Puede aprobar/rechazar el informe y comentar cada observación
    """
    if 'usuario_id' not in request.session:
        return redirect('login_docente')
    
    if request.session.get('usuario_tipo') != 'docente':
        messages.error(request, 'Acceso denegado.')
        return redirect('login_docente')
    
    informe = get_object_or_404(Informe, id=informe_id)
    
    observaciones = informe.observaciones.all().order_by('seccion', 'id')
    
    # Procesar formulario de revisión
    if request.method == 'POST':
        accion = request.POST.get('accion')  # 'aprobar' o 'rechazar'
        comentario_general = request.POST.get('comentario_general', '')
        
        # Actualizar estado de cada observación
        for obs in observaciones:
            obs_accion = request.POST.get(f'obs_accion_{obs.id}')
            obs_comentario = request.POST.get(f'obs_comentario_{obs.id}', '')
            obs_severidad = request.POST.get(f'obs_severidad_{obs.id}')
            
            if obs_accion:
                if obs_accion == 'confirmar':
                    obs.estado = ObservacionGenerada.ESTADO_CONFIRMADA
                elif obs_accion == 'descartar':
                    obs.estado = ObservacionGenerada.ESTADO_DESCARTADA
                
                obs.comentario_docente = obs_comentario
                obs.severidad = obs_severidad if obs_severidad else obs.severidad
                obs.fecha_revision = timezone.now()
                obs.save()
        
        # Actualizar informe
        docente = Usuario.objects.get(id=request.session.get('usuario_id'))
        informe.docente_revisor = docente
        informe.comentario_docente = comentario_general
        informe.fecha_revision_docente = timezone.now()

        if informe.estado == Informe.ESTADO_OBSERVADO:
            informe.transition_to(Informe.ESTADO_EN_REVISION_DOCENTE)

        if accion == 'aprobar':
            informe.transition_to(Informe.ESTADO_APROBADO)
            messages.success(request, f'Informe "{informe.nombre_archivo}" aprobado exitosamente.')
        elif accion == 'rechazar':
            informe.transition_to(Informe.ESTADO_RECHAZADO)
            messages.warning(request, f'Informe "{informe.nombre_archivo}" rechazado. El alumno debe corregir.')
        
        informe.save()
        return redirect('panel_docente')
    
    # Agrupar observaciones por severidad
    obs_criticas = observaciones.filter(severidad=ObservacionGenerada.SEVERIDAD_CRITICA)
    obs_importantes = observaciones.filter(severidad=ObservacionGenerada.SEVERIDAD_IMPORTANTE)
    obs_menores = observaciones.filter(severidad=ObservacionGenerada.SEVERIDAD_MENOR)
    obs_sugerencias = observaciones.filter(severidad=ObservacionGenerada.SEVERIDAD_SUGERENCIA)
    
    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
        'informe': informe,
        'observaciones': observaciones,
        'obs_criticas': obs_criticas,
        'obs_importantes': obs_importantes,
        'obs_menores': obs_menores,
        'obs_sugerencias': obs_sugerencias,
        'total_observaciones': observaciones.count(),
    }
    
    return render(request, 'admin/revisar_informe.html', context)
