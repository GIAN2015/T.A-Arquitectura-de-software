"""
Script para poblar datos iniciales del sistema
Ejecutar con: python poblar_datos_iniciales.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.reglamento.models import Reglamento
from apps.observaciones.models import BancoObservaciones
from apps.usuarios.models import Usuario
from apps.escuelas.models import Escuela

def poblar_reglamento():
    """Crear reglamento inicial"""
    if Reglamento.objects.filter(activo=True).exists():
        print("✓ Ya existe un reglamento activo")
        return
    
    contenido_reglamento = """
REGLAMENTO DE INFORMES DE PRÁCTICAS PREPROFESIONALES - UNTELS

1. ESTRUCTURA DEL INFORME
   1.1. Carátula institucional con datos completos
   1.2. Índice numerado
   1.3. Introducción (mínimo 1 página)
   1.4. Descripción de la empresa
   1.5. Actividades realizadas (detalladas)
   1.6. Conclusiones y recomendaciones
   1.7. Anexos (evidencias fotográficas, documentos)

2. FORMATO Y PRESENTACIÓN
   2.1. Tamaño: A4
   2.2. Márgenes: Superior e inferior 2.5cm, izquierdo y derecho 3cm
   2.3. Fuente: Arial 12 o Times New Roman 12
   2.4. Interlineado: 1.5
   2.5. Numeración de páginas

3. CONTENIDO ACADÉMICO
   3.1. Mínimo 20 páginas de contenido
   3.2. Redacción formal y técnica
   3.3. Sin faltas ortográficas
   3.4. Citas y referencias según normas APA
   3.5. Coherencia y cohesión textual

