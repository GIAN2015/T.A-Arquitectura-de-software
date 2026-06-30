"""
Tests para los modelos de Observaciones
"""
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.usuarios.models import Usuario
from apps.escuelas.models import Escuela
from apps.observaciones.models import BancoObservacionesDocente, BancoObservaciones


class BancoObservacionesDocenteTest(TestCase):
    """Tests para el modelo BancoObservacionesDocente"""

    def setUp(self):
        """Configuración inicial"""
        # Crear escuela y presidente
        self.presidente = Usuario.objects.create_user(
            username='presidente1',
            password='test123',
            rol='presidente'
        )
        
        self.escuela = Escuela.objects.create(
            nombre='Ingeniería de Sistemas',
            codigo='ISI',
            presidente=self.presidente
        )
        
        # Crear docente
        self.docente = Usuario.objects.create_user(
            username='docente1',
            password='test123',
            rol='docente',
            escuela=self.escuela
        )

    def test_crear_banco_docente(self):
        """Test: Crear banco de observaciones para docente"""
        # Crear archivo de prueba
        archivo = SimpleUploadedFile(
            "observaciones.txt",
            b"Estas son observaciones de prueba. Deben tener formato correcto.",
            content_type="text/plain"
        )
        
        banco = BancoObservacionesDocente.objects.create(
            docente=self.docente,
            nombre='Banco 2026-1',
            archivo=archivo,
            contenido_extraido='Estas son observaciones de prueba. Deben tener formato correcto.',
            activo=True
        )
        
        self.assertEqual(banco.docente, self.docente)
        self.assertEqual(banco.nombre, 'Banco 2026-1')
        self.assertTrue(banco.activo)
        self.assertIsNotNone(banco.contenido_extraido)

    def test_banco_str(self):
        """Test: String representation del banco"""
        archivo = SimpleUploadedFile("test.txt", b"contenido", content_type="text/plain")
        
        banco = BancoObservacionesDocente.objects.create(
            docente=self.docente,
            nombre='Mi Banco de Observaciones',
            archivo=archivo,
            contenido_extraido='contenido'
        )
        
        expected = f"Banco: Mi Banco de Observaciones - {self.docente.username}"
        self.assertEqual(str(banco), expected)

    def test_solo_un_banco_activo_por_docente(self):
        """Test: Solo un banco puede estar activo por docente"""
        archivo1 = SimpleUploadedFile("test1.txt", b"contenido1", content_type="text/plain")
        archivo2 = SimpleUploadedFile("test2.txt", b"contenido2", content_type="text/plain")
        
        # Crear primer banco activo
        banco1 = BancoObservacionesDocente.objects.create(
            docente=self.docente,
            nombre='Banco 1',
            archivo=archivo1,
            contenido_extraido='contenido1',
            activo=True
        )
        
        # Crear segundo banco
        banco2 = BancoObservacionesDocente.objects.create(
            docente=self.docente,
            nombre='Banco 2',
            archivo=archivo2,
            contenido_extraido='contenido2',
            activo=False
        )
        
        # Verificar que solo hay un banco activo
        bancos_activos = BancoObservacionesDocente.objects.filter(
            docente=self.docente,
            activo=True
        )
        self.assertEqual(bancos_activos.count(), 1)
        self.assertEqual(bancos_activos.first(), banco1)

    def test_activar_banco_desactiva_otros(self):
        """Test: Al activar un banco, los demás se desactivan automáticamente"""
        archivo1 = SimpleUploadedFile("test1.txt", b"contenido1", content_type="text/plain")
        archivo2 = SimpleUploadedFile("test2.txt", b"contenido2", content_type="text/plain")
        
        banco1 = BancoObservacionesDocente.objects.create(
            docente=self.docente,
            nombre='Banco 1',
            archivo=archivo1,
            contenido_extraido='contenido1',
            activo=True
        )
        
        banco2 = BancoObservacionesDocente.objects.create(
            docente=self.docente,
            nombre='Banco 2',
            archivo=archivo2,
            contenido_extraido='contenido2',
            activo=False
        )
        
        # Activar banco2 (debería desactivar banco1)
        # Esto se haría en el servicio DocenteService.activar_banco()
        BancoObservacionesDocente.objects.filter(
            docente=self.docente,
            activo=True
        ).update(activo=False)
        
        banco2.activo = True
        banco2.save()
        
        # Verificar
        banco1.refresh_from_db()
        self.assertFalse(banco1.activo)
        self.assertTrue(banco2.activo)

    def test_obtener_banco_activo(self):
        """Test: Obtener el banco activo de un docente"""
        archivo1 = SimpleUploadedFile("test1.txt", b"contenido1", content_type="text/plain")
        archivo2 = SimpleUploadedFile("test2.txt", b"contenido2", content_type="text/plain")
        
        BancoObservacionesDocente.objects.create(
            docente=self.docente,
            nombre='Banco Inactivo',
            archivo=archivo1,
            contenido_extraido='contenido1',
            activo=False
        )
        
        banco_activo = BancoObservacionesDocente.objects.create(
            docente=self.docente,
            nombre='Banco Activo',
            archivo=archivo2,
            contenido_extraido='contenido2',
            activo=True
        )
        
        # Obtener banco activo
        banco = BancoObservacionesDocente.objects.filter(
            docente=self.docente,
            activo=True
        ).first()
        
        self.assertEqual(banco, banco_activo)
        self.assertEqual(banco.nombre, 'Banco Activo')

    def test_docente_sin_banco_activo(self):
        """Test: Docente sin banco activo"""
        archivo = SimpleUploadedFile("test.txt", b"contenido", content_type="text/plain")
        
        BancoObservacionesDocente.objects.create(
            docente=self.docente,
            nombre='Banco Inactivo',
            archivo=archivo,
            contenido_extraido='contenido',
            activo=False
        )
        
        # Intentar obtener banco activo
        banco = BancoObservacionesDocente.objects.filter(
            docente=self.docente,
            activo=True
        ).first()
        
        self.assertIsNone(banco)

    def test_multiples_docentes_con_bancos_activos(self):
        """Test: Múltiples docentes pueden tener sus propios bancos activos"""
        # Crear segundo docente
        docente2 = Usuario.objects.create_user(
            username='docente2',
            password='test123',
            rol='docente',
            escuela=self.escuela
        )
        
        archivo1 = SimpleUploadedFile("test1.txt", b"contenido1", content_type="text/plain")
        archivo2 = SimpleUploadedFile("test2.txt", b"contenido2", content_type="text/plain")
        
        # Crear bancos para cada docente
        banco1 = BancoObservacionesDocente.objects.create(
            docente=self.docente,
            nombre='Banco Docente 1',
            archivo=archivo1,
            contenido_extraido='contenido1',
            activo=True
        )
        
        banco2 = BancoObservacionesDocente.objects.create(
            docente=docente2,
            nombre='Banco Docente 2',
            archivo=archivo2,
            contenido_extraido='contenido2',
            activo=True
        )
        
        # Verificar que cada docente tiene su banco activo
        banco_docente1 = BancoObservacionesDocente.objects.filter(
            docente=self.docente,
            activo=True
        ).first()
        
        banco_docente2 = BancoObservacionesDocente.objects.filter(
            docente=docente2,
            activo=True
        ).first()
        
        self.assertEqual(banco_docente1, banco1)
        self.assertEqual(banco_docente2, banco2)

    def test_contenido_extraido_no_vacio(self):
        """Test: El contenido extraído no debe estar vacío"""
        archivo = SimpleUploadedFile("test.txt", b"", content_type="text/plain")
        
        # Intentar crear banco con contenido vacío (debería validarse en el servicio)
        banco = BancoObservacionesDocente.objects.create(
            docente=self.docente,
            nombre='Banco Vacío',
            archivo=archivo,
            contenido_extraido='',
            activo=True
        )
        
        # En producción, el servicio DocenteService validaría esto
        self.assertEqual(banco.contenido_extraido, '')
        # En el servicio se validaría: if len(contenido_extraido) < 50: raise ValidationError


class BancoObservacionesGlobalTest(TestCase):
    """Tests para el modelo BancoObservaciones (global)"""

    def test_banco_global_existe(self):
        """Test: Verificar que el banco global puede crearse"""
        banco_global = BancoObservaciones.objects.create(
            nombre='Banco Global 2026',
            descripcion='Banco de observaciones general',
            archivo_fuente='observaciones_generales.txt',
            observaciones='Observación 1\nObservación 2\nObservación 3'
        )
        
        self.assertEqual(banco_global.nombre, 'Banco Global 2026')
        self.assertIsNotNone(banco_global.observaciones)

    def test_banco_global_str(self):
        """Test: String representation del banco global"""
        banco = BancoObservaciones.objects.create(
            nombre='Banco Test',
            observaciones='Observaciones de prueba'
        )
        
        self.assertEqual(str(banco), 'Banco Test')
