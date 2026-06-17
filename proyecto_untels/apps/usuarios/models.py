from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Usuario(models.Model):
    TIPO_CHOICES = [
        ('estudiante', 'Estudiante'),
        ('egresado', 'Egresado'),
        ('docente', 'Docente'),
    ]
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=200)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_CHOICES, default='estudiante')
    password = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()
    
    def check_password(self, raw_password):
        if not self.password:
            return False
        return check_password(raw_password, self.password)
