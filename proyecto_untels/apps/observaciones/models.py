from django.db import models
from apps.informes.models import Informe

class BancoObservaciones(models.Model):
    seccion = models.CharField(max_length=100)
    descripcion = models.TextField()

    class Meta:
        db_table = 'banco_observaciones'

    def __str__(self):
        return f"{self.seccion}: {self.descripcion[:50]}"


class ObservacionGenerada(models.Model):
    ESTADO_PENDIENTE = 'pendiente'
    ESTADO_CONFIRMADA = 'confirmada'
    ESTADO_DESCARTADA = 'descartada'
    ESTADO_CORREGIDA = 'corregida'

    ESTADO_CHOICES = [
        (ESTADO_PENDIENTE, 'Pendiente de Revision'),
        (ESTADO_CONFIRMADA, 'Confirmada por Docente'),
        (ESTADO_DESCARTADA, 'Descartada por Docente'),
        (ESTADO_CORREGIDA, 'Corregida por Alumno'),
    ]

    SEVERIDAD_CRITICA = 'critica'
    SEVERIDAD_IMPORTANTE = 'importante'
    SEVERIDAD_MENOR = 'menor'
    SEVERIDAD_SUGERENCIA = 'sugerencia'

    SEVERIDAD_CHOICES = [
        (SEVERIDAD_CRITICA, 'Critica'),
        (SEVERIDAD_IMPORTANTE, 'Importante'),
        (SEVERIDAD_MENOR, 'Menor'),
        (SEVERIDAD_SUGERENCIA, 'Sugerencia'),
    ]

    informe = models.ForeignKey(Informe, on_delete=models.CASCADE, related_name='observaciones')
    seccion = models.CharField(max_length=200)
    observacion = models.TextField(blank=True, default='')
    sustento = models.TextField(blank=True, default='')
    ubicacion_error = models.CharField(max_length=255, blank=True, default='')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ESTADO_PENDIENTE)
    estado_conformidad = models.CharField(max_length=20, default='Observado')
    comentario_docente = models.TextField(blank=True, default='')
    fecha_revision = models.DateTimeField(null=True, blank=True)
    severidad = models.CharField(max_length=20, choices=SEVERIDAD_CHOICES, default=SEVERIDAD_IMPORTANTE)

    class Meta:
        db_table = 'observacion_generada'

    def __str__(self):
        return f"{self.seccion} - {self.estado_conformidad}"
