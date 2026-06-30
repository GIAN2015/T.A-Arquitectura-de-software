from django.db import models

class Reglamento(models.Model):
    nombre = models.CharField(max_length=255)
    contenido = models.TextField()
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'reglamento'

    def __str__(self):
        return self.nombre
