from django.contrib import admin
from .models import Reglamento

@admin.register(Reglamento)
class ReglamentoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo']
    list_editable = ['activo']
