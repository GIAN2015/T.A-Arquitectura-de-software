from django.db import models
from apps.usuarios.models import Usuario

class Informe(models.Model):
    ESTADO_ENVIADO = 'enviado'
    ESTADO_VALIDANDO = 'validando'
    ESTADO_OBSERVADO = 'observado'
    ESTADO_EN_REVISION_DOCENTE = 'revision_docente'
    ESTADO_RECHAZADO = 'rechazado'
    ESTADO_APROBADO = 'aprobado'
    ESTADO_COMPLETADO = 'completado'

    ESTADO_CHOICES = [
        (ESTADO_ENVIADO, 'Enviado'),
        (ESTADO_VALIDANDO, 'Validando con IA'),
        (ESTADO_OBSERVADO, 'Con Observaciones'),
        (ESTADO_EN_REVISION_DOCENTE, 'En Revision del Docente'),
        (ESTADO_RECHAZADO, 'Rechazado - Requiere Correcciones'),
        (ESTADO_APROBADO, 'Aprobado por Docente'),
        (ESTADO_COMPLETADO, 'Completado'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre_archivo = models.CharField(max_length=255)
    contenido = models.TextField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_revision_docente = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(
        max_length=30,
        choices=ESTADO_CHOICES,
        default=ESTADO_ENVIADO,
    )
    docente_revisor = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='informes_revisados'
    )
    comentario_docente = models.TextField(blank=True, default='')
    version = models.IntegerField(default=1)
    informe_anterior = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='versiones_posteriores'
    )

    class Meta:
        db_table = 'informe'

    def __str__(self):
        return f"{self.nombre_archivo} [{self.get_estado_display()}]"
