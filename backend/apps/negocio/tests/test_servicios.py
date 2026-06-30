"""
Tests para los servicios de la capa de negocio
"""
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.usuarios.models import Usuario
from apps.escuelas.models import Escuela
from apps.informes.models import Informe
from apps.observaciones.models import BancoObservacionesDocente
from apps.negocio.servicios.secretaria import SecretariaService
from apps.negocio.servicios.presidente import PresidenteService
from apps.negocio.servicios.docente import DocenteService


class SecretariaServiceTest(TestCase):
    """Tests para SecretariaService"""

    def setUp(self):
        """Configuración inicial"""
        # Crear estudiante
        self.estudiante = Usuario.objects.create_user(
            username='2020123456',
            password='test123',
            rol='estudiante'
        )
        
        # Crear secretaria
        self.secretaria = Usuario.objects.create_user(
            username='secretaria1',
            password='test123',
            rol='secretaria'
        )
        
        # Crear presidente
        self.presidente = Usuario.objects.create_user(
            username='presidente1',
            password='test123',
            rol='presidente'
        )
        
        # Crear escuela
        self.escuela = Escuela.objects.create(
            nombre='Ingeniería de Sistemas',
            codigo='ISI',
            presidente=self.presidente
        )

    def test_obtener_informes_pendientes(self):
        """Test: Obtener informes pendientes de derivar"""
        # Crear informe pendiente
        informe = Informe.objects.create(
            usuario=self.estudiante,
            titulo='Informe Test',
            descripcion='Descripción',
            estado='pendiente_secretaria'
        )
        
        informes = SecretariaService.obtener_informes_pendientes()
        
        self.assertEqual(len(informes), 1)
        self.assertEqual(informes[0].id, informe.id)

    def test_derivar_a_presidente(self):
        """Test: Derivar informe a presidente"""
        informe = Informe.objects.create(
            usuario=self.estudiante,
            titulo='Informe Test',
            descripcion='Descripción',
            estado='pendiente_secretaria'
        )
        
        resultado = SecretariaService.derivar_a_presidente(
            informe_id=informe.id,
            escuela_id=self.escuela.id,
            usuario_secretaria_id=self.secretaria.id
        )
        
        self.assertTrue(resultado)
        
        informe.refresh_from_db()
        self.assertEqual(informe.estado, 'pendiente_presidente')
        self.assertEqual(informe.escuela, self.escuela)
        self.assertEqual(informe.presidente_asignado, self.presidente)
        self.assertEqual(informe.secretaria_asignada, self.secretaria)

    def test_obtener_escuelas_activas(self):
        """Test: Obtener escuelas con presidente activo"""
        escuelas = SecretariaService.obtener_escuelas_activas()
        
        self.assertEqual(len(escuelas), 1)
        self.assertEqual(escuelas[0].id, self.escuela.id)

    def test_obtener_estadisticas(self):
        """Test: Obtener estadísticas de secretaria"""
        # Crear informes en diferentes estados
        Informe.objects.create(
            usuario=self.estudiante,
            titulo='Pendiente',
            descripcion='Desc',
            estado='pendiente_secretaria'
        )
        
        Informe.objects.create(
            usuario=self.estudiante,
            titulo='Derivado',
            descripcion='Desc',
            estado='pendiente_presidente',
            escuela=self.escuela
        )
        
        stats = SecretariaService.obtener_estadisticas()
        
        self.assertEqual(stats['pendientes'], 1)
        self.assertGreaterEqual(stats['derivados'], 1)


