"""
Servicio de notificaciones
Capa de Negocio - Clean Architecture
Versión 2.0
"""
from apps.notificaciones.models import Notificacion
from apps.usuarios.models import Usuario
from apps.informes.models import Informe


class NotificacionService:
    """
    Servicio para gestionar notificaciones del sistema
    Responsable de crear y gestionar notificaciones para todos los roles
    """
    
    @staticmethod
    def crear_notificacion(usuario, informe, tipo, titulo, mensaje):
        """
        Crear una nueva notificación
        
        Args:
            usuario: Usuario que recibe la notificación
            informe: Informe relacionado
            tipo: Tipo de notificación (ver Notificacion.TIPO_CHOICES)
            titulo: Título de la notificación
            mensaje: Mensaje completo
        
        Returns:
            Notificacion creada
        """
        return Notificacion.objects.create(
            usuario=usuario,
            informe=informe,
            tipo=tipo,
            titulo=titulo,
            mensaje=mensaje
        )
    
    @staticmethod
    def notificar_nuevo_informe_a_secretaria(informe):
        """
        Notificar a secretaria cuando estudiante envía informe
        
        Args:
            informe: Informe recién creado
        
        Returns:
            Notificacion o None si no hay secretaria
        """
        # Obtener secretaria activa (puede ser sistema de rotación o asignación)
        secretaria = Usuario.objects.filter(
            tipo_usuario='secretaria',
            activo=True
        ).first()
        
        if not secretaria:
            return None
        
        return NotificacionService.crear_notificacion(
            usuario=secretaria,
            informe=informe,
            tipo='nuevo_informe',
            titulo='Nuevo Informe Recibido',
            mensaje=f'El estudiante {informe.usuario.nombre} ({informe.usuario.codigo}) '
                    f'ha enviado el informe "{informe.nombre_archivo}". '
                    f'Debe ser derivado a la escuela correspondiente.'
        )
    
    @staticmethod
    def notificar_asignacion_presidente(informe, presidente):
        """
        Notificar a presidente cuando secretaria deriva informe
        
        Args:
            informe: Informe derivado
            presidente: Usuario presidente que recibe
        
        Returns:
            Notificacion creada
        """
        return NotificacionService.crear_notificacion(
            usuario=presidente,
            informe=informe,
            tipo='asignado_presidente',
            titulo='Informe Asignado a su Escuela',
            mensaje=f'Se le ha asignado el informe "{informe.nombre_archivo}" '
                    f'del estudiante {informe.usuario.nombre} ({informe.usuario.codigo}). '
                    f'Debe designar un docente revisor de su escuela.'
        )
    
    @staticmethod
    def notificar_asignacion_docente(informe, docente):
        """
        Notificar a docente cuando presidente le asigna informe
        
        Args:
            informe: Informe asignado
            docente: Usuario docente que recibe
        
        Returns:
            Notificacion creada
        """
        return NotificacionService.crear_notificacion(
            usuario=docente,
            informe=informe,
            tipo='asignado_docente',
            titulo='Informe Asignado para Revisión',
            mensaje=f'El presidente {informe.presidente_asignado.nombre} le ha asignado '
                    f'el informe "{informe.nombre_archivo}" del estudiante {informe.usuario.nombre}. '
                    f'Debe revisar el informe utilizando su banco de observaciones.'
        )
    
    @staticmethod
    def notificar_revision_completa_a_presidente(informe):
        """
        Notificar a presidente cuando docente completa revisión
        
        Args:
            informe: Informe revisado
        
        Returns:
            Notificacion creada
        """
        return NotificacionService.crear_notificacion(
            usuario=informe.presidente_asignado,
            informe=informe,
            tipo='revision_completa',
            titulo='Revisión de Docente Completada',
            mensaje=f'El docente {informe.docente_revisor.nombre} ha completado '
                    f'la revisión del informe "{informe.nombre_archivo}". '
                    f'Debe revisar el dictamen y aprobar o rechazar.'
        )
    
    @staticmethod
    def notificar_aprobacion_presidente_a_secretaria(informe):
        """
        Notificar a secretaria cuando presidente aprueba
        
        Args:
            informe: Informe aprobado por presidente
        
        Returns:
            Notificacion creada
        """
        return NotificacionService.crear_notificacion(
            usuario=informe.secretaria_asignada,
            informe=informe,
            tipo='aprobado_presidente',
            titulo='Informe Aprobado por Presidente',
            mensaje=f'El presidente {informe.presidente_asignado.nombre} ha aprobado '
                    f'el informe "{informe.nombre_archivo}" del estudiante {informe.usuario.nombre}. '
                    f'Debe notificar al estudiante del resultado final.'
        )
    
    @staticmethod
    def notificar_rechazo_presidente_a_docente(informe):
        """
        Notificar a docente cuando presidente rechaza su dictamen
        
        Args:
            informe: Informe rechazado por presidente
        
        Returns:
            Notificacion creada
        """
        return NotificacionService.crear_notificacion(
            usuario=informe.docente_revisor,
            informe=informe,
            tipo='rechazado_presidente',
            titulo='Dictamen Rechazado por Presidente',
            mensaje=f'El presidente {informe.presidente_asignado.nombre} ha rechazado '
                    f'su dictamen del informe "{informe.nombre_archivo}". '
                    f'Motivo: {informe.comentario_presidente or "No especificado"}. '
                    f'Debe revisar nuevamente el informe.'
        )
    
    @staticmethod
    def notificar_aprobacion_final_a_estudiante(informe):
        """
        Notificar a estudiante cuando su informe es aprobado
        
        Args:
            informe: Informe aprobado final
        
        Returns:
            Notificacion creada
        """
        return NotificacionService.crear_notificacion(
            usuario=informe.usuario,
            informe=informe,
            tipo='aprobado_final',
            titulo='¡Informe APROBADO!',
            mensaje=f'¡Felicitaciones! Su informe "{informe.nombre_archivo}" '
                    f'ha sido APROBADO por la escuela de {informe.escuela.nombre}. '
                    f'El proceso de validación ha concluido exitosamente.'
        )
    
    @staticmethod
    def notificar_rechazo_a_estudiante(informe):
        """
        Notificar a estudiante cuando su informe es rechazado
        
        Args:
            informe: Informe rechazado
        
        Returns:
            Notificacion creada
        """
        return NotificacionService.crear_notificacion(
            usuario=informe.usuario,
            informe=informe,
            tipo='rechazado_estudiante',
            titulo='Informe Rechazado - Requiere Correcciones',
            mensaje=f'Su informe "{informe.nombre_archivo}" requiere correcciones. '
                    f'Por favor revise las observaciones del docente {informe.docente_revisor.nombre} '
                    f'y vuelva a enviar el informe corregido. '
                    f'Comentario: {informe.comentario_docente or "Ver observaciones en el sistema"}'
        )
    
    @staticmethod
    def notificar_rechazo_final_a_estudiante(informe):
        """
        Notificar a estudiante cuando su informe es rechazado por el presidente
        (después de que el docente lo había aprobado)
        
        Args:
            informe: Informe rechazado por presidente
        
        Returns:
            Notificacion creada
        """
        motivo = informe.comentario_presidente or "No se especificó motivo"
        
        return NotificacionService.crear_notificacion(
            usuario=informe.usuario,
            informe=informe,
            tipo='rechazado_estudiante',
            titulo='Informe Rechazado por Presidente - Requiere Correcciones',
            mensaje=f'Su informe "{informe.nombre_archivo}" fue revisado por el docente '
                    f'{informe.docente_revisor.nombre}, pero el Presidente de Escuela '
                    f'{informe.presidente_asignado.nombre} solicitó correcciones adicionales. '
                    f'Motivo del rechazo: {motivo}. '
                    f'Por favor corrija su informe y envíelo nuevamente.'
        )
    
    @staticmethod
    def obtener_no_leidas(usuario):
        """
        Obtener notificaciones no leídas de un usuario
        
        Args:
            usuario: Usuario
        
        Returns:
            QuerySet de notificaciones no leídas
        """
        return Notificacion.objects.filter(
            usuario=usuario,
            leida=False
        ).select_related('informe', 'informe__usuario').order_by('-fecha_creacion')
    
    @staticmethod
    def obtener_todas(usuario, limit=50):
        """
        Obtener todas las notificaciones de un usuario
        
        Args:
            usuario: Usuario
            limit: Límite de notificaciones a retornar
        
        Returns:
            QuerySet de notificaciones
        """
        return Notificacion.objects.filter(
            usuario=usuario
        ).select_related('informe', 'informe__usuario').order_by('-fecha_creacion')[:limit]
    
    @staticmethod
    def contar_no_leidas(usuario):
        """
        Contar notificaciones no leídas de un usuario
        
        Args:
            usuario: Usuario
        
        Returns:
            int: Cantidad de notificaciones no leídas
        """
        return Notificacion.objects.filter(
            usuario=usuario,
            leida=False
        ).count()
    
    @staticmethod
    def marcar_como_leida(notificacion_id, usuario):
        """
        Marcar una notificación como leída
        
        Args:
            notificacion_id: ID de la notificación
            usuario: Usuario (para validación)
        
        Returns:
            tuple: (success: bool, notificacion: Notificacion, error: str)
        """
        try:
            notificacion = Notificacion.objects.get(id=notificacion_id, usuario=usuario)
            notificacion.marcar_como_leida()
            return True, notificacion, None
        except Notificacion.DoesNotExist:
            return False, None, "Notificación no encontrada"
    
    @staticmethod
    def marcar_todas_como_leidas(usuario):
        """
        Marcar todas las notificaciones de un usuario como leídas
        
        Args:
            usuario: Usuario
        
        Returns:
            int: Cantidad de notificaciones marcadas
        """
        from django.utils import timezone
        cantidad = Notificacion.objects.filter(
            usuario=usuario,
            leida=False
        ).update(
            leida=True,
            fecha_leida=timezone.now()
        )
        return cantidad