4. REQUISITOS ESPECÍFICOS
   4.1. Duración mínima de prácticas: 3 meses
   4.2. Constancia de prácticas adjunta
   4.3. Carta de presentación de la empresa
   4.4. Plan de actividades firmado por supervisor
    """
    
    Reglamento.objects.create(
        nombre="Reglamento de Informes PPP 2024",
        contenido=contenido_reglamento,
        activo=True
    )
    print("✓ Reglamento creado exitosamente")

def poblar_observaciones():
    """Crear banco de observaciones frecuentes"""
    if BancoObservaciones.objects.exists():
        print("✓ Ya existen observaciones en el banco")
        return
    
    observaciones = [
        # Carátula
        {
            "seccion": "Carátula",
            "descripcion": "Falta el logo oficial de la UNTELS"
        },
        {
            "seccion": "Carátula",
            "descripcion": "Datos incompletos del estudiante (falta código o escuela profesional)"
        },
        {
            "seccion": "Carátula",
            "descripcion": "Falta el nombre completo del asesor"
        },
        
        # Formato
        {
            "seccion": "Formato",
            "descripcion": "Márgenes incorrectos, no cumplen con lo especificado (3cm izq/der, 2.5cm sup/inf)"
        },
        {
            "seccion": "Formato",
            "descripcion": "Fuente incorrecta o tamaño inadecuado (debe ser Arial o Times 12)"
        },
        {
            "seccion": "Formato",
            "descripcion": "Interlineado incorrecto (debe ser 1.5)"
        },
        {
            "seccion": "Formato",
            "descripcion": "Falta numeración de páginas"
        },
        
        # Índice
        {
            "seccion": "Índice",
            "descripcion": "Índice sin numeración de páginas"
        },
        {
            "seccion": "Índice",
            "descripcion": "Índice desactualizado, no coincide con el contenido"
        },
        
        # Introducción
        {
            "seccion": "Introducción",
            "descripcion": "Introducción muy breve (menos de 1 página)"
        },
        {
            "seccion": "Introducción",
            "descripcion": "No presenta objetivos de las prácticas"
        },
        
        # Descripción de empresa
        {
            "seccion": "Descripción de Empresa",
            "descripcion": "Descripción incompleta de la empresa (falta misión, visión o actividad principal)"
        },
        {
            "seccion": "Descripción de Empresa",
            "descripcion": "No especifica el área donde realizó las prácticas"
        },
        
        # Actividades
        {
            "seccion": "Actividades Realizadas",
            "descripcion": "Descripción muy general de las actividades, falta detalle técnico"
        },
        {
            "seccion": "Actividades Realizadas",
            "descripcion": "No relaciona las actividades con su formación profesional"
        },
        {
            "seccion": "Actividades Realizadas",
            "descripcion": "Falta cronograma o línea de tiempo de actividades"
        },
        
        # Conclusiones
        {
            "seccion": "Conclusiones",
            "descripcion": "Conclusiones muy breves o poco fundamentadas"
        },
        {
            "seccion": "Conclusiones",
            "descripcion": "No presenta recomendaciones"
        },
        
        # Anexos
        {
            "seccion": "Anexos",
            "descripcion": "Faltan evidencias fotográficas de las actividades"
        },
        {
            "seccion": "Anexos",
            "descripcion": "No adjunta constancia de prácticas"
        },
        {
            "seccion": "Anexos",
            "descripcion": "Imágenes de baja calidad o sin pie de foto"
        },
        
        # Redacción
        {
            "seccion": "Redacción",
            "descripcion": "Múltiples errores ortográficos detectados"
        },
        {
            "seccion": "Redacción",
            "descripcion": "Redacción informal o coloquial, debe ser técnico-profesional"
        },
        {
            "seccion": "Redacción",
            "descripcion": "Falta coherencia entre párrafos"
        },
        
        # Referencias
        {
            "seccion": "Referencias",
            "descripcion": "Referencias bibliográficas no siguen formato APA"
        },
        {
            "seccion": "Referencias",
            "descripcion": "Citas en el texto sin referencia bibliográfica"
        },
    ]
    
    for obs in observaciones:
        BancoObservaciones.objects.create(**obs)
    
    print(f"✓ {len(observaciones)} observaciones agregadas al banco")

def crear_usuarios_demo():
    """Crear usuarios de demostración"""
    # Migrar códigos antiguos a los nuevos (evita duplicados en despliegues ya poblados)
    renombres = {
        'DOCENTE001': 'docente_isi_1',
        'SECRETARIA001': 'secretaria1',
        'PRESIDENTE001': 'presidente_isi',
    }
    for codigo_viejo, codigo_nuevo in renombres.items():
        if Usuario.objects.filter(codigo=codigo_viejo).exists() and not Usuario.objects.filter(codigo=codigo_nuevo).exists():
            Usuario.objects.filter(codigo=codigo_viejo).update(codigo=codigo_nuevo)
            print(f"✓ Usuario {codigo_viejo} renombrado a {codigo_nuevo}")

    # Escuela (requerida para vincular docente y presidente)
    escuela, _ = Escuela.objects.get_or_create(
        codigo='ISI',
        defaults={'nombre': 'Ingeniería de Sistemas e Informática'}
    )

    # Docente (requiere escuela asignada para aparecer en la lista del presidente)
    docente, creado = Usuario.objects.get_or_create(
        codigo='docente_isi_1',
        defaults={
            'nombre': 'Ing. Carlos Ramírez',
            'tipo_usuario': 'docente',
            'escuela': escuela,
            'email': 'cramirez@untels.edu.pe',
        }
    )
    if creado:
        docente.set_password('docente123')
        print("✓ Usuario docente creado: docente_isi_1 / docente123")
    elif docente.escuela_id is None:
        docente.escuela = escuela
        docente.save()
        print("✓ Usuario docente ya existía, se le asignó la escuela ISI")
    else:
        print("✓ Usuario docente ya existe")

    # Estudiante
    if not Usuario.objects.filter(codigo='2021101234').exists():
        estudiante = Usuario.objects.create(
            codigo='2021101234',
            nombre='Juan Pérez López',
            tipo_usuario='estudiante'
        )
        estudiante.set_password('estudiante123')
        print("✓ Usuario estudiante creado: 2021101234 / estudiante123")
    else:
        print("✓ Usuario estudiante ya existe")

    # Secretaria
    if not Usuario.objects.filter(codigo='secretaria1').exists():
        secretaria = Usuario.objects.create(
            codigo='secretaria1',
            nombre='Lic. Ana Torres Mendoza',
            tipo_usuario='secretaria',
            email='secretaria@untels.edu.pe',
        )
        secretaria.set_password('secretaria123')
        print("✓ Usuario secretaria creado: secretaria1 / secretaria123")
    else:
        print("✓ Usuario secretaria ya existe")

    # Presidente (requiere escuela asignada para que su panel funcione)
    presidente, creado = Usuario.objects.get_or_create(
        codigo='presidente_isi',
        defaults={
            'nombre': 'Dr. Juan Pérez García',
            'tipo_usuario': 'presidente',
            'escuela': escuela,
            'email': 'presidente.isi@untels.edu.pe',
        }
    )
    if creado:
        presidente.set_password('presidente123')
        print("✓ Usuario presidente creado: presidente_isi / presidente123")
    elif presidente.escuela_id is None:
        presidente.escuela = escuela
        presidente.save()
        print("✓ Usuario presidente ya existía, se le asignó la escuela ISI")
    else:
        print("✓ Usuario presidente ya existe")

if __name__ == '__main__':
    print("\n" + "="*60)
    print("POBLANDO DATOS INICIALES DEL SISTEMA")
    print("="*60 + "\n")
    
    print("1. Creando reglamento...")
    poblar_reglamento()
    
    print("\n2. Creando banco de observaciones...")
    poblar_observaciones()
    
    print("\n3. Creando usuarios de demostración...")
    crear_usuarios_demo()
    
    print("\n" + "="*60)
    print("✓ PROCESO COMPLETADO EXITOSAMENTE")
    print("="*60)
    print("\nCredenciales de acceso:")
    print("\nDOCENTE:")
    print("  URL: http://127.0.0.1:8000/docente/login/")
    print("  Código: docente_isi_1")
    print("  Contraseña: docente123")
    print("\nESTUDIANTE:")
    print("  URL: http://127.0.0.1:8000/")
    print("  Código: 2021101234")
    print("  Contraseña: estudiante123")
    print("\nSECRETARIA:")
    print("  URL: http://127.0.0.1:8000/secretaria/login/")
    print("  Código: secretaria1")
    print("  Contraseña: secretaria123")
    print("\nPRESIDENTE:")
    print("  URL: http://127.0.0.1:8000/presidente/login/")
    print("  Código: presidente_isi")
    print("  Contraseña: presidente123")
    print("\n" + "="*60 + "\n")
