from django.db.models import Count

from apps.observaciones.models import BancoObservaciones, ObservacionGenerada


def listar_banco():
    return BancoObservaciones.objects.all().order_by('seccion')


def listar_por_informe(informe):
    return ObservacionGenerada.objects.filter(informe=informe)


def top_secciones(limite=5):
    return ObservacionGenerada.objects.values('seccion').annotate(total=Count('id')).order_by('-total')[:limite]


def top_observaciones(limite=10):
    return ObservacionGenerada.objects.values('seccion', 'observacion').annotate(total=Count('id')).order_by('-total')[:limite]
