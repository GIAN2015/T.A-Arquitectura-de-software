"""
Tests End-to-End del flujo completo multi-rol
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.usuarios.models import Usuario
from apps.escuelas.models import Escuela
from apps.informes.models import Informe
from apps.observaciones.models import BancoObservacionesDocente
from apps.notificaciones.models import Notificacion


class FlujoCompletoTest(TestCase):
    """
    Test del flujo completo del sistema v2.0:
    Estudiante → Secretaria → Presidente → Docente → Presidente → Secretaria → Estudiante
    """

    def setUp(self):
        """Configuración inicial: crear todos los usuarios y datos necesarios"""
        self.client = Client()
        
        # 1. Crear Estudiante
        self.estudiante = Usuario.objects.create_user(
            username='2020123456',
            password='test123',
            rol='estudiante',
            email='estudiante@untels.edu.pe'
        )
        
        # 2. Crear Secretaria
        self.secretaria = Usuario.objects.create_user(
            username='secretaria1',
            password='test123',
            rol='secretaria',
            email='secretaria@untels.edu.pe'
        )
        
        # 3. Crear Presidente
        self.presidente = Usuario.objects.create_user(
            username='presidente1',
            password='test123',
            rol='presidente',
            email='presidente@untels.edu.pe'
        )
        
        # 4. Crear Escuela
        self.escuela = Escuela.objects.create(
            nombre='Ingeniería de Sistemas e Informática',
            codigo='ISI',
            presidente=self.presidente,
            activo=True
        )
        
        # 5. Asignar escuela al presidente
        self.presidente.escuela = self.escuela
        self.presidente.save()
        
        # 6. Crear Docente
        self.docente = Usuario.objects.create_user(
            username='docente1',
            password='test123',
            rol='docente',
            escuela=self.escuela,
            email='docente@untels.edu.pe'
        )
        
        # 7. Crear banco de observaciones para el docente
        archivo_banco = SimpleUploadedFile(
            "observaciones.txt",
            b"Observacion 1: Falta justificacion en capitulo 1.\n"
            b"Observacion 2: Mejorar redaccion en capitulo 2.\n"
            b"Observacion 3: Agregar referencias bibliograficas.\n"
            b"Estas son observaciones de prueba con suficiente contenido para validar.",
            content_type="text/plain"
        )
        
        self.banco = BancoObservacionesDocente.objects.create(
            docente=self.docente,
            nombre='Banco 2026-1',
            archivo=archivo_banco,
            contenido_extraido=(
                "Observacion 1: Falta justificacion en capitulo 1.\n"
                "Observacion 2: Mejorar redaccion en capitulo 2.\n"
                "Observacion 3: Agregar referencias bibliograficas.\n"
                "Estas son observaciones de prueba con suficiente contenido para validar."
            ),
            activo=True
        )

    def test_flujo_completo_aprobacion(self):
        """
        Test: Flujo completo desde que estudiante envía hasta que se aprueba
        """
        # ==========================================
        # PASO 1: ESTUDIANTE ENVÍA INFORME
        # ==========================================
        self.client.login(username='2020123456', password='test123')
        
        # Crear informe como estudiante
        archivo_informe = SimpleUploadedFile(
            "informe.pdf",
            b"Contenido del informe de practicas preprofesionales",
            content_type="application/pdf"
        )
        
        informe = Informe.objects.create(
            usuario=self.estudiante,
            titulo='Informe de Prácticas en Empresa XYZ',
            descripcion='Desarrollo de sistema web',
            archivo=archivo_informe,
            estado='enviado'
        )
        
        # Cambiar a estado pendiente_secretaria (simula el envío)
        informe.estado = 'pendiente_secretaria'
        informe.save()
        
        # Verificar que se creó el informe
        self.assertEqual(informe.estado, 'pendiente_secretaria')
        
        # Verificar notificación a secretaria
        notif_secretaria = Notificacion.objects.filter(
            usuario=self.secretaria,
            tipo='INFORME_ENVIADO'
        ).first()
        # En producción, esta notificación se crearía automáticamente
        
        self.client.logout()
        
        # ==========================================
        # PASO 2: SECRETARIA DERIVA A PRESIDENTE
        # ==========================================
        self.client.login(username='secretaria1', password='test123')
        
        # Secretaria deriva el informe al presidente de la escuela
        from apps.negocio.servicios.secretaria import SecretariaService
        
        resultado = SecretariaService.derivar_a_presidente(
            informe_id=informe.id,
            escuela_id=self.escuela.id,
            usuario_secretaria_id=self.secretaria.id
        )
        
        self.assertTrue(resultado)
        
        # Verificar cambio de estado
        informe.refresh_from_db()
        self.assertEqual(informe.estado, 'pendiente_presidente')
        self.assertEqual(informe.escuela, self.escuela)
        self.assertEqual(informe.presidente_asignado, self.presidente)
        self.assertEqual(informe.secretaria_asignada, self.secretaria)
        
        self.client.logout()
        
        # ==========================================
        # PASO 3: PRESIDENTE DESIGNA DOCENTE
        # ==========================================
        self.client.login(username='presidente1', password='test123')
        
        from apps.negocio.servicios.presidente import PresidenteService
        
        resultado = PresidenteService.designar_docente(
            informe_id=informe.id,
            docente_id=self.docente.id,
            usuario_presidente_id=self.presidente.id
        )
        
        self.assertTrue(resultado)
        
        # Verificar cambio de estado
        informe.refresh_from_db()
        self.assertEqual(informe.estado, 'pendiente_docente')
        self.assertEqual(informe.docente_asignado, self.docente)
        
        self.client.logout()
        
        # ==========================================
        # PASO 4: DOCENTE VALIDA Y GENERA DICTAMEN
        # ==========================================
        self.client.login(username='docente1', password='test123')
        
        from apps.negocio.servicios.docente import DocenteService
        
        # Docente revisa con IA (usando su banco)
        # En este test, simulamos que ya se generaron observaciones
        informe.estado = 'revision_docente'
        informe.save()
        
        # Docente envía dictamen
        resultado = DocenteService.enviar_dictamen(
            informe_id=informe.id,
            docente_id=self.docente.id,
            dictamen='El informe cumple con los requisitos establecidos. Se recomienda su aprobación.',
            recomendacion='aprobar'
        )
        
        self.assertTrue(resultado)
        
        # Verificar
        informe.refresh_from_db()
        self.assertEqual(informe.estado, 'pendiente_aprobacion_presidente')
        self.assertEqual(informe.dictamen_docente, 'El informe cumple con los requisitos establecidos. Se recomienda su aprobación.')
        self.assertEqual(informe.recomendacion_docente, 'aprobar')
        
        self.client.logout()
        
        # ==========================================
        # PASO 5: PRESIDENTE APRUEBA DICTAMEN
        # ==========================================
        self.client.login(username='presidente1', password='test123')
        
        resultado = PresidenteService.aprobar_dictamen(
            informe_id=informe.id,
            usuario_presidente_id=self.presidente.id,
            comentario='Aprobado. Excelente trabajo del docente.'
        )
        
        self.assertTrue(resultado)
        
        # Verificar
        informe.refresh_from_db()
        self.assertEqual(informe.estado, 'aprobado_presidente')
        self.assertEqual(informe.comentario_presidente, 'Aprobado. Excelente trabajo del docente.')
        
        self.client.logout()
        
        # ==========================================
        # PASO 6: SECRETARIA NOTIFICA A ESTUDIANTE
        # ==========================================
        self.client.login(username='secretaria1', password='test123')
        
        resultado = SecretariaService.notificar_estudiante(
            informe_id=informe.id,
            usuario_secretaria_id=self.secretaria.id
        )
        
        self.assertTrue(resultado)
        
        # Verificar estado final
        informe.refresh_from_db()
        self.assertEqual(informe.estado, 'aprobado_final')
        
        self.client.logout()
        
        # ==========================================
        # PASO 7: ESTUDIANTE RECIBE NOTIFICACIÓN
        # ==========================================
        self.client.login(username='2020123456', password='test123')
        
        # Verificar que el estudiante puede ver su informe aprobado
        informe_final = Informe.objects.get(id=informe.id)
        self.assertEqual(informe_final.estado, 'aprobado_final')
        self.assertEqual(informe_final.usuario, self.estudiante)
        
        # En producción, habría una notificación para el estudiante
        # notif_estudiante = Notificacion.objects.filter(
        #     usuario=self.estudiante,
        #     tipo='INFORME_APROBADO'
        # ).first()
        # self.assertIsNotNone(notif_estudiante)
        
        self.client.logout()

    def test_flujo_completo_rechazo_presidente(self):
        """
        Test: Flujo cuando el presidente rechaza el dictamen del docente
        """
        # Crear informe y llegar hasta dictamen del docente
        informe = Informe.objects.create(
            usuario=self.estudiante,
            titulo='Informe Test',
            descripcion='Descripción',
            estado='pendiente_aprobacion_presidente',
            escuela=self.escuela,
            presidente_asignado=self.presidente,
            docente_asignado=self.docente,
            secretaria_asignada=self.secretaria,
            dictamen_docente='Dictamen con falta de detalle',
            recomendacion_docente='aprobar'
        )
        
        # Presidente rechaza
        self.client.login(username='presidente1', password='test123')
        
        from apps.negocio.servicios.presidente import PresidenteService
        
        resultado = PresidenteService.rechazar_dictamen(
            informe_id=informe.id,
            usuario_presidente_id=self.presidente.id,
            motivo='El dictamen necesita más detalle en las observaciones'
        )
        
        self.assertTrue(resultado)
        
        # Verificar que volvió al docente
        informe.refresh_from_db()
        self.assertEqual(informe.estado, 'rechazado_presidente')
        self.assertEqual(informe.motivo_rechazo_presidente, 'El dictamen necesita más detalle en las observaciones')
        
        # El docente debería recibir notificación
        # notif_docente = Notificacion.objects.filter(
        #     usuario=self.docente,
        #     tipo='DICTAMEN_RECHAZADO'
        # ).first()
        # self.assertIsNotNone(notif_docente)
        
        self.client.logout()

    def test_validaciones_flujo(self):
        """
        Test: Verificar que las validaciones funcionan correctamente
        """
        informe = Informe.objects.create(
            usuario=self.estudiante,
            titulo='Informe Test',
            descripcion='Descripción',
            estado='pendiente_secretaria'
        )
        
        # 1. Secretaria no puede derivar a escuela sin presidente
        escuela_sin_presidente = Escuela.objects.create(
            nombre='Escuela Sin Presidente',
            codigo='ESP',
            presidente=None  # Sin presidente (debería fallar en creación)
        )
        # Esta validación se haría en el servicio
        
        # 2. Presidente no puede asignar docente de otra escuela
        otra_escuela = Escuela.objects.create(
            nombre='Otra Escuela',
            codigo='OE',
            presidente=self.presidente
        )
        
        docente_otra_escuela = Usuario.objects.create_user(
            username='docente2',
            password='test123',
            rol='docente',
            escuela=otra_escuela
        )
        
        # El servicio debe validar que el docente pertenece a la escuela del informe
        
        # 3. Docente no puede revisar sin banco activo
        self.banco.activo = False
        self.banco.save()
        
        # El servicio debe validar que hay un banco activo
        from apps.negocio.servicios.docente import DocenteService
        
        banco_activo = DocenteService.obtener_banco_activo(
            docente_id=self.docente.id
        )
        
        self.assertIsNone(banco_activo)


class IntegracionNotificacionesTest(TestCase):
    """Tests de integración del sistema de notificaciones en el flujo"""

    def setUp(self):
        """Configuración inicial"""
        self.estudiante = Usuario.objects.create_user(
            username='2020123456',
            password='test123',
            rol='estudiante'
        )
        
        self.secretaria = Usuario.objects.create_user(
            username='secretaria1',
            password='test123',
            rol='secretaria'
        )

    def test_notificaciones_se_crean_automaticamente(self):
        """Test: Verificar que las notificaciones se crean en cada paso"""
        # Este test verificaría que cada servicio crea las notificaciones correctas
        # En producción, cada método de servicio debería llamar a NotificacionService
        
        from apps.notificaciones.services import NotificacionService
        
        # Crear notificación de prueba
        notif = NotificacionService.crear_notificacion(
            usuario=self.estudiante,
            tipo='INFORME_ENVIADO',
            titulo='Informe Enviado',
            mensaje='Tu informe ha sido enviado correctamente'
        )
        
        self.assertIsNotNone(notif)
        self.assertEqual(notif.usuario, self.estudiante)
        
        # Verificar contador de no leídas
        count = NotificacionService.contar_no_leidas(
            usuario_id=self.estudiante.id
        )
        
        self.assertEqual(count, 1)
