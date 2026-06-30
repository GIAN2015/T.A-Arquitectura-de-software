"""
Servicio de negocio para funciones de Docente
Capa de Negocio - Clean Architecture
Versión 2.0 - Ampliado con banco de observaciones personalizado
"""
from django.utils import timezone
from apps.informes.models import Informe
from apps.observaciones.models import BancoObservacionesDocente, ObservacionGenerada
from apps.notificaciones.services import NotificacionService
import docx
import pypdf


class DocenteService:
    """
    Lógica de negocio para operaciones de Docente
    Gestiona bancos de observaciones personalizados y revisión con IA
    """
    
    @staticmethod
    def obtener_informes_asignados(docente):
        """
        Obtener informes asignados a este docente
        
        Args:
            docente: Usuario docente
        
        Returns:
            QuerySet de informes asignados
        """
        return Informe.objects.filter(
            docente_revisor=docente,
            estado__in=[
                Informe.ESTADO_PENDIENTE_DOCENTE,
                Informe.ESTADO_VALIDANDO_IA,
                Informe.ESTADO_REVISION_DOCENTE,
                Informe.ESTADO_RECHAZADO_PRESIDENTE
            ]
        ).select_related('usuario', 'presidente_asignado', 'escuela').order_by('-fecha_asignacion_docente')
    
    @staticmethod
    def obtener_informes_revisados(docente):
        """
        Obtener informes que el docente ya revisó y envió al presidente
        
        Args:
            docente: Usuario docente
        
        Returns:
            QuerySet de informes revisados
        """
        return Informe.objects.filter(
            docente_revisor=docente,
            estado__in=[
                Informe.ESTADO_PENDIENTE_APROBACION_PRESIDENTE,
                Informe.ESTADO_APROBADO_PRESIDENTE,
                Informe.ESTADO_APROBADO_FINAL
            ]
        ).select_related('usuario', 'presidente_asignado').order_by('-fecha_revision_docente')
    
    @staticmethod
    def obtener_banco_activo(docente):
        """
        Obtener el banco de observaciones activo del docente
        
        Args:
            docente: Usuario docente
        
        Returns:
            BancoObservacionesDocente o None
        """
        return BancoObservacionesDocente.objects.filter(
            docente=docente,
            activo=True
        ).first()
    
    @staticmethod
    def obtener_todos_bancos(docente):
        """
        Obtener todos los bancos de observaciones del docente
        
        Args:
            docente: Usuario docente
        
        Returns:
            QuerySet de bancos ordenados por activo y fecha
        """
        return BancoObservacionesDocente.objects.filter(
            docente=docente
        ).order_by('-activo', '-fecha_creacion')
    
    @staticmethod
    def crear_banco_observaciones(docente, nombre, archivo):
        """
        Crear un nuevo banco de observaciones para el docente
        Extrae el contenido del archivo PDF/DOCX
        
        Args:
            docente: Usuario docente
            nombre: Nombre descriptivo del banco
            archivo: Archivo PDF o DOCX
        
        Returns:
            tuple: (success: bool, banco: BancoObservacionesDocente, error: str)
        """
        try:
            # Extraer contenido del archivo
            contenido = DocenteService._extraer_contenido_archivo(archivo)
            
            if not contenido or len(contenido.strip()) < 50:
                return False, None, "El archivo está vacío o tiene muy poco contenido (mínimo 50 caracteres)"
            
            # Crear banco (automáticamente se vuelve activo)
            banco = BancoObservacionesDocente.objects.create(
                docente=docente,
                nombre=nombre,
                archivo=archivo,
                contenido_extraido=contenido,
                activo=True
            )
            
            return True, banco, None
            
        except ValueError as e:
            return False, None, str(e)
        except Exception as e:
            return False, None, f"Error al procesar el archivo: {str(e)}"
    
    @staticmethod
    def _extraer_contenido_archivo(archivo):
        """
        Extraer texto de archivo PDF o DOCX
        
        Args:
            archivo: FileField de Django
        
        Returns:
            str: Contenido extraído
        
        Raises:
            ValueError: Si el formato no es soportado
        """
        nombre = archivo.name.lower()
        
        try:
            if nombre.endswith('.docx'):
                # Extraer de DOCX
                doc = docx.Document(archivo)
                texto = []
                for paragraph in doc.paragraphs:
                    if paragraph.text.strip():
                        texto.append(paragraph.text)
                return '\n'.join(texto)
            
            elif nombre.endswith('.pdf'):
                # Extraer de PDF
                reader = pypdf.PdfReader(archivo)
                texto = []
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text.strip():
                        texto.append(page_text)
                return '\n'.join(texto)
            
            else:
                raise ValueError("Formato no soportado. Solo se permiten archivos PDF o DOCX.")
        
        except Exception as e:
            raise ValueError(f"Error al leer el archivo: {str(e)}")
    
    @staticmethod
    def activar_banco(banco_id, docente):
        """
        Activar un banco específico (desactiva los demás del mismo docente)
        
        Args:
            banco_id: ID del banco a activar
            docente: Usuario docente propietario
        
        Returns:
            tuple: (success: bool, banco: BancoObservacionesDocente, error: str)
        """
        try:
            # Desactivar todos los bancos del docente
            BancoObservacionesDocente.objects.filter(
                docente=docente
            ).update(activo=False)
            
            # Activar el seleccionado
            banco = BancoObservacionesDocente.objects.get(
                id=banco_id,
                docente=docente
            )
            banco.activo = True
            banco.save()
            
            return True, banco, None
            
        except BancoObservacionesDocente.DoesNotExist:
            return False, None, "Banco de observaciones no encontrado"
        except Exception as e:
            return False, None, f"Error inesperado: {str(e)}"
    
    @staticmethod
    def eliminar_banco(banco_id, docente):
        """
        Eliminar un banco de observaciones
        No se puede eliminar el banco activo si es el único
        
        Args:
            banco_id: ID del banco a eliminar
            docente: Usuario docente propietario
        
        Returns:
            tuple: (success: bool, error: str)
        """
        try:
            banco = BancoObservacionesDocente.objects.get(
                id=banco_id,
                docente=docente
            )
            
            # Validar que no sea el único banco activo
            total_bancos = BancoObservacionesDocente.objects.filter(docente=docente).count()
            if banco.activo and total_bancos == 1:
                return False, "No puede eliminar su único banco de observaciones activo"
            
            banco.delete()
            return True, None
            
        except BancoObservacionesDocente.DoesNotExist:
            return False, "Banco de observaciones no encontrado"
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"
    
    @staticmethod
    def validar_informe_con_ia(informe_id, docente):
        """
        Validar informe usando IA con el banco de observaciones del docente
        
        Args:
            informe_id: ID del informe
            docente: Usuario docente
        
        Returns:
            tuple: (success: bool, observaciones: list, error: str)
        """
        try:
            informe = Informe.objects.get(
                id=informe_id,
                docente_revisor=docente,
                estado__in=[Informe.ESTADO_PENDIENTE_DOCENTE, Informe.ESTADO_RECHAZADO_PRESIDENTE]
            )
            
            # Obtener banco activo del docente
            banco = DocenteService.obtener_banco_activo(docente)
            
            if not banco:
                return False, [], "No tiene un banco de observaciones activo. Debe subir uno primero."
            
            # Actualizar estado y banco usado
            informe.banco_observaciones_usado = banco
            informe.estado = Informe.ESTADO_VALIDANDO_IA
            informe.save()
            
            # Llamar al servicio de IA (importar dinámicamente)
            try:
                from apps.observaciones.services import validar_informe_con_ia
                
                observaciones = validar_informe_con_ia(
                    contenido_informe=informe.contenido,
                    banco_observaciones=banco.contenido_extraido
                )
                
            except ImportError:
                # Si no existe el servicio de IA, usar uno básico
                observaciones = DocenteService._validacion_basica(informe.contenido, banco.contenido_extraido)
            
            # Crear observaciones generadas
            for obs_data in observaciones:
                ObservacionGenerada.objects.create(
                    informe=informe,
                    seccion=obs_data.get('seccion', 'General'),
                    observacion=obs_data.get('observacion', ''),
                    ubicacion_error=obs_data.get('ubicacion', 'No especificada'),
                    severidad=obs_data.get('severidad', ObservacionGenerada.SEVERIDAD_IMPORTANTE),
                    estado=ObservacionGenerada.ESTADO_PENDIENTE
                )
            
            # Actualizar estado a revisión
            informe.estado = Informe.ESTADO_REVISION_DOCENTE
            informe.save()
            
            return True, observaciones, None
            
        except Informe.DoesNotExist:
            return False, [], "Informe no encontrado o no está en estado correcto"
        except Exception as e:
            # Revertir estado en caso de error
            try:
                informe.estado = Informe.ESTADO_PENDIENTE_DOCENTE
                informe.save()
            except:
                pass
            return False, [], f"Error al validar con IA: {str(e)}"
    
    @staticmethod
    def _validacion_basica(contenido_informe, banco_observaciones):
        """
        Validación básica sin IA (fallback)
        Retorna formato compatible con validación de IA
        
        Args:
            contenido_informe: Texto del informe
            banco_observaciones: Texto del banco
        
        Returns:
            list de observaciones en formato estándar
        """
        return [{
            'seccion': 'Sistema',
            'observacion': 'Validación básica: El servicio de IA no está disponible. Por favor, revise manualmente.',
            'ubicacion': 'N/A',
            'severidad': ObservacionGenerada.SEVERIDAD_IMPORTANTE
        }]
    
    @staticmethod
    def enviar_dictamen_a_presidente(informe_id, docente, comentario_docente, recomendar_aprobacion=True):
        """
        Enviar dictamen final al presidente
        
        Args:
            informe_id: ID del informe
            docente: Usuario docente
            comentario_docente: Comentario/dictamen del docente
            recomendar_aprobacion: Si recomienda aprobar o no
        
        Returns:
            tuple: (success: bool, informe: Informe, error: str)
        """
        try:
            if not comentario_docente or len(comentario_docente.strip()) < 20:
                return False, None, "Debe proporcionar un dictamen detallado (mínimo 20 caracteres)"
            
            informe = Informe.objects.get(
                id=informe_id,
                docente_revisor=docente,
                estado__in=[Informe.ESTADO_REVISION_DOCENTE, Informe.ESTADO_RECHAZADO_PRESIDENTE]
            )
            
            # Actualizar informe
            informe.comentario_docente = comentario_docente
            informe.fecha_revision_docente = timezone.now()
            informe.estado = Informe.ESTADO_PENDIENTE_APROBACION_PRESIDENTE
            informe.save()
            
            # Notificar al presidente
            if informe.presidente_asignado:
                NotificacionService.notificar_revision_completa_a_presidente(informe)
            
            return True, informe, None
            
        except Informe.DoesNotExist:
            return False, None, "Informe no encontrado o no está en estado correcto"
        except Exception as e:
            return False, None, f"Error inesperado: {str(e)}"
    
    @staticmethod
    def obtener_estadisticas(docente):
        """
        Obtener estadísticas de los informes del docente
        
        Args:
            docente: Usuario docente
        
        Returns:
            dict con estadísticas
        """
        total_asignados = Informe.objects.filter(docente_revisor=docente).count()
        
        pendientes_revisar = Informe.objects.filter(
            docente_revisor=docente,
            estado__in=[Informe.ESTADO_PENDIENTE_DOCENTE, Informe.ESTADO_RECHAZADO_PRESIDENTE]
        ).count()
        
        en_revision = Informe.objects.filter(
            docente_revisor=docente,
            estado__in=[Informe.ESTADO_VALIDANDO_IA, Informe.ESTADO_REVISION_DOCENTE]
        ).count()
        
        enviados_presidente = Informe.objects.filter(
            docente_revisor=docente,
            estado__in=[
                Informe.ESTADO_PENDIENTE_APROBACION_PRESIDENTE,
                Informe.ESTADO_APROBADO_PRESIDENTE,
                Informe.ESTADO_APROBADO_FINAL
            ]
        ).count()
        
        rechazados_por_presidente = Informe.objects.filter(
            docente_revisor=docente,
            estado=Informe.ESTADO_RECHAZADO_PRESIDENTE
        ).count()
        
        total_bancos = BancoObservacionesDocente.objects.filter(docente=docente).count()
        banco_activo = DocenteService.obtener_banco_activo(docente)
        
        return {
            'total_asignados': total_asignados,
            'pendientes_revisar': pendientes_revisar,
            'en_revision': en_revision,
            'enviados_presidente': enviados_presidente,
            'rechazados_por_presidente': rechazados_por_presidente,
            'total_bancos': total_bancos,
            'tiene_banco_activo': banco_activo is not None,
            'nombre_banco_activo': banco_activo.nombre if banco_activo else None,
        }
