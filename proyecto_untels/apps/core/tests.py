from django.test import TestCase, Client
from django.urls import reverse
from apps.usuarios.models import Usuario
from apps.usuarios.services import registrar_usuario

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuario = registrar_usuario(
            codigo='2021101234',
            nombre='Juan Pérez',
            password='test123',
            tipo_usuario='estudiante'
        )
        self.docente = registrar_usuario(
            codigo='DOC001',
            nombre='Prof. García',
            password='test123',
            tipo_usuario='docente'
        )
    
    def test_login_view_get(self):
        """Test GET request a la página de login"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
    
    def test_login_view_post_success(self):
        """Test login exitoso"""
        response = self.client.post(reverse('login'), {
            'codigo': '2021101234',
            'password': 'test123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse('upload'))
    
    def test_login_view_post_fail(self):
        """Test login con contraseña incorrecta"""
        response = self.client.post(reverse('login'), {
            'codigo': '2021101234',
            'password': 'wrong_password'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'incorrectos')
    
    def test_registro_view_get(self):
        """Test GET request a la página de registro"""
        response = self.client.get(reverse('registro'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registro.html')
    
    def test_registro_view_post_success(self):
        """Test registro exitoso"""
        response = self.client.post(reverse('registro'), {
            'codigo': '2021999999',
            'nombre': 'Test User',
            'password': 'test123',
            'password_confirm': 'test123',
            'tipo_usuario': 'estudiante'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(Usuario.objects.filter(codigo='2021999999').exists())
    
    def test_upload_view_requires_login(self):
        """Test que upload requiere login"""
        response = self.client.get(reverse('upload'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
    
    def test_historial_view_requires_login(self):
        """Test que historial requiere login"""
        response = self.client.get(reverse('historial'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
    
    def test_panel_docente_requires_login(self):
        """Test que panel docente requiere login"""
        response = self.client.get(reverse('panel_docente'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
    
    def test_panel_docente_requires_docente_role(self):
        """Test que panel docente requiere rol de docente"""
        # Login como estudiante
        session = self.client.session
        session['usuario_id'] = self.usuario.id
        session['usuario_tipo'] = 'estudiante'
        session.save()
        
        response = self.client.get(reverse('panel_docente'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('upload'))
    
    def test_logout_view(self):
        """Test logout"""
        # Login primero
        session = self.client.session
        session['usuario_id'] = self.usuario.id
        session.save()
        
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        
        # Verificar que la sesión fue limpiada
        self.assertNotIn('usuario_id', self.client.session)
