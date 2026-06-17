from django.core.management.base import BaseCommand
from apps.usuarios.services import registrar_usuario

class Command(BaseCommand):
    help = 'Crea usuarios de demostración para pruebas'

    def handle(self, *args, **options):
        usuarios_demo = [
            {
                'codigo': '2021101234',
                'nombre': 'Juan Carlos Pérez García',
                'password': 'demo123',
                'tipo_usuario': 'estudiante'
            },
            {
                'codigo': '2022105678',
                'nombre': 'María Elena Rodríguez López',
                'password': 'demo123',
                'tipo_usuario': 'estudiante'
            },
            {
                'codigo': '2019103456',
                'nombre': 'Pedro Antonio Sánchez Díaz',
                'password': 'demo123',
                'tipo_usuario': 'egresado'
            },
            {
                'codigo': 'DOC001',
                'nombre': 'Prof. Roberto García Martínez',
                'password': 'docente123',
                'tipo_usuario': 'docente'
            },
        ]

        created_count = 0
        existing_count = 0

        for datos in usuarios_demo:
            usuario = registrar_usuario(
                codigo=datos['codigo'],
                nombre=datos['nombre'],
                password=datos['password'],
                tipo_usuario=datos['tipo_usuario']
            )
            
            if usuario:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Usuario creado: {datos["codigo"]} - {datos["nombre"]} ({datos["tipo_usuario"]})'
                    )
                )
                created_count += 1
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'○ Usuario ya existe: {datos["codigo"]}'
                    )
                )
                existing_count += 1

        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'\nResumen:'))
        self.stdout.write(f'  Usuarios creados: {created_count}')
        self.stdout.write(f'  Usuarios existentes: {existing_count}')
        self.stdout.write('\nTodos los usuarios usan la contraseña: demo123')
        self.stdout.write('(excepto docentes que usan: docente123)\n')