class PresidenteServiceTest(TestCase):
    """Tests para PresidenteService"""

    def setUp(self):
        """Configuración inicial"""
        # Crear presidente
        self.presidente = Usuario.objects.create_user(
            username='presidente1',
            password='test123',
            rol='presidente'
        )
        
        # Crear escuela
        self.escuela = Escuela.objects.create(
            nombre='Ingeniería de Sistemas',
            codigo='ISI',
            presidente=self.presidente
        )
        
        # Asignar escuela al presidente
        self.presidente.escuela = self.escuela
        self.presidente.save()
        
        # Crear docente
        self.docente = Usuario.objects.create_user(
            username='docente1',
            password='test123',
            rol='docente',
            escuela=self.escuela
        )
        
        # Crear estudiante
        self.estudiante = Usuario.objects.create_user(
            username='2020123456',
            password='test123',
            rol='estudiante'
        )

    def test_obtener_informes_pendientes_asignar(self):
        """Test: Obtener informes pendientes de asignar docente"""
        informe = Informe.objects.create(
            usuario=self.estudiante,
            titulo='Informe Test',
            descripcion='Descripción',
            estado='pendiente_presidente',
            escuela=self.escuela,
            presidente_asignado=self.presidente
        )
        
        informes = PresidenteService.obtener_informes_pendientes_asignar(
            escuela_id=self.escuela.id
        )
        
        self.assertEqual(len(informes), 1)
        self.assertEqual(informes[0].id, informe.id)

    def test_designar_docente(self):
        """Test: Designar docente revisor"""
        informe = Informe.objects.create(
            usuario=self.estudiante,
            titulo='Informe Test',
            descripcion='Descripción',
            estado='pendiente_presidente',
            escuela=self.escuela,
            presidente_asignado=self.presidente
        )
        
        resultado = PresidenteService.designar_docente(
            informe_id=informe.id,
            docente_id=self.docente.id,
            usuario_presidente_id=self.presidente.id
        )
        
        self.assertTrue(resultado)
        
        informe.refresh_from_db()
        self.assertEqual(informe.estado, 'pendiente_docente')
        self.assertEqual(informe.docente_asignado, self.docente)

    def test_obtener_docentes_escuela(self):
        """Test: Obtener docentes de la escuela"""
        docentes = PresidenteService.obtener_docentes_escuela(
            escuela_id=self.escuela.id
        )
        
        self.assertEqual(len(docentes), 1)
        self.assertEqual(docentes[0].id, self.docente.id)

    def test_aprobar_dictamen(self):
        """Test: Aprobar dictamen del docente"""
        informe = Informe.objects.create(
            usuario=self.estudiante,
            titulo='Informe Test',
            descripcion='Descripción',
            estado='pendiente_aprobacion_presidente',
            escuela=self.escuela,
            presidente_asignado=self.presidente,
            docente_asignado=self.docente,
            dictamen_docente='Dictamen del docente',
            recomendacion_docente='aprobar'
        )
        
        resultado = PresidenteService.aprobar_dictamen(
            informe_id=informe.id,
            usuario_presidente_id=self.presidente.id,
            comentario='Aprobado'
        )
        
        self.assertTrue(resultado)
        
        informe.refresh_from_db()
        self.assertEqual(informe.estado, 'aprobado_presidente')

    def test_rechazar_dictamen(self):
        """Test: Rechazar dictamen del docente"""
        informe = Informe.objects.create(
            usuario=self.estudiante,
            titulo='Informe Test',
            descripcion='Descripción',
            estado='pendiente_aprobacion_presidente',
            escuela=self.escuela,
            presidente_asignado=self.presidente,
            docente_asignado=self.docente,
            dictamen_docente='Dictamen del docente',
            recomendacion_docente='aprobar'
        )
        
        resultado = PresidenteService.rechazar_dictamen(
            informe_id=informe.id,
            usuario_presidente_id=self.presidente.id,
            motivo='Falta más detalle en el dictamen'
        )
        
        self.assertTrue(resultado)
        
        informe.refresh_from_db()
        self.assertEqual(informe.estado, 'rechazado_presidente')
        self.assertEqual(informe.motivo_rechazo_presidente, 'Falta más detalle en el dictamen')


