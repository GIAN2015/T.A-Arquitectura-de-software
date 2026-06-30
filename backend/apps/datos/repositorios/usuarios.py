from apps.usuarios.models import Usuario


def obtener_por_id(usuario_id):
    return Usuario.objects.get(id=usuario_id)


def obtener_por_codigo(codigo):
    return Usuario.objects.filter(codigo=codigo).first()


def listar_todos():
    return Usuario.objects.all()


def contar_todos():
    return Usuario.objects.count()


def contar_por_tipo(tipo_usuario):
    return Usuario.objects.filter(tipo_usuario=tipo_usuario).count()
