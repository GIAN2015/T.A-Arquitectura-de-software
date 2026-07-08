#!/usr/bin/env python
"""
Script simple para poblar datos iniciales
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.usuarios.models import Usuario
from apps.escuelas.models import Escuela

print("="*80)
print("POBLANDO DATOS DE PRUEBA - Sistema UNTELS")
print("="*80)

# Limpiar datos previos
print("\n1. Limpiando datos previos...")
Usuario.objects.all().delete()
Escuela.objects.all().delete()

# Crear Escuelas
print("\n2. Creando Escuelas...")
escuela_isi = Escuela.objects.create(
    codigo='ISI',
    nombre='Ingeniería de Sistemas e Informática',
    activo=True
)
print(f"   ✓ Escuela creada: {escuela_isi.nombre}")

escuela_imec = Escuela.objects.create(
    codigo='IMEC',
    nombre='Ingeniería Mecánica',
    activo=True
)
print(f"   ✓ Escuela creada: {escuela_imec.nombre}")

# Crear Presidentes
print("\n3. Creando Presidentes...")
presidente_isi = Usuario.objects.create(
    codigo='presidente_isi',
    nombre='Dr. Juan Pérez García',
    tipo_usuario='presidente',
    email='presidente.isi@untels.edu.pe',
    escuela=escuela_isi,
    activo=True
)
presidente_isi.set_password('test123')
print(f"   ✓ {presidente_isi.codigo} - {presidente_isi.nombre}")

presidente_imec = Usuario.objects.create(
    codigo='presidente_imec',
    nombre='Dra. María López Rodríguez',
    tipo_usuario='presidente',
    email='presidente.imec@untels.edu.pe',
    escuela=escuela_imec,
    activo=True
)
presidente_imec.set_password('test123')
print(f"   ✓ {presidente_imec.codigo} - {presidente_imec.nombre}")

# Actualizar escuelas con presidentes
escuela_isi.presidente = presidente_isi
escuela_isi.save()
escuela_imec.presidente = presidente_imec
escuela_imec.save()

# Crear Secretaria
print("\n4. Creando Secretaria Académica...")
secretaria = Usuario.objects.create(
    codigo='secretaria1',
    nombre='Lic. Ana Torres Mendoza',
    tipo_usuario='secretaria',
    email='secretaria@untels.edu.pe',
    activo=True
)
secretaria.set_password('test123')
print(f"   ✓ {secretaria.codigo} - {secretaria.nombre}")

# Crear Docentes
print("\n5. Creando Docentes...")
docentes_data = [
    {
        'codigo': 'docente_isi_1',
        'nombre': 'Ing. Carlos Ramírez Santos',
        'escuela': escuela_isi,
        'email': 'cramirez@untels.edu.pe'
    },
    {
        'codigo': 'docente_isi_2',
        'nombre': 'Ing. Laura Fernández Díaz',
        'escuela': escuela_isi,
        'email': 'lfernandez@untels.edu.pe'
    },
    {
        'codigo': 'docente_imec_1',
        'nombre': 'Ing. Pedro García Flores',
        'escuela': escuela_imec,
        'email': 'pgarcia@untels.edu.pe'
    },
    {
        'codigo': 'docente_imec_2',
        'nombre': 'Ing. Rosa Martínez López',
        'escuela': escuela_imec,
        'email': 'rmartinez@untels.edu.pe'
    }
]

for data in docentes_data:
    docente = Usuario.objects.create(
        codigo=data['codigo'],
        nombre=data['nombre'],
        tipo_usuario='docente',
        email=data['email'],
        escuela=data['escuela'],
        activo=True
    )
    docente.set_password('test123')
    print(f"   ✓ {docente.codigo} - {docente.nombre}")

# Crear Estudiantes
print("\n6. Creando Estudiantes...")
estudiantes_data = [
    {
        'codigo': '2020123456',
        'nombre': 'José Antonio Gonzales Rojas',
        'escuela': escuela_isi,
        'tipo': 'estudiante',
        'email': '2020123456@untels.edu.pe'
    },
    {
        'codigo': '2020123457',
        'nombre': 'María Isabel Sánchez Torres',
        'escuela': escuela_isi,
        'tipo': 'estudiante',
        'email': '2020123457@untels.edu.pe'
    },
    {
        'codigo': '2019123458',
        'nombre': 'Luis Alberto Mendoza Vargas',
        'escuela': escuela_imec,
        'tipo': 'estudiante',
        'email': '2019123458@untels.edu.pe'
    }
]

for data in estudiantes_data:
    estudiante = Usuario.objects.create(
        codigo=data['codigo'],
        nombre=data['nombre'],
        tipo_usuario=data['tipo'],
        email=data['email'],
        escuela=data['escuela'],
        activo=True
    )
    estudiante.set_password('test123')
    print(f"   ✓ {estudiante.codigo} - {estudiante.nombre}")

# Crear Egresados
print("\n7. Creando Egresados...")
egresados_data = [
    {
        'codigo': '2018123459',
        'nombre': 'Andrea Patricia Vargas Luna',
        'escuela': escuela_isi,
        'email': '2018123459@untels.edu.pe'
    },
    {
        'codigo': '2018123460',
        'nombre': 'Ricardo Manuel Torres Campos',
        'escuela': escuela_imec,
        'email': '2018123460@untels.edu.pe'
    }
]

for data in egresados_data:
    egresado = Usuario.objects.create(
        codigo=data['codigo'],
        nombre=data['nombre'],
        tipo_usuario='egresado',
        email=data['email'],
        escuela=data['escuela'],
        activo=True
    )
    egresado.set_password('test123')
    print(f"   ✓ {egresado.codigo} - {egresado.nombre}")

# Resumen
print("\n" + "="*80)
print("RESUMEN DE DATOS CREADOS")
print("="*80)
print(f"Escuelas:     {Escuela.objects.count()}")
print(f"Presidentes:  {Usuario.objects.filter(tipo_usuario='presidente').count()}")
print(f"Secretarias:  {Usuario.objects.filter(tipo_usuario='secretaria').count()}")
print(f"Docentes:     {Usuario.objects.filter(tipo_usuario='docente').count()}")
print(f"Estudiantes:  {Usuario.objects.filter(tipo_usuario='estudiante').count()}")
print(f"Egresados:    {Usuario.objects.filter(tipo_usuario='egresado').count()}")
print(f"Total:        {Usuario.objects.count()} usuarios")
print("="*80)
print("\n✅ DATOS POBLADOS EXITOSAMENTE")
print("\nCredenciales de acceso:")
print("  Usuario: [código de usuario]")
print("  Contraseña: test123")
print("\nEjemplos:")
print("  - Secretaria:     secretaria1 / test123")
print("  - Presidente ISI: presidente_isi / test123")
print("  - Docente ISI 1:  docente_isi_1 / test123")
print("  - Estudiante:     2020123456 / test123")
print("="*80)
