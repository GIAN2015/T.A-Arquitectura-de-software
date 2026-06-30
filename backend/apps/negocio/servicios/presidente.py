"""
Servicio de negocio para funciones de Presidente de Escuela
Capa de Negocio - Clean Architecture
Versión 2.0
"""
from django.utils import timezone
from apps.informes.models import Informe
from apps.usuarios.models import Usuario
from apps.notificaciones.services import NotificacionService


class PresidenteService:
    """
    Lógica de negocio para operaciones de Presidente de Escuela
    Responsable de asignar docentes y aprobar/rechazar dictámenes
    """
    
    @staticmethod
    def obtener_informes_pendientes_asignar(presidente):
        """
        Obtener informes pendientes de asignar docente revisor
        
        Args:
            presidente: Usuario presidente
        
        Returns:
            QuerySet de informes pendientes
        """
        return Informe.objects.filter(
            presidente_asignado=presidente,
            estado=Informe.ESTADO_PENDIENTE_PRESIDENTE
        ).select_related('usuario', 'escuela', 'secretaria_asignada').order_by('-fecha_asignacion_presidente')
    
    @staticmethod
    def obtener_informes_en_revision(presidente):
        """
        Obtener informes que están siendo revisados por docentes de la escuela
        
        Args:
            presidente: Usuario presidente
        
        Returns:
            QuerySet de informes en revisión
        """
        return Informe.objects.filter(
            presidente_asignado=presidente,
            estado__in=[
                Informe.ESTADO_PENDIENTE_DOCENTE,
                Informe.ESTADO_VALIDANDO_IA,
                Informe.ESTADO_REVISION_DOCENTE
            ]
        ).select_related('usuario', 'docente_revisor', 'escuela').order_by('-fecha_asignacion_docente')
    
    @staticmethod
    def obtener_informes_pendientes_aprobar(presidente):
        """
        Obtener informes pendientes de aprobación del presidente
        (Docente ya completó su revisión)
        
        Args:
            presidente: Usuario presidente
        
        Returns:
            QuerySet de informes pendientes de aprobar
        """
        return Informe.objects.filter(
            presidente_asignado=presidente,
            estado=Informe.ESTADO_PENDIENTE_APROBACION_PRESIDENTE
        ).select_related('usuario', 'docente_revisor', 'escuela').order_by('-fecha_revision_docente')
    
    @staticmethod
    def obtener_informes_rechazados_por_presidente(presidente):
        """
        Obtener informes que el presidente rechazó (vuelven al docente)
        
        Args:
            presidente: Usuario presidente
        
        Returns:
            QuerySet de informes rechazados
        """
        return Informe.objects.filter(
            presidente_asignado=presidente,
            estado=Informe.ESTADO_RECHAZADO_PRESIDENTE
        ).select_related('usuario', 'docente_revisor').order_by('-fecha_aprobacion_presidente')
    
    @staticmethod
    def obtener_docentes_disponibles(presidente):
        """
        Obtener docentes de la escuela del presidente
        
        Args:
            presidente: Usuario presidente
        
        Returns:
            QuerySet de docentes disponibles
        """
        if not presidente.escuela:
            return Usuario.objects.none()
        
        return Usuario.objects.filter(
            escuela=presidente.escuela,
            tipo_usuario='docente',
            activo=True
        ).order_by('nombre')
    
    @staticmethod
    def designar_docente(informe_id, docente_id, presidente):
        """
        Designar docente revisor a un informe
        
        Args:
            informe_id: ID del informe
            docente_id: ID del docente a asignar
            presidente: Usuario presidente (para validación)
        
        Returns:
            tuple: (success: bool, informe: Informe, error: str)
        """
        try:
            informe = Informe.objects.get(
                id=informe_id,
                presidente_asignado=presidente,
                estado=Informe.ESTADO_PENDIENTE_PRESIDENTE
            )
            
            docente = Usuario.objects.get(
                id=docente_id,
                tipo_usuario='docente',
                activo=True
            )
            
            # Validar que el docente pertenece a la misma escuela
            if informe.escuela != docente.escuela:
                return False, None, f"El docente {docente.nombre} no pertenece a la escuela {informe.escuela.nombre}"
            
            # Actualizar informe
            informe.docente_revisor = docente
            informe.fecha_asignacion_docente = timezone.now()
            informe.estado = Informe.ESTADO_PENDIENTE_DOCENTE
            informe.save()
            
            # Notificar al docente
            NotificacionService.notificar_asignacion_docente(informe, docente)
            
            return True, informe, None
            
        except Informe.DoesNotExist:
            return False, None, "Informe no encontrado o no está en estado correcto"
        except Usuario.DoesNotExist:
            return False, None, "Docente no encontrado o inactivo"
        except Exception as e:
            return False, None, f"Error inesperado: {str(e)}"
    
    @staticmethod
    def aprobar_dictamen_docente(informe_id, presidente, comentario_presidente=""):
        """
        Aprobar el dictamen del docente
        
        Args:
            informe_id: ID del informe
            presidente: Usuario presidente (para validación)
            comentario_presidente: Comentario opcional del presidente
        
        Returns:
            tuple: (success: bool, informe: Informe, error: str)
        """
        try:
            informe = Informe.objects.get(
                id=informe_id,
                presidente_asignado=presidente,
                estado=Informe.ESTADO_PENDIENTE_APROBACION_PRESIDENTE
            )
            
            # Actualizar informe
            informe.comentario_presidente = comentario_presidente
            informe.fecha_aprobacion_presidente = timezone.now()
            informe.estado = Informe.ESTADO_APROBADO_PRESIDENTE
            informe.save()
            
            # Notificar a secretaria
            if informe.secretaria_asignada:
                NotificacionService.notificar_aprobacion_presidente_a_secretaria(informe)
            
            return True, informe, None
            
        except Informe.DoesNotExist:
            return False, None, "Informe no encontrado o no está en estado correcto"
        except Exception as e:
            return False, None, f"Error inesperado: {str(e)}"
    
    @staticmethod
    def rechazar_dictamen_docente(informe_id, presidente, comentario_presidente):
        """
        Rechazar el dictamen del docente (vuelve a revisión docente)
        
        Args:
            informe_id: ID del informe
            presidente: Usuario presidente (para validación)
            comentario_presidente: Motivo del rechazo (OBLIGATORIO)
        
        Returns:
            tuple: (success: bool, informe: Informe, error: str)
        """
        try:
            # Validar que haya comentario
            if not comentario_presidente or len(comentario_presidente.strip()) < 10:
                return False, None, "Debe proporcionar un motivo detallado del rechazo (mínimo 10 caracteres)"
            
            informe = Informe.objects.get(
                id=informe_id,
                presidente_asignado=presidente,
                estado=Informe.ESTADO_PENDIENTE_APROBACION_PRESIDENTE
            )
            
            # Actualizar informe
            informe.comentario_presidente = comentario_presidente
            informe.estado = Informe.ESTADO_RECHAZADO_PRESIDENTE
            informe.save()
            
            # Notificar al docente
            if informe.docente_revisor:
                NotificacionService.notificar_rechazo_presidente_a_docente(informe)
            
            return True, informe, None
            
        except Informe.DoesNotExist:
            return False, None, "Informe no encontrado o no está en estado correcto"
        except Exception as e:
            return False, None, f"Error inesperado: {str(e)}"
    
    @staticmethod
    def obtener_estadisticas(presidente):
        """
        Obtener estadísticas de los informes de la escuela del presidente
        
        Args:
            presidente: Usuario presidente
        
        Returns:
            dict con estadísticas
        """
        total_recibidos = Informe.objects.filter(presidente_asignado=presidente).count()
        
        pendientes_asignar = Informe.objects.filter(
            presidente_asignado=presidente,
            estado=Informe.ESTADO_PENDIENTE_PRESIDENTE
        ).count()
        
        en_revision = Informe.objects.filter(
            presidente_asignado=presidente,
            estado__in=[
                Informe.ESTADO_PENDIENTE_DOCENTE,
                Informe.ESTADO_VALIDANDO_IA,
                Informe.ESTADO_REVISION_DOCENTE
            ]
        ).count()
        
        pendientes_aprobar = Informe.objects.filter(
            presidente_asignado=presidente,
            estado=Informe.ESTADO_PENDIENTE_APROBACION_PRESIDENTE
        ).count()
        
        aprobados = Informe.objects.filter(
            presidente_asignado=presidente,
            estado__in=[Informe.ESTADO_APROBADO_PRESIDENTE, Informe.ESTADO_APROBADO_FINAL]
        ).count()
        
        rechazados_por_mi = Informe.objects.filter(
            presidente_asignado=presidente,
            estado=Informe.ESTADO_RECHAZADO_PRESIDENTE
        ).count()
        
        return {
            'total_recibidos': total_recibidos,
            'pendientes_asignar': pendientes_asignar,
            'en_revision': en_revision,
            'pendientes_aprobar': pendientes_aprobar,
            'aprobados': aprobados,
            'rechazados_por_mi': rechazados_por_mi,
        }
    
    @staticmethod
    def obtener_informes_por_docente(presidente):
        """
        Obtener estadísticas de informes agrupados por docente de la escuela
        Útil para dashboard del presidente
        
        Args:
            presidente: Usuario presidente
        
        Returns:
            QuerySet con agregación por docente
        """
        from django.db.models import Count
        
        return Informe.objects.filter(
            presidente_asignado=presidente,
            docente_revisor__isnull=False
        ).values(
            'docente_revisor__nombre',
            'docente_revisor__codigo'
        ).annotate(
            total_asignados=Count('id'),
            total_revisados=Count('id', filter=Q(estado__in=[
                Informe.ESTADO_PENDIENTE_APROBACION_PRESIDENTE,
                Informe.ESTADO_APROBADO_PRESIDENTE,
                Informe.ESTADO_APROBADO_FINAL
            ]))
        ).order_by('-total_asignados')


# Importar Q para el método obtener_informes_por_docente
from django.db.models import Q
