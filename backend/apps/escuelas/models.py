"""
Modelos para gestión de Escuelas Profesionales
Capa de Datos - Clean Architecture
"""
from django.db import models


class Escuela(models.Model):
    """
    Representa una escuela profesional (carrera) de la universidad
    Cada escuela tiene un presidente asignado
    """
    nombre = models.CharField(
        max_length=200,
        help_text="Ej: Ingeniería de Sistemas, Ingeniería Ambiental"
    )
    codigo = models.CharField(
        max_length=20, 
        unique=True,
        help_text="Código único de la escuela (Ej: IS, IA, IM)"
    )
    presidente = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='escuela_presidida',
        limit_choices_to={'tipo_usuario': 'presidente'},
        help_text="Presidente de esta escuela"
    )
    activo = models.BooleanField(
        default=True,
        help_text="Si la escuela está activa"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'escuela'
        verbose_name = 'Escuela Profesional'
        verbose_name_plural = 'Escuelas Profesionales'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
