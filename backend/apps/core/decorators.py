"""
Decoradores para validación de roles y sesiones
Clean Architecture - Core Layer
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def requiere_rol(*roles_permitidos):
    """
    Decorador para verificar que el usuario tiene uno de los roles permitidos.
    
    Uso:
        @requiere_rol('estudiante')
        @requiere_rol('secretaria', 'presidente')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # 1. Verificar que hay sesión activa
            if 'usuario_id' not in request.session:
                messages.warning(request, 'Debes iniciar sesión primero.')
                # Redirigir al login apropiado según el primer rol permitido
                if 'estudiante' in roles_permitidos:
                    return redirect('login')
                elif 'secretaria' in roles_permitidos:
                    return redirect('login_secretaria')
                elif 'presidente' in roles_permitidos:
                    return redirect('login_presidente')
                elif 'docente' in roles_permitidos:
                    return redirect('login_docente')
                else:
                    return redirect('login')
            
            # 2. Obtener tipo de usuario de la sesión
            usuario_tipo = request.session.get('usuario_tipo')
            
            # 3. Verificar que el tipo está en los roles permitidos
            if usuario_tipo not in roles_permitidos:
                messages.error(
                    request, 
                    f'Acceso denegado. Esta página es solo para {", ".join(roles_permitidos)}.'
                )
                
                # Redirigir al dashboard correcto según su rol actual
                if usuario_tipo == 'estudiante':
                    return redirect('upload')  # Dashboard de estudiante
                elif usuario_tipo == 'secretaria':
                    return redirect('secretaria_dashboard')
                elif usuario_tipo == 'presidente':
                    return redirect('presidente_dashboard')
                elif usuario_tipo == 'docente':
                    return redirect('panel_docente')  # Dashboard de docente
                else:
                    return redirect('login')
            
            # 4. Todo OK, ejecutar la vista
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator


def requiere_sesion(view_func):
    """
    Decorador simple que solo verifica que haya sesión activa.
    Útil para vistas públicas que requieren login pero no un rol específico.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'usuario_id' not in request.session:
            messages.warning(request, 'Debes iniciar sesión primero.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    
    return wrapper
