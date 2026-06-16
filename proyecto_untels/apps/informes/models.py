from django.db import models
from apps.usuarios.models import Usuario

class Informe(models.Model):
    ESTADO_ENVIADO = 'enviado'
    ESTADO_EN_REVISION = 'en_revision'
    ESTADO_COMPLETADO = 'completado'

    ESTADO_CHOICES = [
        (ESTADO_ENVIADO, 'Enviado'),
        (ESTADO_EN_REVISION, 'En Revisión'),
        (ESTADO_COMPLETADO, 'Completado'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre_archivo = models.CharField(max_length=255)
    contenido = models.TextField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default=ESTADO_ENVIADO,
    )

    class Meta:
        db_table = 'informe'

    def __str__(self):
        return f"{self.nombre_archivo} [{self.get_estado_display()}]"
