from django.db import models
from apps.usuarios.models import Usuario

class Informe(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre_archivo = models.CharField(max_length=255)
    contenido = models.TextField()
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'informe'

    def __str__(self):
        return self.nombre_archivo
