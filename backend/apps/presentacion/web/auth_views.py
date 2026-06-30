from django.contrib import messages
from django.shortcuts import redirect, render

from apps.usuarios.services import autenticar_usuario, registrar_usuario


def login_view(request):
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

        messages.error(request, 'Código o contraseña incorrectos.')
        return render(request, 'login.html')

    return render(request, 'login.html')


def login_docente_view(request):
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

        messages.error(request, 'Código o contraseña incorrectos.')
        return render(request, 'login_docente.html')

    return render(request, 'login_docente.html')


def registro_view(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo', '').strip()
        nombre = request.POST.get('nombre', '').strip()
        password = request.POST.get('password', '').strip()
        password_confirm = request.POST.get('password_confirm', '').strip()
        tipo_usuario = request.POST.get('tipo_usuario', 'estudiante')

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

        messages.error(request, 'El código ya está registrado.')
        return render(request, 'registro.html')

    return render(request, 'registro.html')


def login_secretaria_view(request):
    """
    Login para Secretaria Académica
    NUEVO v2.0
    """
    if 'usuario_id' in request.session and request.session.get('usuario_tipo') == 'secretaria':
        return redirect('secretaria_dashboard')

    if request.method == 'POST':
        codigo = request.POST.get('codigo', '').strip()
        password = request.POST.get('password', '').strip()

        if not codigo or not password:
            messages.error(request, 'Por favor ingresa tu código y contraseña.')
            return render(request, 'login_secretaria.html')

        usuario = autenticar_usuario(codigo, password)
        if usuario:
            if usuario.tipo_usuario != 'secretaria':
                messages.error(request, 'Esta área es solo para secretarias académicas.')
                return render(request, 'login_secretaria.html')

            request.session['usuario_id'] = usuario.id
            request.session['usuario_codigo'] = usuario.codigo
            request.session['usuario_nombre'] = usuario.nombre
            request.session['usuario_tipo'] = usuario.tipo_usuario
            messages.success(request, f'Bienvenida, {usuario.nombre}')
            return redirect('secretaria_dashboard')

        messages.error(request, 'Código o contraseña incorrectos.')
        return render(request, 'login_secretaria.html')

    return render(request, 'login_secretaria.html')


def login_presidente_view(request):
    """
    Login para Presidente de Escuela
    NUEVO v2.0
    """
    if 'usuario_id' in request.session and request.session.get('usuario_tipo') == 'presidente':
        return redirect('presidente_dashboard')

    if request.method == 'POST':
        codigo = request.POST.get('codigo', '').strip()
        password = request.POST.get('password', '').strip()

        if not codigo or not password:
            messages.error(request, 'Por favor ingresa tu código y contraseña.')
            return render(request, 'login_presidente.html')

        usuario = autenticar_usuario(codigo, password)
        if usuario:
            if usuario.tipo_usuario != 'presidente':
                messages.error(request, 'Esta área es solo para presidentes de escuela.')
                return render(request, 'login_presidente.html')

            request.session['usuario_id'] = usuario.id
            request.session['usuario_codigo'] = usuario.codigo
            request.session['usuario_nombre'] = usuario.nombre
            request.session['usuario_tipo'] = usuario.tipo_usuario
            request.session['escuela_id'] = usuario.escuela.id if usuario.escuela else None
            request.session['escuela_nombre'] = usuario.escuela.nombre if usuario.escuela else 'Sin asignar'
            messages.success(request, f'Bienvenido, {usuario.nombre}')
            return redirect('presidente_dashboard')

        messages.error(request, 'Código o contraseña incorrectos.')
        return render(request, 'login_presidente.html')

    return render(request, 'login_presidente.html')


def logout_view(request):
    """
    Cerrar sesión para todos los roles
    """
    tipo = request.session.get('usuario_tipo')
    request.session.flush()
    messages.success(request, 'Has cerrado sesión correctamente.')

    # Redirigir según el tipo de usuario
    if tipo == 'docente':
        return redirect('login_docente')
    elif tipo == 'secretaria':
        return redirect('login_secretaria')
    elif tipo == 'presidente':
        return redirect('login_presidente')
    return redirect('login')
