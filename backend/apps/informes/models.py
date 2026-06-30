from django.db import models
from apps.usuarios.models import Usuario
from apps.informes.state import get_state


class Informe(models.Model):
    """
    Informe de práctica preprofesional enviado por estudiante
    Pasa por múltiples estados y roles
    Versión 2.0 - Flujo completo multi-rol
    """
    # ESTADOS COMPLETOS DEL NUEVO FLUJO v2.0
    ESTADO_ENVIADO = 'enviado'
    ESTADO_PENDIENTE_SECRETARIA = 'pendiente_secretaria'
    ESTADO_PENDIENTE_PRESIDENTE = 'pendiente_presidente'
    ESTADO_PENDIENTE_DOCENTE = 'pendiente_docente'
    ESTADO_VALIDANDO_IA = 'validando_ia'
    ESTADO_REVISION_DOCENTE = 'revision_docente'
    ESTADO_PENDIENTE_APROBACION_PRESIDENTE = 'pendiente_aprobacion_presidente'
    ESTADO_APROBADO_PRESIDENTE = 'aprobado_presidente'
    ESTADO_RECHAZADO_PRESIDENTE = 'rechazado_presidente'
    ESTADO_APROBADO_FINAL = 'aprobado_final'
    ESTADO_RECHAZADO_ESTUDIANTE = 'rechazado_estudiante'
    
    # MANTENER estados antiguos para compatibilidad (deprecados)
    ESTADO_VALIDANDO = 'validando'                  # DEPRECADO - usar ESTADO_VALIDANDO_IA
    ESTADO_OBSERVADO = 'observado'                  # DEPRECADO - usar ESTADO_REVISION_DOCENTE
    ESTADO_EN_REVISION_DOCENTE = 'revision_docente' # OK - se mantiene
    ESTADO_RECHAZADO = 'rechazado'                  # DEPRECADO - usar ESTADO_RECHAZADO_ESTUDIANTE
    ESTADO_APROBADO = 'aprobado'                    # DEPRECADO - usar ESTADO_APROBADO_FINAL
    ESTADO_COMPLETADO = 'completado'                # DEPRECADO - usar ESTADO_APROBADO_FINAL

    ESTADO_CHOICES = [
        (ESTADO_ENVIADO, 'Enviado por Estudiante'),
        (ESTADO_PENDIENTE_SECRETARIA, 'Pendiente - Secretaría'),
        (ESTADO_PENDIENTE_PRESIDENTE, 'Pendiente - Presidente'),
        (ESTADO_PENDIENTE_DOCENTE, 'Pendiente - Docente Asignado'),
        (ESTADO_VALIDANDO_IA, 'Validando con IA'),
        (ESTADO_REVISION_DOCENTE, 'En Revisión del Docente'),
        (ESTADO_PENDIENTE_APROBACION_PRESIDENTE, 'Pendiente Aprobación Presidente'),
        (ESTADO_APROBADO_PRESIDENTE, 'Aprobado por Presidente'),
        (ESTADO_RECHAZADO_PRESIDENTE, 'Rechazado por Presidente'),
        (ESTADO_APROBADO_FINAL, 'APROBADO FINAL'),
        (ESTADO_RECHAZADO_ESTUDIANTE, 'Rechazado - Estudiante debe Corregir'),
        # Deprecados pero mantenidos para compatibilidad
        (ESTADO_VALIDANDO, 'Validando con IA (deprecado)'),
        (ESTADO_OBSERVADO, 'Con Observaciones (deprecado)'),
        (ESTADO_RECHAZADO, 'Rechazado (deprecado)'),
        (ESTADO_APROBADO, 'Aprobado (deprecado)'),
        (ESTADO_COMPLETADO, 'Completado (deprecado)'),
    ]

    # Campos básicos
    usuario = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE,
        related_name='informes_enviados',
        help_text="Estudiante que envió el informe"
    )
    nombre_archivo = models.CharField(max_length=255)
    archivo = models.FileField(
        upload_to='informes/%Y/%m/',
        null=True,
        blank=True,
        help_text="Archivo PDF o DOCX del informe"
    )
    contenido = models.TextField(help_text="Texto extraído del archivo")
    estado = models.CharField(
        max_length=50,
        choices=ESTADO_CHOICES,
        default=ESTADO_ENVIADO,
    )
    
    # NUEVO v2.0: Asignaciones de roles
    secretaria_asignada = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='informes_secretaria',
        limit_choices_to={'tipo_usuario': 'secretaria'},
        help_text="Secretaria que procesó el informe"
    )
    presidente_asignado = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='informes_presidente',
        limit_choices_to={'tipo_usuario': 'presidente'},
        help_text="Presidente de escuela asignado"
    )
    docente_revisor = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='informes_docente',
        limit_choices_to={'tipo_usuario': 'docente'},
        help_text="Docente revisor asignado"
    )
    
    # NUEVO v2.0: Escuela
    escuela = models.ForeignKey(
        'escuelas.Escuela',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='informes',
        help_text="Escuela profesional del estudiante"
    )
    
    # NUEVO v2.0: Banco usado
    banco_observaciones_usado = models.ForeignKey(
        'observaciones.BancoObservacionesDocente',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='informes_validados',
        help_text="Banco de observaciones que usó el docente"
    )
    
    # Comentarios por rol
    comentario_secretaria = models.TextField(blank=True, null=True)
    comentario_presidente = models.TextField(blank=True, null=True)
    comentario_docente = models.TextField(blank=True, null=True)
    
    # Fechas de procesamiento
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_asignacion_secretaria = models.DateTimeField(null=True, blank=True)
    fecha_asignacion_presidente = models.DateTimeField(null=True, blank=True)
    fecha_asignacion_docente = models.DateTimeField(null=True, blank=True)
    fecha_revision_docente = models.DateTimeField(null=True, blank=True)
    fecha_aprobacion_presidente = models.DateTimeField(null=True, blank=True)
    fecha_completado = models.DateTimeField(null=True, blank=True)
    
    # Versionado
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
        verbose_name = 'Informe de Práctica'
        verbose_name_plural = 'Informes de Práctica'
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.nombre_archivo} - {self.usuario.nombre} [{self.get_estado_display()}]"

    def transition_to(self, next_state):
        """Cambiar de estado usando máquina de estados"""
        state = get_state(self.estado)
        state.transition(self, next_state)
        return self
