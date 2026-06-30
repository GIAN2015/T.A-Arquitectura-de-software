from django.contrib import admin
from .models import Escuela


@admin.register(Escuela)
class EscuelaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'presidente', 'activo']
    list_filter = ['activo']
    search_fields = ['codigo', 'nombre']
