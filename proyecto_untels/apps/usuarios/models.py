from django.db import models

class Usuario(models.Model):
    TIPO_CHOICES = [('estudiante', 'Estudiante'), ('egresado', 'Egresado')]
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=200)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_CHOICES, default='estudiante')

    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
