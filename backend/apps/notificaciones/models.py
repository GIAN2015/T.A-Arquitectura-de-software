"""
Modelos para Sistema de Notificaciones
Capa de Datos - Clean Architecture
Versión 2.0
"""
from django.db import models
from apps.usuarios.models import Usuario
from apps.informes.models import Informe


class Notificacion(models.Model):
    """
    Sistema de notificaciones para todos los roles
    """
    TIPO_CHOICES = [
        ('nuevo_informe', 'Nuevo Informe Recibido'),
        ('asignado_presidente', 'Informe Asignado a Presidente'),
        ('asignado_docente', 'Informe Asignado a Docente'),
        ('revision_completa', 'Revisión Completada'),
        ('aprobado_presidente', 'Aprobado por Presidente'),
        ('rechazado_presidente', 'Rechazado por Presidente'),
        ('aprobado_final', 'Informe Aprobado - Proceso Completo'),
        ('rechazado_estudiante', 'Informe Rechazado - Requiere Correcciones'),
    ]
    
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='notificaciones',
        help_text="Usuario que recibe la notificación"
    )
    informe = models.ForeignKey(
        Informe,
        on_delete=models.CASCADE,
        related_name='notificaciones',
        help_text="Informe relacionado"
    )
    tipo = models.CharField(
        max_length=50,
        choices=TIPO_CHOICES,
        help_text="Tipo de notificación"
    )
    titulo = models.CharField(
        max_length=255,
        help_text="Título de la notificación"
    )
    mensaje = models.TextField(
        help_text="Mensaje completo de la notificación"
    )
    leida = models.BooleanField(
        default=False,
        help_text="Si el usuario ya leyó la notificación"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_leida = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'notificacion'
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.usuario.nombre} - {self.titulo} {'(Leída)' if self.leida else '(No leída)'}"
    
    def marcar_como_leida(self):
        """Marcar notificación como leída"""
        from django.utils import timezone
        self.leida = True
        self.fecha_leida = timezone.now()
        self.save()
