from django.contrib import admin
from .models import Informe

@admin.register(Informe)
class InformeAdmin(admin.ModelAdmin):
    list_display = ['nombre_archivo', 'usuario', 'estado', 'fecha_registro']
    list_filter = ['estado']
