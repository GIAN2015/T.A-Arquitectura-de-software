"""
Servicio de negocio para funciones de Secretaria
Capa de Negocio - Clean Architecture
Versión 2.0
"""
from django.utils import timezone
from apps.informes.models import Informe
from apps.escuelas.models import Escuela
from apps.notificaciones.services import NotificacionService


class SecretariaService:
    """
    Lógica de negocio para operaciones de Secretaria Académica
    Responsable de recibir informes y derivar a presidentes de escuela
    """
    
    @staticmethod
    def obtener_informes_pendientes():
        """
        Obtener informes pendientes de derivar a presidente
        
        Returns:
            QuerySet de informes en estado PENDIENTE_SECRETARIA
        """
        return Informe.objects.filter(
            estado=Informe.ESTADO_PENDIENTE_SECRETARIA
        ).select_related('usuario', 'escuela').order_by('-fecha_registro')
    
    @staticmethod
    def obtener_informes_recibidos():
        """
        Obtener todos los informes recibidos (recién enviados por estudiantes)
        Incluye ESTADO_ENVIADO que aún no han sido procesados
        
        Returns:
            QuerySet de informes enviados
        """
        return Informe.objects.filter(
            estado__in=[Informe.ESTADO_ENVIADO, Informe.ESTADO_PENDIENTE_SECRETARIA]
        ).select_related('usuario').order_by('-fecha_registro')
    
    @staticmethod
    def derivar_a_presidente(informe_id, escuela_id, secretaria, comentario_secretaria=""):
        """
        Derivar informe a presidente de escuela
        
        Args:
            informe_id: ID del informe
            escuela_id: ID de la escuela a la que derivar
            secretaria: Usuario secretaria que deriva
            comentario_secretaria: Comentario opcional de la secretaria
        
        Returns:
            tuple: (success: bool, informe: Informe, error: str)
        """
        try:
            informe = Informe.objects.get(id=informe_id)
            escuela = Escuela.objects.get(id=escuela_id, activo=True)
            
            # Validar que la escuela tenga presidente asignado
            if not escuela.presidente:
                return False, None, f"La escuela {escuela.nombre} no tiene presidente asignado"
            
            # Validar estado del informe
            if informe.estado not in [Informe.ESTADO_ENVIADO, Informe.ESTADO_PENDIENTE_SECRETARIA]:
                return False, None, f"El informe está en estado {informe.get_estado_display()}, no se puede derivar"
            
            # Actualizar informe
            informe.secretaria_asignada = secretaria
            informe.escuela = escuela
            informe.presidente_asignado = escuela.presidente
            informe.comentario_secretaria = comentario_secretaria
            informe.fecha_asignacion_secretaria = timezone.now()
            informe.estado = Informe.ESTADO_PENDIENTE_PRESIDENTE
            informe.save()
            
            # Notificar al presidente
            NotificacionService.notificar_asignacion_presidente(
                informe, 
                escuela.presidente
            )
            
            return True, informe, None
            
        except Informe.DoesNotExist:
            return False, None, "Informe no encontrado"
        except Escuela.DoesNotExist:
            return False, None, "Escuela no encontrada o inactiva"
        except Exception as e:
            return False, None, f"Error inesperado: {str(e)}"
    
    @staticmethod
    def obtener_informes_enviados(secretaria):
        """
        Obtener informes que esta secretaria derivó a presidentes
        
        Args:
            secretaria: Usuario secretaria
        
        Returns:
            QuerySet de informes derivados
        """
        return Informe.objects.filter(
            secretaria_asignada=secretaria
        ).exclude(
            estado__in=[Informe.ESTADO_ENVIADO, Informe.ESTADO_PENDIENTE_SECRETARIA]
        ).select_related('usuario', 'escuela', 'presidente_asignado').order_by('-fecha_asignacion_secretaria')
    
    @staticmethod
    def obtener_informes_en_proceso(secretaria):
        """
        Obtener informes que están en proceso (derivados pero no completados)
        
        Args:
            secretaria: Usuario secretaria
        
        Returns:
            QuerySet de informes en proceso
        """
        return Informe.objects.filter(
            secretaria_asignada=secretaria,
            estado__in=[
                Informe.ESTADO_PENDIENTE_PRESIDENTE,
                Informe.ESTADO_PENDIENTE_DOCENTE,
                Informe.ESTADO_VALIDANDO_IA,
                Informe.ESTADO_REVISION_DOCENTE,
                Informe.ESTADO_PENDIENTE_APROBACION_PRESIDENTE,
                Informe.ESTADO_RECHAZADO_PRESIDENTE,
            ]
        ).select_related('usuario', 'escuela', 'presidente_asignado', 'docente_revisor').order_by('-fecha_asignacion_secretaria')
    
    @staticmethod
    def obtener_informes_aprobados_pendientes_notificar(secretaria):
        """
        Obtener informes aprobados por presidente pendientes de notificar al estudiante
        
        Args:
            secretaria: Usuario secretaria
        
        Returns:
            QuerySet de informes aprobados pendientes
        """
        return Informe.objects.filter(
            secretaria_asignada=secretaria,
            estado=Informe.ESTADO_APROBADO_PRESIDENTE
        ).select_related('usuario', 'presidente_asignado', 'docente_revisor').order_by('-fecha_aprobacion_presidente')
    
    @staticmethod
    def notificar_estudiante_aprobado(informe_id, secretaria):
        """
        Notificar a estudiante que su informe fue aprobado (paso final)
        
        Args:
            informe_id: ID del informe
            secretaria: Usuario secretaria (para validación)
        
        Returns:
            tuple: (success: bool, informe: Informe, error: str)
        """
        try:
            informe = Informe.objects.get(
                id=informe_id,
                secretaria_asignada=secretaria,
                estado=Informe.ESTADO_APROBADO_PRESIDENTE
            )
            
            # Actualizar estado final
            informe.estado = Informe.ESTADO_APROBADO_FINAL
            informe.fecha_completado = timezone.now()
            informe.save()
            
            # Notificar al estudiante
            NotificacionService.notificar_aprobacion_final_a_estudiante(informe)
            
            return True, informe, None
            
        except Informe.DoesNotExist:
            return False, None, "Informe no encontrado o no está en estado correcto"
        except Exception as e:
            return False, None, f"Error inesperado: {str(e)}"
    
    @staticmethod
    def obtener_estadisticas(secretaria):
        """
        Obtener estadísticas de los informes gestionados por la secretaria
        
        Args:
            secretaria: Usuario secretaria
        
        Returns:
            dict con estadísticas
        """
        total_gestionados = Informe.objects.filter(secretaria_asignada=secretaria).count()
        
        pendientes_derivar = Informe.objects.filter(
            estado=Informe.ESTADO_PENDIENTE_SECRETARIA
        ).count()
        
        en_proceso = Informe.objects.filter(
            secretaria_asignada=secretaria,
            estado__in=[
                Informe.ESTADO_PENDIENTE_PRESIDENTE,
                Informe.ESTADO_PENDIENTE_DOCENTE,
                Informe.ESTADO_VALIDANDO_IA,
                Informe.ESTADO_REVISION_DOCENTE,
                Informe.ESTADO_PENDIENTE_APROBACION_PRESIDENTE,
            ]
        ).count()
        
        pendientes_notificar = Informe.objects.filter(
            secretaria_asignada=secretaria,
            estado=Informe.ESTADO_APROBADO_PRESIDENTE
        ).count()
        
        completados = Informe.objects.filter(
            secretaria_asignada=secretaria,
            estado=Informe.ESTADO_APROBADO_FINAL
        ).count()
        
        return {
            'total_gestionados': total_gestionados,
            'pendientes_derivar': pendientes_derivar,
            'en_proceso': en_proceso,
            'pendientes_notificar': pendientes_notificar,
            'completados': completados,
        }
