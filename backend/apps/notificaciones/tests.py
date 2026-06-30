"""
Tests para el modelo Notificacion y NotificacionService
"""
from django.test import TestCase
from django.utils import timezone
from apps.usuarios.models import Usuario
from apps.escuelas.models import Escuela
from apps.informes.models import Informe
from apps.notificaciones.models import Notificacion
from apps.notificaciones.services import NotificacionService


class NotificacionModelTest(TestCase):
    """Tests para el modelo Notificacion"""

    def setUp(self):
        """Configuración inicial"""
        # Crear usuarios
        self.estudiante = Usuario.objects.create_user(
            username='2020123456',
            password='test123',
            rol='estudiante',
            email='estudiante@untels.edu.pe'
        )
        
        self.secretaria = Usuario.objects.create_user(
            username='secretaria1',
            password='test123',
            rol='secretaria',
            email='secretaria@untels.edu.pe'
        )

    def test_crear_notificacion(self):
        """Test: Crear una notificación"""
        notificacion = Notificacion.objects.create(
            usuario=self.estudiante,
            tipo='INFORME_APROBADO',
            titulo='Tu informe ha sido aprobado',
            mensaje='El informe ha sido aprobado por el presidente de escuela',
            leida=False
        )
        
        self.assertEqual(notificacion.usuario, self.estudiante)
        self.assertEqual(notificacion.tipo, 'INFORME_APROBADO')
        self.assertFalse(notificacion.leida)
        self.assertIsNotNone(notificacion.fecha_creacion)

    def test_notificacion_str(self):
        """Test: String representation de notificación"""
        notificacion = Notificacion.objects.create(
            usuario=self.estudiante,
            tipo='INFORME_ENVIADO',
            titulo='Informe enviado',
            mensaje='Tu informe ha sido enviado correctamente'
        )
        
        expected = f"Notificación para {self.estudiante.username}: Informe enviado"
        self.assertEqual(str(notificacion), expected)

    def test_marcar_como_leida(self):
        """Test: Marcar notificación como leída"""
        notificacion = Notificacion.objects.create(
            usuario=self.estudiante,
            tipo='INFORME_APROBADO',
            titulo='Aprobado',
            mensaje='Tu informe fue aprobado',
            leida=False
        )
        
        # Marcar como leída
        notificacion.leida = True
        notificacion.fecha_lectura = timezone.now()
        notificacion.save()
        
        notificacion.refresh_from_db()
        self.assertTrue(notificacion.leida)
        self.assertIsNotNone(notificacion.fecha_lectura)

    def test_notificacion_con_informe(self):
        """Test: Notificación relacionada a un informe"""
        # Crear presidente y escuela para el informe
        presidente = Usuario.objects.create_user(
            username='presidente1',
            password='test123',
            rol='presidente'
        )
        
        escuela = Escuela.objects.create(
            nombre='Ingeniería de Sistemas',
            codigo='ISI',
            presidente=presidente
        )
        
        # Crear informe
        informe = Informe.objects.create(
            usuario=self.estudiante,
            titulo='Informe de Prácticas',
            descripcion='Descripción del informe',
            estado='enviado'
        )
        
        # Crear notificación relacionada al informe
        notificacion = Notificacion.objects.create(
            usuario=self.secretaria,
            tipo='INFORME_ENVIADO',
            titulo='Nuevo informe recibido',
            mensaje=f'El estudiante {self.estudiante.username} envió un informe',
            informe=informe
        )
        
        self.assertEqual(notificacion.informe, informe)

    def test_obtener_notificaciones_no_leidas(self):
        """Test: Obtener notificaciones no leídas de un usuario"""
        # Crear notificaciones
        Notificacion.objects.create(
            usuario=self.estudiante,
            tipo='INFORME_APROBADO',
            titulo='Aprobado',
            mensaje='Tu informe fue aprobado',
            leida=False
        )
        
        Notificacion.objects.create(
            usuario=self.estudiante,
            tipo='INFORME_RECHAZADO',
            titulo='Rechazado',
            mensaje='Tu informe fue rechazado',
            leida=False
        )
        
        Notificacion.objects.create(
            usuario=self.estudiante,
            tipo='INFORME_ENVIADO',
            titulo='Enviado',
            mensaje='Tu informe fue enviado',
            leida=True
        )
        
        # Obtener no leídas
        no_leidas = Notificacion.objects.filter(
            usuario=self.estudiante,
            leida=False
        )
        
        self.assertEqual(no_leidas.count(), 2)

    def test_contar_no_leidas(self):
        """Test: Contar notificaciones no leídas"""
        Notificacion.objects.create(
            usuario=self.estudiante,
            tipo='INFORME_APROBADO',
            titulo='Aprobado',
            mensaje='Aprobado',
            leida=False
        )
        
        Notificacion.objects.create(
            usuario=self.estudiante,
            tipo='INFORME_RECHAZADO',
            titulo='Rechazado',
            mensaje='Rechazado',
            leida=True
        )
        
        count = Notificacion.objects.filter(
            usuario=self.estudiante,
            leida=False
        ).count()
        
        self.assertEqual(count, 1)

    def test_ordenar_notificaciones_por_fecha(self):
        """Test: Las notificaciones se ordenan por fecha de creación"""
        notif1 = Notificacion.objects.create(
            usuario=self.estudiante,
            tipo='INFORME_ENVIADO',
            titulo='Primera',
            mensaje='Primera notificación'
        )
        
        notif2 = Notificacion.objects.create(
            usuario=self.estudiante,
            tipo='INFORME_APROBADO',
            titulo='Segunda',
            mensaje='Segunda notificación'
        )
        
        notificaciones = Notificacion.objects.filter(
            usuario=self.estudiante
        ).order_by('-fecha_creacion')
        
        # La más reciente debe ser la segunda
        self.assertEqual(notificaciones.first(), notif2)
        self.assertEqual(notificaciones.last(), notif1)


