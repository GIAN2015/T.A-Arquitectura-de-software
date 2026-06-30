from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Usuario(models.Model):
    """
    Usuario del sistema con múltiples roles
    Versión 2.0 - Incluye Presidente y Secretaria
    """
    TIPO_CHOICES = [
        ('estudiante', 'Estudiante'),
        ('egresado', 'Egresado'),
        ('docente', 'Docente'),
        ('presidente', 'Presidente de Escuela'),
        ('secretaria', 'Secretaria Académica'),
    ]
    
    codigo = models.CharField(
        max_length=20, 
        unique=True,
        help_text="Código único del usuario"
    )
    nombre = models.CharField(max_length=200)
    tipo_usuario = models.CharField(
        max_length=20, 
        choices=TIPO_CHOICES, 
        default='estudiante'
    )
    password = models.CharField(max_length=255, blank=True, null=True)
    
    # NUEVO: Relación con escuela
    escuela = models.ForeignKey(
        'escuelas.Escuela',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios',
        help_text="Escuela a la que pertenece (estudiantes, docentes, presidente)"
    )
    
    # NUEVO: Email para notificaciones
    email = models.EmailField(
        blank=True,
        null=True,
        help_text="Email para notificaciones"
    )
    
    # NUEVO: Estado activo
    activo = models.BooleanField(
        default=True,
        help_text="Si el usuario está activo en el sistema"
    )
    
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['tipo_usuario', 'nombre']

    def __str__(self):
        return f"{self.codigo} - {self.nombre} ({self.get_tipo_usuario_display()})"
    
    def set_password(self, raw_password):
        """Encriptar contraseña"""
        self.password = make_password(raw_password)
        self.save()
    
    def check_password(self, raw_password):
        """Verificar contraseña"""
        if not self.password:
            return False
        return check_password(raw_password, self.password)
    
    # NUEVO: Métodos de utilidad
    def is_secretaria(self):
        return self.tipo_usuario == 'secretaria'
    
    def is_presidente(self):
        return self.tipo_usuario == 'presidente'
    
    def is_docente(self):
        return self.tipo_usuario == 'docente'
    
    def is_estudiante(self):
        return self.tipo_usuario in ['estudiante', 'egresado']
