"""
Tests para el modelo Escuela
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.usuarios.models import Usuario
from apps.escuelas.models import Escuela


class EscuelaModelTest(TestCase):
    """Tests para el modelo Escuela"""

    def setUp(self):
        """Configuración inicial para los tests"""
        # Crear un usuario presidente
        self.presidente = Usuario.objects.create_user(
            username='presidente1',
            password='test123',
            rol='presidente',
            email='presidente@untels.edu.pe',
            activo=True
        )

    def test_crear_escuela(self):
        """Test: Crear una escuela correctamente"""
        escuela = Escuela.objects.create(
            nombre='Ingeniería de Sistemas e Informática',
            codigo='ISI',
            presidente=self.presidente,
            activo=True
        )
        
        self.assertEqual(escuela.nombre, 'Ingeniería de Sistemas e Informática')
        self.assertEqual(escuela.codigo, 'ISI')
        self.assertEqual(escuela.presidente, self.presidente)
        self.assertTrue(escuela.activo)

    def test_escuela_str(self):
        """Test: String representation de escuela"""
        escuela = Escuela.objects.create(
            nombre='Ingeniería Ambiental',
            codigo='IA',
            presidente=self.presidente
        )
        
        self.assertEqual(str(escuela), 'Ingeniería Ambiental')

    def test_escuela_sin_presidente(self):
        """Test: Crear escuela sin presidente (debe fallar)"""
        with self.assertRaises(Exception):
            Escuela.objects.create(
                nombre='Ingeniería Mecánica',
                codigo='IM',
                presidente=None
            )

    def test_codigo_unico(self):
        """Test: El código de escuela debe ser único"""
        Escuela.objects.create(
            nombre='Ingeniería de Sistemas',
            codigo='ISI',
            presidente=self.presidente
        )
        
        # Intentar crear otra escuela con el mismo código
        with self.assertRaises(Exception):
            Escuela.objects.create(
                nombre='Otra Escuela',
                codigo='ISI',
                presidente=self.presidente
            )

    def test_desactivar_escuela(self):
        """Test: Desactivar una escuela"""
        escuela = Escuela.objects.create(
            nombre='Ingeniería Electrónica',
            codigo='IE',
            presidente=self.presidente,
            activo=True
        )
        
        escuela.activo = False
        escuela.save()
        
        escuela_actualizada = Escuela.objects.get(id=escuela.id)
        self.assertFalse(escuela_actualizada.activo)

    def test_cambiar_presidente(self):
        """Test: Cambiar presidente de una escuela"""
        # Crear segundo presidente
        nuevo_presidente = Usuario.objects.create_user(
            username='presidente2',
            password='test123',
            rol='presidente',
            email='presidente2@untels.edu.pe'
        )
        
        escuela = Escuela.objects.create(
            nombre='Ingeniería Mecatrónica',
            codigo='IMT',
            presidente=self.presidente
        )
        
        # Cambiar presidente
        escuela.presidente = nuevo_presidente
        escuela.save()
        
        escuela_actualizada = Escuela.objects.get(id=escuela.id)
        self.assertEqual(escuela_actualizada.presidente, nuevo_presidente)

    def test_obtener_escuelas_activas(self):
        """Test: Filtrar escuelas activas"""
        Escuela.objects.create(
            nombre='Escuela Activa 1',
            codigo='EA1',
            presidente=self.presidente,
            activo=True
        )
        Escuela.objects.create(
            nombre='Escuela Activa 2',
            codigo='EA2',
            presidente=self.presidente,
            activo=True
        )
        Escuela.objects.create(
            nombre='Escuela Inactiva',
            codigo='EI',
            presidente=self.presidente,
            activo=False
        )
        
        escuelas_activas = Escuela.objects.filter(activo=True)
        self.assertEqual(escuelas_activas.count(), 2)

    def test_relacion_con_usuario(self):
        """Test: Relación entre Escuela y Usuario (presidente)"""
        escuela = Escuela.objects.create(
            nombre='Ingeniería Civil',
            codigo='IC',
            presidente=self.presidente
        )
        
        # Asignar escuela al presidente
        self.presidente.escuela = escuela
        self.presidente.save()
        
        # Verificar relación
        self.assertEqual(self.presidente.escuela, escuela)
        self.assertEqual(escuela.presidente, self.presidente)
