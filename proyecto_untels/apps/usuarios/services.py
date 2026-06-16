from .models import Usuario

def identificar_usuario(codigo: str, nombre: str) -> Usuario:
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
