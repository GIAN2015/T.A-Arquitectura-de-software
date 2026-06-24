import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.usuarios.models import Usuario

if not Usuario.objects.filter(codigo='DOCENTE001').exists():
    docente = Usuario.objects.create(
        codigo='DOCENTE001',
        nombre='Docente de Prueba',
        tipo_usuario='docente'
    )
    docente.set_password('docente123')
    print('Docente de prueba creado: DOCENTE001 / docente123')
else:
    print('Docente de prueba ya existe')
