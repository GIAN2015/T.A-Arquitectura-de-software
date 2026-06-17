from .models import Usuario

def identificar_usuario(codigo: str, nombre: str) -> Usuario:
    """Para compatibilidad con el sistema anterior (sin contraseña)"""
    try:
        year = int(codigo[:4])
        tipo = 'egresado' if year < 2020 else 'estudiante'
    except (ValueError, IndexError):
        tipo = 'estudiante'

    usuario, _ = Usuario.objects.get_or_create(
        codigo=codigo,
        defaults={'nombre': nombre, 'tipo_usuario': tipo}
    )
    usuario.nombre = nombre
    usuario.tipo_usuario = tipo
    usuario.save()
    return usuario

def autenticar_usuario(codigo: str, password: str):
    """Autentica un usuario con contraseña"""
    try:
        usuario = Usuario.objects.get(codigo=codigo)
        if usuario.check_password(password):
            return usuario
        return None
    except Usuario.DoesNotExist:
        return None

def registrar_usuario(codigo: str, nombre: str, password: str, tipo_usuario: str = 'estudiante'):
    """Registra un nuevo usuario con contraseña"""
    if Usuario.objects.filter(codigo=codigo).exists():
        return None
    
    usuario = Usuario.objects.create(
        codigo=codigo,
        nombre=nombre,
        tipo_usuario=tipo_usuario
    )
    usuario.set_password(password)
    return usuario
