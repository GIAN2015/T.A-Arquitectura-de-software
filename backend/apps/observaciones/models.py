from django.db import models
from apps.informes.models import Informe


class BancoObservaciones(models.Model):
    """
    Banco de observaciones GLOBAL
    Usado para observaciones comunes generales
    """
    seccion = models.CharField(max_length=100)
    descripcion = models.TextField()

    class Meta:
        db_table = 'banco_observaciones'

    def __str__(self):
        return f"{self.seccion}: {self.descripcion[:50]}"


class BancoObservacionesDocente(models.Model):
    """
    Banco de observaciones personalizado de cada docente
    Cada docente puede subir su propio PDF/DOCX con observaciones
    NUEVO en v2.0
    """
    docente = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.CASCADE,
        related_name='bancos_observaciones',
        limit_choices_to={'tipo_usuario': 'docente'},
        help_text="Docente propietario de este banco"
    )
    nombre = models.CharField(
        max_length=255,
        help_text="Nombre descriptivo del banco (Ej: Observaciones 2026-1)"
    )
    archivo = models.FileField(
        upload_to='bancos_observaciones/%Y/%m/',
        help_text="Archivo PDF o DOCX con observaciones"
    )
    contenido_extraido = models.TextField(
        blank=True,
        help_text="Texto extraído del archivo para usar con IA"
    )
    activo = models.BooleanField(
        default=True,
        help_text="Si este banco está activo (solo uno activo por docente)"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'banco_observaciones_docente'
        verbose_name = 'Banco de Observaciones del Docente'
        verbose_name_plural = 'Bancos de Observaciones de Docentes'
        ordering = ['-activo', '-fecha_creacion']
        unique_together = [['docente', 'nombre']]

    def __str__(self):
        return f"{self.docente.nombre} - {self.nombre} {'(Activo)' if self.activo else ''}"
    
    def save(self, *args, **kwargs):
        """
        Guardar banco de observaciones
        Versión 2.1: Permite múltiples bancos activos
        El docente elige cuál usar al momento de validar
        """
        super().save(*args, **kwargs)

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