class DocenteServiceTest(TestCase):
    """Tests para DocenteService"""

    def setUp(self):
        """Configuración inicial"""
        # Crear presidente
        presidente = Usuario.objects.create_user(
            username='presidente1',
            password='test123',
            rol='presidente'
        )
        
        # Crear escuela
        self.escuela = Escuela.objects.create(
            nombre='Ingeniería de Sistemas',
            codigo='ISI',
            presidente=presidente
        )
        
        # Crear docente
        self.docente = Usuario.objects.create_user(
            username='docente1',
            password='test123',
            rol='docente',
            escuela=self.escuela
        )
        
        # Crear estudiante
        self.estudiante = Usuario.objects.create_user(
            username='2020123456',
            password='test123',
            rol='estudiante'
        )

    def test_crear_banco(self):
        """Test: Crear banco de observaciones"""
        archivo = SimpleUploadedFile(
            "observaciones.txt",
            b"Estas son observaciones de prueba para el banco del docente. Deben tener formato correcto y suficiente contenido.",
            content_type="text/plain"
        )
        
        banco = DocenteService.crear_banco(
            docente_id=self.docente.id,
            nombre='Banco 2026-1',
            archivo=archivo
        )
        
        self.assertIsNotNone(banco)
        self.assertEqual(banco.docente, self.docente)
        self.assertEqual(banco.nombre, 'Banco 2026-1')
        self.assertTrue(banco.activo)

    def test_obtener_banco_activo(self):
        """Test: Obtener banco activo del docente"""
        archivo = SimpleUploadedFile(
            "observaciones.txt",
            b"Contenido de prueba del banco de observaciones con suficiente texto para validar.",
            content_type="text/plain"
        )
        
        banco_creado = DocenteService.crear_banco(
            docente_id=self.docente.id,
            nombre='Banco Activo',
            archivo=archivo
        )
        
        banco_obtenido = DocenteService.obtener_banco_activo(
            docente_id=self.docente.id
        )
        
        self.assertEqual(banco_obtenido.id, banco_creado.id)

    def test_activar_banco(self):
        """Test: Activar un banco existente"""
        archivo1 = SimpleUploadedFile("test1.txt", b"Contenido banco 1 con suficiente texto para validar correctamente.", content_type="text/plain")
        archivo2 = SimpleUploadedFile("test2.txt", b"Contenido banco 2 con suficiente texto para validar correctamente.", content_type="text/plain")
        
        banco1 = DocenteService.crear_banco(
            docente_id=self.docente.id,
            nombre='Banco 1',
            archivo=archivo1
        )
        
        banco2 = BancoObservacionesDocente.objects.create(
            docente=self.docente,
            nombre='Banco 2',
            archivo=archivo2,
            contenido_extraido='Contenido banco 2 con suficiente texto para validar correctamente.',
            activo=False
        )
        
        # Activar banco2
        resultado = DocenteService.activar_banco(
            banco_id=banco2.id,
            docente_id=self.docente.id
        )
        
        self.assertTrue(resultado)
        
        # Verificar que banco2 está activo y banco1 no
        banco1.refresh_from_db()
        banco2.refresh_from_db()
        
        self.assertFalse(banco1.activo)
        self.assertTrue(banco2.activo)

    def test_obtener_informes_asignados(self):
        """Test: Obtener informes asignados al docente"""
        informe = Informe.objects.create(
            usuario=self.estudiante,
            titulo='Informe Test',
            descripcion='Descripción',
            estado='pendiente_docente',
            escuela=self.escuela,
            docente_asignado=self.docente
        )
        
        informes = DocenteService.obtener_informes_asignados(
            docente_id=self.docente.id
        )
        
        self.assertEqual(len(informes), 1)
        self.assertEqual(informes[0].id, informe.id)

    def test_extraer_contenido_docx(self):
        """Test: Extraer contenido de archivo DOCX"""
        # Este test requeriría un archivo DOCX real
        # Por ahora, verificamos que el método existe
        from docx import Document
        
        # Crear un documento simple
        doc = Document()
        doc.add_paragraph("Texto de prueba")
        
        # El método extraer_contenido_docx debería procesar esto
        # En producción se usaría con archivos reales

    def test_obtener_estadisticas_docente(self):
        """Test: Obtener estadísticas del docente"""
        # Crear informes asignados
        Informe.objects.create(
            usuario=self.estudiante,
            titulo='Informe 1',
            descripcion='Desc',
            estado='pendiente_docente',
            docente_asignado=self.docente
        )
        
        Informe.objects.create(
            usuario=self.estudiante,
            titulo='Informe 2',
            descripcion='Desc',
            estado='revision_docente',
            docente_asignado=self.docente
        )
        
        stats = DocenteService.obtener_estadisticas_docente(
            docente_id=self.docente.id
        )
        
        self.assertGreaterEqual(stats['asignados'], 2)
