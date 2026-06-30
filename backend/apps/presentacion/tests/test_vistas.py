"""
Tests para las vistas de la capa de presentación
"""
from django.test import TestCase, Client
from django.urls import reverse
from apps.usuarios.models import Usuario
from apps.escuelas.models import Escuela
from apps.informes.models import Informe


class AuthViewsTest(TestCase):
    """Tests para vistas de autenticación"""

    def setUp(self):
        """Configuración inicial"""
        self.client = Client()
        
        # Crear secretaria
        self.secretaria = Usuario.objects.create_user(
            username='secretaria1',
            password='test123',
            rol='secretaria',
            email='secretaria@untels.edu.pe'
        )
        
        # Crear presidente
        self.presidente = Usuario.objects.create_user(
            username='presidente1',
            password='test123',
            rol='presidente',
            email='presidente@untels.edu.pe'
        )
        
        # Crear escuela
        self.escuela = Escuela.objects.create(
            nombre='Ingeniería de Sistemas',
            codigo='ISI',
            presidente=self.presidente
        )
        
        self.presidente.escuela = self.escuela
        self.presidente.save()

    def test_login_secretaria_get(self):
        """Test: GET login secretaria muestra el formulario"""
        response = self.client.get(reverse('login_secretaria'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login_secretaria.html')

    def test_login_secretaria_post_correcto(self):
        """Test: POST login secretaria con credenciales correctas"""
        response = self.client.post(reverse('login_secretaria'), {
            'username': 'secretaria1',
            'password': 'test123'
        })
        
        # Debe redirigir al dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('secretaria_dashboard'))

    def test_login_secretaria_post_incorrecto(self):
        """Test: POST login secretaria con credenciales incorrectas"""
        response = self.client.post(reverse('login_secretaria'), {
            'username': 'secretaria1',
            'password': 'wrongpassword'
        })
        
        # Debe mostrar error
        self.assertEqual(response.status_code, 200)
        # Verificar mensaje de error en messages framework

    def test_login_presidente_get(self):
        """Test: GET login presidente muestra el formulario"""
        response = self.client.get(reverse('login_presidente'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login_presidente.html')

    def test_login_presidente_post_correcto(self):
        """Test: POST login presidente con credenciales correctas"""
        response = self.client.post(reverse('login_presidente'), {
            'username': 'presidente1',
            'password': 'test123'
        })
        
        # Debe redirigir al dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('presidente_dashboard'))


class SecretariaViewsTest(TestCase):
    """Tests para vistas de Secretaria"""

    def setUp(self):
        """Configuración inicial"""
        self.client = Client()
        
        self.secretaria = Usuario.objects.create_user(
            username='secretaria1',
            password='test123',
            rol='secretaria'
        )
        
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
        
        self.estudiante = Usuario.objects.create_user(
            username='2020123456',
            password='test123',
            rol='estudiante'
        )
        
        # Login como secretaria
        self.client.login(username='secretaria1', password='test123')

    def test_secretaria_dashboard_acceso(self):
        """Test: Secretaria puede acceder a su dashboard"""
        response = self.client.get(reverse('secretaria_dashboard'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'secretaria/dashboard.html')

    def test_secretaria_dashboard_contenido(self):
        """Test: Dashboard muestra estadísticas"""
        # Crear informe pendiente
        Informe.objects.create(
            usuario=self.estudiante,
            titulo='Informe Test',
            descripcion='Descripción',
            estado='pendiente_secretaria'
        )
        
        response = self.client.get(reverse('secretaria_dashboard'))
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('estadisticas', response.context)
        self.assertIn('informes_pendientes', response.context)

    def test_secretaria_derivar_get(self):
        """Test: GET derivar muestra el formulario"""
        informe = Informe.objects.create(
            usuario=self.estudiante,
            titulo='Informe Test',
            descripcion='Descripción',
            estado='pendiente_secretaria'
        )
        
        response = self.client.get(
            reverse('secretaria_derivar', args=[informe.id])
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'secretaria/derivar.html')
        self.assertIn('informe', response.context)
        self.assertIn('escuelas', response.context)

    def test_secretaria_derivar_post(self):
        """Test: POST derivar envía informe a presidente"""
        informe = Informe.objects.create(
            usuario=self.estudiante,
            titulo='Informe Test',
            descripcion='Descripción',
            estado='pendiente_secretaria'
        )
        
        response = self.client.post(
            reverse('secretaria_derivar', args=[informe.id]),
            {'escuela_id': self.escuela.id}
        )
        
        # Debe redirigir al dashboard
        self.assertEqual(response.status_code, 302)
        
        # Verificar que el informe cambió de estado
        informe.refresh_from_db()
        self.assertEqual(informe.estado, 'pendiente_presidente')
        self.assertEqual(informe.escuela, self.escuela)


class PresidenteViewsTest(TestCase):
    """Tests para vistas de Presidente"""

    def setUp(self):
        """Configuración inicial"""
        self.client = Client()
        
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
        
        self.presidente.escuela = self.escuela
        self.presidente.save()
        
        self.docente = Usuario.objects.create_user(
            username='docente1',
            password='test123',
            rol='docente',
            escuela=self.escuela
        )
        
        self.estudiante = Usuario.objects.create_user(
            username='2020123456',
            password='test123',
            rol='estudiante'
        )
        
        # Login como presidente
        self.client.login(username='presidente1', password='test123')

    def test_presidente_dashboard_acceso(self):
        """Test: Presidente puede acceder a su dashboard"""
        response = self.client.get(reverse('presidente_dashboard'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'presidente/dashboard.html')

    def test_presidente_designar_get(self):
        """Test: GET designar muestra el formulario"""
        informe = Informe.objects.create(
            usuario=self.estudiante,
            titulo='Informe Test',
            descripcion='Descripción',
            estado='pendiente_presidente',
            escuela=self.escuela,
            presidente_asignado=self.presidente
        )
        
        response = self.client.get(
            reverse('presidente_designar', args=[informe.id])
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'presidente/designar.html')
        self.assertIn('informe', response.context)
        self.assertIn('docentes', response.context)

    def test_presidente_designar_post(self):
        """Test: POST designar asigna docente"""
        informe = Informe.objects.create(
            usuario=self.estudiante,
            titulo='Informe Test',
            descripcion='Descripción',
            estado='pendiente_presidente',
            escuela=self.escuela,
            presidente_asignado=self.presidente
        )
        
        response = self.client.post(
            reverse('presidente_designar', args=[informe.id]),
            {'docente_id': self.docente.id}
        )
        
        # Debe redirigir
        self.assertEqual(response.status_code, 302)
        
        # Verificar asignación
        informe.refresh_from_db()
        self.assertEqual(informe.estado, 'pendiente_docente')
        self.assertEqual(informe.docente_asignado, self.docente)

    def test_presidente_revisar_get(self):
        """Test: GET revisar muestra el dictamen"""
        informe = Informe.objects.create(
            usuario=self.estudiante,
            titulo='Informe Test',
            descripcion='Descripción',
            estado='pendiente_aprobacion_presidente',
            escuela=self.escuela,
            presidente_asignado=self.presidente,
            docente_asignado=self.docente,
            dictamen_docente='Dictamen de prueba',
            recomendacion_docente='aprobar'
        )
        
        response = self.client.get(
            reverse('presidente_revisar', args=[informe.id])
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'presidente/revisar.html')
        self.assertIn('informe', response.context)


class DocenteViewsTest(TestCase):
    """Tests para vistas de Docente"""

    def setUp(self):
        """Configuración inicial"""
        self.client = Client()
        
        presidente = Usuario.objects.create_user(
            username='presidente1',
            password='test123',
            rol='presidente'
        )
        
        self.escuela = Escuela.objects.create(
            nombre='Ingeniería de Sistemas',
            codigo='ISI',
            presidente=presidente
        )
        
        self.docente = Usuario.objects.create_user(
            username='docente1',
            password='test123',
            rol='docente',
            escuela=self.escuela
        )
        
        self.estudiante = Usuario.objects.create_user(
            username='2020123456',
            password='test123',
            rol='estudiante'
        )
        
        # Login como docente
        self.client.login(username='docente1', password='test123')

    def test_docente_dashboard_acceso(self):
        """Test: Docente puede acceder a su dashboard"""
        response = self.client.get(reverse('panel_docente'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'docente/dashboard.html')

    def test_docente_banco_get(self):
        """Test: GET banco muestra la gestión de bancos"""
        response = self.client.get(reverse('docente_banco'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'docente/banco.html')
        self.assertIn('bancos', response.context)

    def test_docente_revisar_get(self):
        """Test: GET revisar muestra el informe a revisar"""
        informe = Informe.objects.create(
            usuario=self.estudiante,
            titulo='Informe Test',
            descripcion='Descripción',
            estado='pendiente_docente',
            escuela=self.escuela,
            docente_asignado=self.docente
        )
        
        response = self.client.get(
            reverse('docente_revisar', args=[informe.id])
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'docente/revisar.html')
        self.assertIn('informe', response.context)
