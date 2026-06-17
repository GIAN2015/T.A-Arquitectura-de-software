from django.test import TestCase
from .models import Usuario
from .services import registrar_usuario, autenticar_usuario

class UsuarioModelTest(TestCase):
    def test_crear_usuario(self):
        """Test crear un usuario básico"""
        usuario = Usuario.objects.create(
            codigo='2021101234',
            nombre='Juan Pérez',
            tipo_usuario='estudiante'
        )
        self.assertEqual(usuario.codigo, '2021101234')
        self.assertEqual(usuario.nombre, 'Juan Pérez')
        self.assertEqual(usuario.tipo_usuario, 'estudiante')
    
    def test_set_password(self):
        """Test establecer contraseña"""
        usuario = Usuario.objects.create(
            codigo='2021101234',
            nombre='Juan Pérez'
        )
        usuario.set_password('test123')
        self.assertIsNotNone(usuario.password)
        self.assertTrue(usuario.check_password('test123'))
        self.assertFalse(usuario.check_password('wrong_password'))

class UsuarioServiceTest(TestCase):
    def test_registrar_usuario(self):
        """Test registrar un nuevo usuario"""
        usuario = registrar_usuario(
            codigo='2021101234',
            nombre='Juan Pérez',
            password='test123',
            tipo_usuario='estudiante'
        )
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.codigo, '2021101234')
        self.assertTrue(usuario.check_password('test123'))
    
    def test_registrar_usuario_duplicado(self):
        """Test registrar usuario con código duplicado"""
        registrar_usuario('2021101234', 'Juan Pérez', 'test123')
        usuario2 = registrar_usuario('2021101234', 'Pedro García', 'test456')
        self.assertIsNone(usuario2)
    
    def test_autenticar_usuario(self):
        """Test autenticar usuario"""
        registrar_usuario('2021101234', 'Juan Pérez', 'test123')
        
        # Autenticación correcta
        usuario = autenticar_usuario('2021101234', 'test123')
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.codigo, '2021101234')
        
        # Autenticación incorrecta
        usuario = autenticar_usuario('2021101234', 'wrong_password')
        self.assertIsNone(usuario)
        
        # Usuario no existe
        usuario = autenticar_usuario('9999999999', 'test123')
        self.assertIsNone(usuario)
