from apps.reglamento.models import Reglamento


def obtener_activo():
    return Reglamento.objects.filter(activo=True).first()


def listar_todos():
    return Reglamento.objects.all().order_by('-activo', '-id')
