from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.usuarios.services import identificar_usuario
from apps.informes.models import Informe
from apps.informes.services import leer_archivo
from apps.reglamento.services import obtener_reglamento
from apps.observaciones.services import obtener_observaciones, validar_informe
from apps.observaciones.models import ObservacionGenerada
import json

def login_view(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo', '').strip()
        nombre = request.POST.get('nombre', '').strip()
        if not codigo or not nombre:
            messages.error(request, 'Por favor ingresa tu código y nombre completo.')
            return render(request, 'login.html')
        usuario = identificar_usuario(codigo, nombre)
        request.session['usuario_id'] = usuario.id
        request.session['usuario_codigo'] = usuario.codigo
        request.session['usuario_nombre'] = usuario.nombre
        request.session['usuario_tipo'] = usuario.tipo_usuario
        return redirect('upload')
    return render(request, 'login.html')

def upload_view(request):
    if 'usuario_id' not in request.session:
        return redirect('login')

    context = {
        'codigo': request.session.get('usuario_codigo'),
        'nombre': request.session.get('usuario_nombre'),
        'tipo': request.session.get('usuario_tipo'),
    }

    if request.method == 'POST':
        archivo = request.FILES.get('informe')
        if not archivo:
            messages.error(request, 'Por favor selecciona un archivo .docx')
            return render(request, 'upload_report.html', context)
        if not archivo.name.endswith('.docx'):
            messages.error(request, 'Solo se permiten archivos .docx')
            return render(request, 'upload_report.html', context)

        try:
            from apps.usuarios.models import Usuario
            usuario = Usuario.objects.get(id=request.session['usuario_id'])
            contenido = leer_archivo(archivo)

            # Estado 1: ENVIADO — se registra la solicitud
            informe = Informe.objects.create(
                usuario=usuario,
                nombre_archivo=archivo.name,
                contenido=contenido,
                estado=Informe.ESTADO_ENVIADO,
            )

            # Estado 2: EN REVISIÓN — la IA empieza a procesar
            informe.estado = Informe.ESTADO_EN_REVISION
            informe.save()

            reglamento = obtener_reglamento()
            observaciones_banco = obtener_observaciones()
            resultado = validar_informe(contenido, reglamento, observaciones_banco)

            for obs in resultado:
                ObservacionGenerada.objects.create(
                    informe=informe,
                    seccion=obs.get('seccion', ''),
                    observacion=obs.get('observacion', ''),
                    ubicacion_error=obs.get('ubicacion', '')
                )

            # Estado 3: COMPLETADO — revisión finalizada
            informe.estado = Informe.ESTADO_COMPLETADO
            informe.save()

            return redirect('resultado', informe_id=informe.id)
        except Exception as e:
            messages.error(request, f'Error al procesar el informe: {str(e)}')
            return render(request, 'upload_report.html', context)

    return render(request, 'upload_report.html', context)

def resultado_view(request, informe_id):
    informe = get_object_or_404(Informe, id=informe_id)
    observaciones = ObservacionGenerada.objects.filter(informe=informe)
    context = {
        'informe': informe,
        'observaciones': observaciones,
        'usuario': informe.usuario,
    }
    return render(request, 'validation_result.html', context)
