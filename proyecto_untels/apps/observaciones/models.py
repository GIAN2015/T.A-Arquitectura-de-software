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
    informe = models.ForeignKey(Informe, on_delete=models.CASCADE, related_name='observaciones')
    seccion = models.CharField(max_length=100)
    observacion = models.TextField()
    ubicacion_error = models.CharField(max_length=255)

    class Meta:
        db_table = 'observacion_generada'

    def __str__(self):
        return f"{self.seccion} - {self.observacion[:50]}"
