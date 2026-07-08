from django.test import TestCase
from apps.usuarios.models import Usuario
from .models import Informe
from .state import InformeStateError

class InformeModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(
            codigo='2021101234',
            nombre='Juan Pérez',
            tipo_usuario='estudiante'
        )
    
    def test_crear_informe(self):
        """Test crear un informe"""
        informe = Informe.objects.create(
            usuario=self.usuario,
            nombre_archivo='informe_test.docx',
            contenido='Contenido de prueba',
            estado=Informe.ESTADO_ENVIADO
        )
        self.assertEqual(informe.nombre_archivo, 'informe_test.docx')
        self.assertEqual(informe.estado, Informe.ESTADO_ENVIADO)
        self.assertEqual(informe.usuario, self.usuario)
    
    def test_estados_informe(self):
        """Test flujo de estados del informe v2.0"""
        informe = Informe.objects.create(
            usuario=self.usuario,
            nombre_archivo='informe_test.docx',
            contenido='Contenido de prueba'
        )

        self.assertEqual(informe.estado, Informe.ESTADO_ENVIADO)

        informe.transition_to(Informe.ESTADO_PENDIENTE_SECRETARIA)
        self.assertEqual(informe.estado, Informe.ESTADO_PENDIENTE_SECRETARIA)

        informe.transition_to(Informe.ESTADO_PENDIENTE_PRESIDENTE)
        self.assertEqual(informe.estado, Informe.ESTADO_PENDIENTE_PRESIDENTE)

        informe.transition_to(Informe.ESTADO_PENDIENTE_DOCENTE)
        self.assertEqual(informe.estado, Informe.ESTADO_PENDIENTE_DOCENTE)

        informe.transition_to(Informe.ESTADO_VALIDANDO_IA)
        self.assertEqual(informe.estado, Informe.ESTADO_VALIDANDO_IA)

        informe.transition_to(Informe.ESTADO_REVISION_DOCENTE)
        self.assertEqual(informe.estado, Informe.ESTADO_REVISION_DOCENTE)

        informe.transition_to(Informe.ESTADO_PENDIENTE_APROBACION_PRESIDENTE)
        self.assertEqual(informe.estado, Informe.ESTADO_PENDIENTE_APROBACION_PRESIDENTE)

        informe.transition_to(Informe.ESTADO_APROBADO_PRESIDENTE)
        self.assertEqual(informe.estado, Informe.ESTADO_APROBADO_PRESIDENTE)

        informe.transition_to(Informe.ESTADO_APROBADO_FINAL)
        self.assertEqual(informe.estado, Informe.ESTADO_APROBADO_FINAL)

    def test_transicion_invalida_lanza_error(self):
        informe = Informe.objects.create(
            usuario=self.usuario,
            nombre_archivo='informe_test.docx',
            contenido='Contenido de prueba'
        )

        with self.assertRaises(InformeStateError):
            informe.transition_to(Informe.ESTADO_APROBADO_FINAL)
    
    def test_informe_str(self):
        """Test representación en string del informe"""
        informe = Informe.objects.create(
            usuario=self.usuario,
            nombre_archivo='informe_test.docx',
            contenido='Contenido de prueba'
        )
        expected = 'informe_test.docx - Juan Pérez [Enviado por Estudiante]'
        self.assertEqual(str(informe), expected)
