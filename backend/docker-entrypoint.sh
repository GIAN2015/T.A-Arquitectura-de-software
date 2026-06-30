#!/bin/bash
# Script de entrada para el contenedor Docker
# Sistema de Validación de Informes v2.0 - UNTELS

set -e

echo "========================================"
echo "Sistema de Validación de Informes v2.0"
echo "Universidad Nacional Tecnológica de Lima Sur"
echo "========================================"

# Esperar a que la base de datos esté lista
echo ""
echo "Esperando a PostgreSQL..."
while ! nc -z ${DB_HOST:-db} ${DB_PORT:-5432}; do
    sleep 0.5
done
echo "✓ PostgreSQL está listo"

# Ejecutar migraciones
echo ""
echo "Ejecutando migraciones..."
python manage.py migrate --noinput
echo "✓ Migraciones completadas"

# Crear superusuario si no existe (solo en desarrollo)
if [ "$DJANGO_SETTINGS_MODULE" = "config.settings.development" ]; then
    echo ""
    echo "Creando superusuario de desarrollo..."
    python manage.py shell << EOF
from apps.usuarios.models import Usuario
if not Usuario.objects.filter(username='admin').exists():
    Usuario.objects.create_superuser('admin', 'admin@untels.edu.pe', 'admin123')
    print('✓ Superusuario creado: admin / admin123')
else:
    print('✓ Superusuario ya existe')
EOF
fi

# Recolectar archivos estáticos
echo ""
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput --clear
echo "✓ Archivos estáticos recolectados"

# Poblar datos de prueba si la variable está activada
if [ "$POPULATE_TEST_DATA" = "true" ]; then
    echo ""
    echo "Poblando datos de prueba..."
    python manage.py shell < scripts/poblar_datos_prueba_v2.py || echo "⚠ No se pudieron poblar datos de prueba"
fi

echo ""
echo "========================================"
echo "Iniciando servidor..."
echo "========================================"
echo ""

# Ejecutar el comando pasado como argumentos
exec "$@"