class NotificacionServiceTest(TestCase):
    """Tests para NotificacionService"""

    def setUp(self):
        """Configuración inicial"""
        self.estudiante = Usuario.objects.create_user(
            username='2020123456',
            password='test123',
            rol='estudiante',
            email='estudiante@untels.edu.pe'
        )
        
        self.secretaria = Usuario.objects.create_user(
            username='secretaria1',
            password='test123',
            rol='secretaria',
            email='secretaria@untels.edu.pe'
        )

    def test_crear_notificacion_generica(self):
        """Test: Crear notificación genérica con el servicio"""
        notificacion = NotificacionService.crear_notificacion(
            usuario=self.estudiante,
            tipo='INFORME_APROBADO',
            titulo='Informe Aprobado',
            mensaje='Tu informe ha sido aprobado'
        )
        
        self.assertIsNotNone(notificacion)
        self.assertEqual(notificacion.usuario, self.estudiante)
        self.assertEqual(notificacion.tipo, 'INFORME_APROBADO')

    def test_obtener_notificaciones_usuario(self):
        """Test: Obtener notificaciones de un usuario"""
        NotificacionService.crear_notificacion(
            usuario=self.estudiante,
            tipo='INFORME_ENVIADO',
            titulo='Enviado',
            mensaje='Tu informe fue enviado'
        )
        
        NotificacionService.crear_notificacion(
            usuario=self.estudiante,
            tipo='INFORME_APROBADO',
            titulo='Aprobado',
            mensaje='Tu informe fue aprobado'
        )
        
        notificaciones = NotificacionService.obtener_notificaciones_usuario(
            usuario_id=self.estudiante.id
        )
        
        self.assertEqual(len(notificaciones), 2)

    def test_obtener_solo_no_leidas(self):
        """Test: Obtener solo notificaciones no leídas"""
        notif1 = NotificacionService.crear_notificacion(
            usuario=self.estudiante,
            tipo='INFORME_ENVIADO',
            titulo='Enviado',
            mensaje='Enviado'
        )
        
        notif2 = NotificacionService.crear_notificacion(
            usuario=self.estudiante,
            tipo='INFORME_APROBADO',
            titulo='Aprobado',
            mensaje='Aprobado'
        )
        
        # Marcar una como leída
        notif1.leida = True
        notif1.save()
        
        no_leidas = NotificacionService.obtener_notificaciones_usuario(
            usuario_id=self.estudiante.id,
            solo_no_leidas=True
        )
        
        self.assertEqual(len(no_leidas), 1)
        self.assertEqual(no_leidas[0].id, notif2.id)

    def test_contar_no_leidas_service(self):
        """Test: Contar no leídas con el servicio"""
        NotificacionService.crear_notificacion(
            usuario=self.estudiante,
            tipo='INFORME_ENVIADO',
            titulo='Enviado',
            mensaje='Enviado'
        )
        
        NotificacionService.crear_notificacion(
            usuario=self.estudiante,
            tipo='INFORME_APROBADO',
            titulo='Aprobado',
            mensaje='Aprobado'
        )
        
        count = NotificacionService.contar_no_leidas(
            usuario_id=self.estudiante.id
        )
        
        self.assertEqual(count, 2)

    def test_marcar_como_leida_service(self):
        """Test: Marcar notificación como leída con el servicio"""
        notif = NotificacionService.crear_notificacion(
            usuario=self.estudiante,
            tipo='INFORME_ENVIADO',
            titulo='Enviado',
            mensaje='Enviado'
        )
        
        # Marcar como leída
        resultado = NotificacionService.marcar_como_leida(
            notificacion_id=notif.id
        )
        
        self.assertTrue(resultado)
        
        notif.refresh_from_db()
        self.assertTrue(notif.leida)
        self.assertIsNotNone(notif.fecha_lectura)

    def test_obtener_tipos_notificacion(self):
        """Test: Obtener todos los tipos de notificación"""
        tipos = NotificacionService.obtener_tipos_notificacion()
        
        self.assertIsInstance(tipos, list)
        self.assertIn('INFORME_ENVIADO', tipos)
        self.assertIn('INFORME_APROBADO', tipos)
        self.assertIn('INFORME_RECHAZADO', tipos)
        self.assertIn('INFORME_DERIVADO', tipos)
        self.assertIn('DOCENTE_ASIGNADO', tipos)
        self.assertIn('DICTAMEN_ENVIADO', tipos)
        self.assertIn('DICTAMEN_APROBADO', tipos)
        self.assertIn('DICTAMEN_RECHAZADO', tipos)
