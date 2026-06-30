"""
Script para poblar datos de prueba para el sistema v2.0

Uso:
    python manage.py shell < scripts/poblar_datos_prueba_v2.py

O desde el shell de Django:
    python manage.py shell
    >>> exec(open('scripts/poblar_datos_prueba_v2.py').read())
"""

from django.core.files.uploadedfile import SimpleUploadedFile
from apps.usuarios.models import Usuario
from apps.escuelas.models import Escuela
from apps.observaciones.models import BancoObservacionesDocente
from apps.informes.models import Informe


def crear_datos_prueba():
    """Crear todos los datos de prueba para el sistema v2.0"""
    
    print("="*80)
    print("POBLANDO DATOS DE PRUEBA - SISTEMA v2.0")
    print("="*80)
    
    # ==========================================
    # 1. CREAR ESCUELAS Y PRESIDENTES
    # ==========================================
    print("\n1. Creando Escuelas y Presidentes...")
    
    # Presidente 1 - Ingeniería de Sistemas
    presidente_isi, created = Usuario.objects.get_or_create(
        username='presidente_isi',
        defaults={
            'password': 'pbkdf2_sha256$600000$test$test',  # password: test123
            'rol': 'presidente',
            'email': 'presidente.isi@untels.edu.pe',
            'first_name': 'Juan',
            'last_name': 'Pérez García',
            'activo': True
        }
    )
    if created:
        presidente_isi.set_password('test123')
        presidente_isi.save()
        print(f"   ✓ Presidente ISI creado: {presidente_isi.username}")
    
    # Escuela de Ingeniería de Sistemas
    escuela_isi, created = Escuela.objects.get_or_create(
        codigo='ISI',
        defaults={
            'nombre': 'Ingeniería de Sistemas e Informática',
            'presidente': presidente_isi,
            'activo': True
        }
    )
    if created:
        print(f"   ✓ Escuela creada: {escuela_isi.nombre}")
    
    # Asignar escuela al presidente
    presidente_isi.escuela = escuela_isi
    presidente_isi.save()
    
    # Presidente 2 - Ingeniería Ambiental
    presidente_ia, created = Usuario.objects.get_or_create(
        username='presidente_ia',
        defaults={
            'password': 'pbkdf2_sha256$600000$test$test',
            'rol': 'presidente',
            'email': 'presidente.ia@untels.edu.pe',
            'first_name': 'María',
            'last_name': 'López Rodríguez',
            'activo': True
        }
    )
    if created:
        presidente_ia.set_password('test123')
        presidente_ia.save()
        print(f"   ✓ Presidente IA creado: {presidente_ia.username}")
    
    # Escuela de Ingeniería Ambiental
    escuela_ia, created = Escuela.objects.get_or_create(
        codigo='IA',
        defaults={
            'nombre': 'Ingeniería Ambiental',
            'presidente': presidente_ia,
            'activo': True
        }
    )
    if created:
        print(f"   ✓ Escuela creada: {escuela_ia.nombre}")
    
    presidente_ia.escuela = escuela_ia
    presidente_ia.save()
    
    # ==========================================
    # 2. CREAR SECRETARIA
    # ==========================================
    print("\n2. Creando Secretaria...")
    
    secretaria, created = Usuario.objects.get_or_create(
        username='secretaria1',
        defaults={
            'password': 'pbkdf2_sha256$600000$test$test',
            'rol': 'secretaria',
            'email': 'secretaria@untels.edu.pe',
            'first_name': 'Ana',
            'last_name': 'Torres Quispe',
            'activo': True
        }
    )
    if created:
        secretaria.set_password('test123')
        secretaria.save()
        print(f"   ✓ Secretaria creada: {secretaria.username}")
    
    # ==========================================
    # 3. CREAR DOCENTES
    # ==========================================
    print("\n3. Creando Docentes...")
    
    # Docente 1 - ISI
    docente_isi_1, created = Usuario.objects.get_or_create(
        username='docente_isi_1',
        defaults={
            'password': 'pbkdf2_sha256$600000$test$test',
            'rol': 'docente',
            'email': 'docente1.isi@untels.edu.pe',
            'first_name': 'Carlos',
            'last_name': 'Ramírez Soto',
            'escuela': escuela_isi,
            'activo': True
        }
    )
    if created:
        docente_isi_1.set_password('test123')
        docente_isi_1.save()
        print(f"   ✓ Docente ISI 1 creado: {docente_isi_1.username}")
    
    # Docente 2 - ISI
    docente_isi_2, created = Usuario.objects.get_or_create(
        username='docente_isi_2',
        defaults={
            'password': 'pbkdf2_sha256$600000$test$test',
            'rol': 'docente',
            'email': 'docente2.isi@untels.edu.pe',
            'first_name': 'Luis',
            'last_name': 'Fernández Cruz',
            'escuela': escuela_isi,
            'activo': True
        }
    )
    if created:
        docente_isi_2.set_password('test123')
        docente_isi_2.save()
        print(f"   ✓ Docente ISI 2 creado: {docente_isi_2.username}")
    
    # Docente 1 - IA
    docente_ia_1, created = Usuario.objects.get_or_create(
        username='docente_ia_1',
        defaults={
            'password': 'pbkdf2_sha256$600000$test$test',
            'rol': 'docente',
            'email': 'docente1.ia@untels.edu.pe',
            'first_name': 'Patricia',
            'last_name': 'Vargas Mendoza',
            'escuela': escuela_ia,
            'activo': True
        }
    )
    if created:
        docente_ia_1.set_password('test123')
        docente_ia_1.save()
        print(f"   ✓ Docente IA 1 creado: {docente_ia_1.username}")
    
    # ==========================================
    # 4. CREAR ESTUDIANTES
    # ==========================================
    print("\n4. Creando Estudiantes...")
    
    estudiantes_data = [
        ('2020123456', 'Pedro', 'García López', 'pedro.garcia@untels.edu.pe'),
        ('2020123457', 'Laura', 'Martínez Ruiz', 'laura.martinez@untels.edu.pe'),
        ('2020123458', 'Jorge', 'Sánchez Torres', 'jorge.sanchez@untels.edu.pe'),
        ('2021234567', 'Sandra', 'Flores Quispe', 'sandra.flores@untels.edu.pe'),
        ('2021234568', 'Miguel', 'Rojas Castro', 'miguel.rojas@untels.edu.pe'),
    ]
    
    estudiantes = []
    for username, first_name, last_name, email in estudiantes_data:
        estudiante, created = Usuario.objects.get_or_create(
            username=username,
            defaults={
                'password': 'pbkdf2_sha256$600000$test$test',
                'rol': 'estudiante',
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'activo': True
            }
        )
        if created:
            estudiante.set_password('test123')
            estudiante.save()
            print(f"   ✓ Estudiante creado: {estudiante.username} - {first_name} {last_name}")
        estudiantes.append(estudiante)
    
    # ==========================================
    # 5. CREAR BANCOS DE OBSERVACIONES
    # ==========================================
    print("\n5. Creando Bancos de Observaciones para Docentes...")
    
    contenido_banco_isi = """
    BANCO DE OBSERVACIONES - INGENIERÍA DE SISTEMAS
    
    CAPÍTULO I - INTRODUCCIÓN:
    - Falta justificación del proyecto
    - No se presenta el problema claramente
    - Objetivos deben ser más específicos y medibles
    
    CAPÍTULO II - MARCO TEÓRICO:
    - Referencias bibliográficas incompletas
    - Falta actualización de fuentes (últimos 5 años)
    - No se relacionan los conceptos con el proyecto
    
    CAPÍTULO III - METODOLOGÍA:
    - Debe especificar metodología de desarrollo de software
    - Falta descripción de herramientas utilizadas
    - No se justifica la elección de la metodología
    
    CAPÍTULO IV - RESULTADOS:
    - Debe incluir capturas de pantalla del sistema
    - Falta análisis de resultados
    - No se comparan con objetivos planteados
    
    ASPECTOS FORMALES:
    - Revisar ortografía y redacción
    - Unificar formato de citas bibliográficas
    - Numeración de páginas incorrecta
    """
    
    contenido_banco_ia = """
    BANCO DE OBSERVACIONES - INGENIERÍA AMBIENTAL
    
    ASPECTOS TÉCNICOS:
    - Falta análisis de impacto ambiental
    - Debe incluir normativa ambiental vigente
    - No se presentan alternativas de solución
    
    METODOLOGÍA:
    - Debe especificar métodos de medición
    - Falta cronograma de actividades
    - No se justifican los equipos utilizados
    
    RESULTADOS:
    - Falta análisis cuantitativo
    - Debe incluir gráficos comparativos
    - No se relacionan con la normativa
    """
    
    # Banco para docente ISI 1
    archivo_banco_isi_1 = SimpleUploadedFile(
        "banco_isi_1.txt",
        contenido_banco_isi.encode('utf-8'),
        content_type="text/plain"
    )
    
    banco_isi_1, created = BancoObservacionesDocente.objects.get_or_create(
        docente=docente_isi_1,
        nombre='Banco ISI 2026-1',
        defaults={
            'archivo': archivo_banco_isi_1,
            'contenido_extraido': contenido_banco_isi,
            'activo': True
        }
    )
    if created:
        print(f"   ✓ Banco creado para: {docente_isi_1.username}")
    
    # Banco para docente IA 1
    archivo_banco_ia_1 = SimpleUploadedFile(
        "banco_ia_1.txt",
        contenido_banco_ia.encode('utf-8'),
        content_type="text/plain"
    )
    
    banco_ia_1, created = BancoObservacionesDocente.objects.get_or_create(
        docente=docente_ia_1,
        nombre='Banco IA 2026-1',
        defaults={
            'archivo': archivo_banco_ia_1,
            'contenido_extraido': contenido_banco_ia,
            'activo': True
        }
    )
    if created:
        print(f"   ✓ Banco creado para: {docente_ia_1.username}")
    
    # ==========================================
    # 6. CREAR INFORMES DE PRUEBA
    # ==========================================
    print("\n6. Creando Informes de Prueba en diferentes estados...")
    
    # Informe 1 - Pendiente Secretaria
    archivo_informe_1 = SimpleUploadedFile(
        "informe_estudiante_1.pdf",
        b"Contenido del informe de practicas preprofesionales - Estudiante 1",
        content_type="application/pdf"
    )
    
    informe1, created = Informe.objects.get_or_create(
        usuario=estudiantes[0],
        titulo='Desarrollo de Sistema Web en Empresa ABC',
        defaults={
            'descripcion': 'Desarrollo de un sistema de gestión usando Django y React',
            'archivo': archivo_informe_1,
            'estado': 'pendiente_secretaria'
        }
    )
    if created:
        print(f"   ✓ Informe 1 creado: Estado = {informe1.estado}")
    
    # Informe 2 - Pendiente Presidente
    archivo_informe_2 = SimpleUploadedFile(
        "informe_estudiante_2.pdf",
        b"Contenido del informe de practicas preprofesionales - Estudiante 2",
        content_type="application/pdf"
    )
    
    informe2, created = Informe.objects.get_or_create(
        usuario=estudiantes[1],
        titulo='Análisis de Calidad de Agua en Zona Industrial',
        defaults={
            'descripcion': 'Monitoreo y análisis de parámetros de calidad de agua',
            'archivo': archivo_informe_2,
            'estado': 'pendiente_presidente',
            'escuela': escuela_ia,
            'presidente_asignado': presidente_ia,
            'secretaria_asignada': secretaria
        }
    )
    if created:
        print(f"   ✓ Informe 2 creado: Estado = {informe2.estado}")
    
    # Informe 3 - Pendiente Docente
    archivo_informe_3 = SimpleUploadedFile(
        "informe_estudiante_3.pdf",
        b"Contenido del informe de practicas preprofesionales - Estudiante 3",
        content_type="application/pdf"
    )
    
    informe3, created = Informe.objects.get_or_create(
        usuario=estudiantes[2],
        titulo='Implementación de Sistema de Inventario',
        defaults={
            'descripcion': 'Sistema de control de inventario con código de barras',
            'archivo': archivo_informe_3,
            'estado': 'pendiente_docente',
            'escuela': escuela_isi,
            'presidente_asignado': presidente_isi,
            'secretaria_asignada': secretaria,
            'docente_asignado': docente_isi_1
        }
    )
    if created:
        print(f"   ✓ Informe 3 creado: Estado = {informe3.estado}")
    
    # ==========================================
    # 7. RESUMEN
    # ==========================================
    print("\n" + "="*80)
    print("RESUMEN DE DATOS CREADOS")
    print("="*80)
    print(f"\n✓ Escuelas: {Escuela.objects.count()}")
    print(f"✓ Presidentes: {Usuario.objects.filter(rol='presidente').count()}")
    print(f"✓ Secretarias: {Usuario.objects.filter(rol='secretaria').count()}")
    print(f"✓ Docentes: {Usuario.objects.filter(rol='docente').count()}")
    print(f"✓ Estudiantes: {Usuario.objects.filter(rol='estudiante').count()}")
    print(f"✓ Bancos de Observaciones: {BancoObservacionesDocente.objects.count()}")
    print(f"✓ Informes: {Informe.objects.count()}")
    
    print("\n" + "="*80)
    print("CREDENCIALES DE ACCESO")
    print("="*80)
    print("\nSECRETARIA:")
    print("  Usuario: secretaria1")
    print("  Password: test123")
    print("  URL: /secretaria/login/")
    
    print("\nPRESIDENTES:")
    print("  Usuario: presidente_isi | Password: test123 | Escuela: ISI")
    print("  Usuario: presidente_ia  | Password: test123 | Escuela: IA")
    print("  URL: /presidente/login/")
    
    print("\nDOCENTES:")
    print("  Usuario: docente_isi_1 | Password: test123 | Escuela: ISI")
    print("  Usuario: docente_isi_2 | Password: test123 | Escuela: ISI")
    print("  Usuario: docente_ia_1  | Password: test123 | Escuela: IA")
    print("  URL: /docente/login/")
    
    print("\nESTUDIANTES:")
    print("  Usuario: 2020123456 | Password: test123")
    print("  Usuario: 2020123457 | Password: test123")
    print("  Usuario: 2020123458 | Password: test123")
    print("  Usuario: 2021234567 | Password: test123")
    print("  Usuario: 2021234568 | Password: test123")
    print("  URL: /login/")
    
    print("\n" + "="*80)
    print("DATOS DE PRUEBA POBLADOS EXITOSAMENTE")
    print("="*80)
    print("\nPuedes iniciar sesión con cualquiera de los usuarios de prueba.")
    print("El sistema está listo para probar el flujo completo v2.0.\n")


# Ejecutar la función
if __name__ == '__main__':
    crear_datos_prueba()
else:
    # Si se ejecuta desde shell
    crear_datos_prueba()
