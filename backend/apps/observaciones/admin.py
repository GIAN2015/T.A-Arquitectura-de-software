from django.contrib import admin
from .models import BancoObservaciones, ObservacionGenerada

@admin.register(BancoObservaciones)
class BancoObservacionesAdmin(admin.ModelAdmin):
    list_display = ['seccion', 'descripcion']

@admin.register(ObservacionGenerada)
class ObservacionGeneradaAdmin(admin.ModelAdmin):
    list_display = ['informe', 'seccion', 'observacion', 'ubicacion_error']
