from .models import Reglamento

def obtener_reglamento() -> str:
    reglamento = Reglamento.objects.filter(activo=True).first()
    if reglamento:
        return reglamento.contenido
    return "No hay reglamento activo registrado."
