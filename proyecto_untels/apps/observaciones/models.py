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
    # Estados de revisión de observación
    ESTADO_PENDIENTE = 'pendiente'          # IA generó, esperando revisión docente
    ESTADO_CONFIRMADA = 'confirmada'        # Docente confirmó que es válida
    ESTADO_DESCARTADA = 'descartada'        # Docente dice que no aplica
    ESTADO_CORREGIDA = 'corregida'          # Alumno corrigió
    
    ESTADO_CHOICES = [
        (ESTADO_PENDIENTE, 'Pendiente de Revisión'),
        (ESTADO_CONFIRMADA, 'Confirmada por Docente'),
        (ESTADO_DESCARTADA, 'Descartada por Docente'),
        (ESTADO_CORREGIDA, 'Corregida por Alumno'),
    ]
    
    informe = models.ForeignKey(Informe, on_delete=models.CASCADE, related_name='observaciones')
    seccion = models.CharField(max_length=100)
    observacion = models.TextField()
    ubicacion_error = models.CharField(max_length=255)
    
    # Revisión docente
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default=ESTADO_PENDIENTE
    )
    comentario_docente = models.TextField(blank=True, null=True)
    fecha_revision = models.DateTimeField(null=True, blank=True)
    
    # Severidad (puede ser definida por IA o docente)
    SEVERIDAD_CRITICA = 'critica'
    SEVERIDAD_IMPORTANTE = 'importante'
    SEVERIDAD_MENOR = 'menor'
    SEVERIDAD_SUGERENCIA = 'sugerencia'
    
    SEVERIDAD_CHOICES = [
        (SEVERIDAD_CRITICA, 'Crítica - Debe Corregirse'),
        (SEVERIDAD_IMPORTANTE, 'Importante'),
        (SEVERIDAD_MENOR, 'Menor'),
        (SEVERIDAD_SUGERENCIA, 'Sugerencia'),
    ]
    
    severidad = models.CharField(
        max_length=20,
        choices=SEVERIDAD_CHOICES,
        default=SEVERIDAD_IMPORTANTE
    )

    class Meta:
        db_table = 'observacion_generada'

    def __str__(self):
        return f"{self.seccion} - {self.observacion[:50]}"
