from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from apps.informes.models import Informe
from apps.informes.services import leer_archivo
from apps.observaciones.models import ObservacionGenerada
from apps.observaciones.services import obtener_observaciones, validar_informe
from apps.reglamento.services import obtener_reglamento
from apps.usuarios.models import Usuario


def _verificar_estudiante(request):
    if 'usuario_id' not in request.session:
        return False
    if request.session.get('usuario_tipo') == 'docente':
        return False
    return True


def upload_view(request):
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
        if not archivo:
            messages.error(request, 'Por favor selecciona un archivo .docx o .pdf')
            return render(request, 'upload_report.html', context)
        if not archivo.name.lower().endswith(('.docx', '.pdf')):
            messages.error(request, 'Solo se permiten archivos .docx o .pdf')
            return render(request, 'upload_report.html', context)
        if archivo.size > 10 * 1024 * 1024:
            messages.error(request, 'El archivo es demasiado grande. Máximo 10MB.')
            return render(request, 'upload_report.html', context)

        informe = None
        try:
            usuario = Usuario.objects.get(id=request.session['usuario_id'])
            try:
                contenido = leer_archivo(archivo)
            except Exception:
                messages.error(request, 'Error al leer el archivo: archivo dañado o formato incorrecto.')
                return render(request, 'upload_report.html', context)

            if not contenido or len(contenido.strip()) < 50:
                messages.error(request, 'El archivo está vacío o tiene muy poco contenido.')
                return render(request, 'upload_report.html', context)

            informe_previo = Informe.objects.filter(
                usuario=usuario,
                estado=Informe.ESTADO_RECHAZADO,
            ).order_by('-fecha_registro').first()

            version = 1
            if informe_previo:
                version = informe_previo.version + 1
                messages.info(request, f'Detectado reenvío - Versión {version} del informe.')

            informe = Informe.objects.create(
                usuario=usuario,
                nombre_archivo=archivo.name,
                contenido=contenido,
                estado=Informe.ESTADO_ENVIADO,
                version=version,
                informe_anterior=informe_previo,
            )
            informe.transition_to(Informe.ESTADO_VALIDANDO)
            informe.save()

            try:
                reglamento = obtener_reglamento()
                observaciones_banco = obtener_observaciones()
                resultado = validar_informe(contenido, reglamento, observaciones_banco)
            except Exception:
                resultado = []
                messages.warning(request, 'La IA no pudo procesar el informe. Será revisado manualmente por el docente.')

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
                    severidad=severidad,
                )

            if resultado:
                informe.transition_to(Informe.ESTADO_OBSERVADO)
                messages.success(request, f'Informe procesado. La IA detectó {len(resultado)} observación(es). Esperando revisión del docente.')
            else:
                informe.transition_to(Informe.ESTADO_OBSERVADO)
                messages.success(request, 'Informe procesado. No se detectaron observaciones por la IA. Esperando revisión del docente.')

            informe.save()
            return redirect('resultado', informe_id=informe.id)
        except Exception as e:
            if informe:
                if informe.estado == Informe.ESTADO_VALIDANDO:
                    informe.transition_to(Informe.ESTADO_OBSERVADO)
                informe.save()
            messages.error(request, f'Error al procesar el informe: {str(e)}. El informe fue guardado para revisión manual.')
            return render(request, 'upload_report.html', context)

    return render(request, 'upload_report.html', context)


def resultado_view(request, informe_id):
    if 'usuario_id' not in request.session:
        return redirect('login')

    informe = get_object_or_404(Informe, id=informe_id)
    usuario_id = request.session.get('usuario_id')
    tipo = request.session.get('usuario_tipo')

    if tipo != 'docente' and informe.usuario_id != usuario_id:
        messages.error(request, 'No tienes permiso para ver este informe.')
        return redirect('historial')

    if tipo == 'docente':
        observaciones = ObservacionGenerada.objects.filter(informe=informe).order_by('severidad', 'id')
    elif informe.docente_revisor_id:
        observaciones = ObservacionGenerada.objects.filter(
            informe=informe,
            estado__in=[
                ObservacionGenerada.ESTADO_CONFIRMADA,
                ObservacionGenerada.ESTADO_CORREGIDA,
            ],
        ).order_by('severidad', 'id')
    else:
        observaciones = ObservacionGenerada.objects.none()

    context = {
        'informe': informe,
        'observaciones': observaciones,
        'usuario': informe.usuario,
        'es_docente': tipo == 'docente',
        'mostrar_feedback_docente': tipo == 'docente' or bool(informe.docente_revisor_id),
    }
    return render(request, 'validation_result.html', context)


def historial_view(request):
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
