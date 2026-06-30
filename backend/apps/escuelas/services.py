"""
Servicio de negocio para gestión de escuelas
Capa de Negocio - Clean Architecture
"""
from apps.escuelas.models import Escuela
from apps.usuarios.models import Usuario


class EscuelaService:
    """
    Servicio para gestionar escuelas profesionales
    """
    
    @staticmethod
    def obtener_todas_activas():
        """Obtener todas las escuelas activas"""
        return Escuela.objects.filter(activo=True).select_related('presidente')
    
    @staticmethod
    def obtener_por_codigo(codigo):
        """Obtener escuela por código"""
        try:
            return Escuela.objects.get(codigo=codigo, activo=True)
        except Escuela.DoesNotExist:
            return None
    
    @staticmethod
    def asignar_presidente(escuela_id, presidente_id):
        """Asignar presidente a una escuela"""
        try:
            escuela = Escuela.objects.get(id=escuela_id)
            presidente = Usuario.objects.get(id=presidente_id, tipo_usuario='presidente')
            escuela.presidente = presidente
            escuela.save()
            return escuela
        except (Escuela.DoesNotExist, Usuario.DoesNotExist):
            return None
    
    @staticmethod
    def obtener_docentes_de_escuela(escuela_id):
        """Obtener todos los docentes de una escuela"""
        return Usuario.objects.filter(
            escuela_id=escuela_id,
            tipo_usuario='docente',
            activo=True
        )
