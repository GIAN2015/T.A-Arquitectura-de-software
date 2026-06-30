from apps.informes.models import Informe


def obtener_por_id(informe_id):
    return Informe.objects.get(id=informe_id)


def listar_todos():
    return Informe.objects.all()


def listar_ultimos(limite=10):
    return Informe.objects.select_related('usuario').order_by('-fecha_registro')[:limite]


def contar_todos():
    return Informe.objects.count()


def contar_por_estado(estado):
    return Informe.objects.filter(estado=estado).count()


def listar_por_usuario(usuario):
    return Informe.objects.filter(usuario=usuario).order_by('-fecha_registro')
