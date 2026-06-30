#!/bin/bash
# Script de deployment para Sistema de Validación de Informes v2.0
# Universidad Nacional Tecnológica de Lima Sur

set -e

echo "========================================"
echo "DEPLOYMENT - Sistema de Validación v2.0"
echo "UNTELS"
echo "========================================"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Verificar que estamos en el directorio correcto
if [ ! -f "docker-compose.production.yml" ]; then
    print_error "Este script debe ejecutarse desde el directorio raíz del proyecto"
    exit 1
fi

# Verificar que existe el archivo .env.production
if [ ! -f ".env.production" ]; then
    print_error "No se encontró el archivo .env.production"
    print_warning "Copia .env.production.example a .env.production y configúralo"
    echo "  cp .env.production.example .env.production"
    echo "  nano .env.production"
    exit 1
fi

# Verificar que Docker está instalado
if ! command -v docker &> /dev/null; then
    print_error "Docker no está instalado"
    echo "Instala Docker desde: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    print_error "Docker Compose no está instalado"
    echo "Instala Docker Compose desde: https://docs.docker.com/compose/install/"
    exit 1
fi

print_success "Verificaciones iniciales completadas"

# Función para deployment completo
full_deploy() {
    echo ""
    echo "Iniciando deployment completo..."
    echo ""
    
    # 1. Detener servicios existentes
    echo "1. Deteniendo servicios existentes..."
    docker-compose -f docker-compose.production.yml down || true
    print_success "Servicios detenidos"
    
    # 2. Crear certificado SSL autofirmado si no existe
    if [ ! -f "nginx/ssl/selfsigned.crt" ]; then
        echo ""
        echo "2. Generando certificado SSL autofirmado..."
        mkdir -p nginx/ssl
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout nginx/ssl/selfsigned.key \
            -out nginx/ssl/selfsigned.crt \
            -subj "/C=PE/ST=Lima/L=Lima/O=UNTELS/OU=IT/CN=localhost"
        print_success "Certificado SSL generado"
        print_warning "En producción, reemplaza con certificado real (Let's Encrypt)"
    else
        print_success "Certificado SSL ya existe"
    fi
    
    # 3. Construir imágenes
    echo ""
    echo "3. Construyendo imágenes Docker..."
    docker-compose -f docker-compose.production.yml build --no-cache
    print_success "Imágenes construidas"
    
    # 4. Iniciar servicios
    echo ""
    echo "4. Iniciando servicios..."
    docker-compose -f docker-compose.production.yml up -d
    print_success "Servicios iniciados"
    
    # 5. Esperar a que los servicios estén listos
    echo ""
    echo "5. Esperando a que los servicios estén listos..."
    sleep 10
    
    # 6. Verificar estado de los servicios
    echo ""
    echo "6. Verificando estado de los servicios..."
    docker-compose -f docker-compose.production.yml ps
    
    echo ""
    print_success "Deployment completado exitosamente!"
    echo ""
    echo "Los servicios están corriendo en:"
    echo "  - HTTP:  http://localhost"
    echo "  - HTTPS: https://localhost"
    echo ""
    echo "Comandos útiles:"
    echo "  - Ver logs:        docker-compose -f docker-compose.production.yml logs -f"
    echo "  - Detener:         docker-compose -f docker-compose.production.yml down"
    echo "  - Reiniciar:       docker-compose -f docker-compose.production.yml restart"
    echo "  - Ver estado:      docker-compose -f docker-compose.production.yml ps"
    echo ""
}

# Función para actualizar deployment existente
update_deploy() {
    echo ""
    echo "Actualizando deployment existente..."
    echo ""
    
    # 1. Pull últimos cambios
    echo "1. Descargando últimos cambios..."
    git pull origin main || print_warning "No se pudo hacer git pull"
    
    # 2. Reconstruir imágenes
    echo ""
    echo "2. Reconstruyendo imágenes..."
    docker-compose -f docker-compose.production.yml build
    print_success "Imágenes reconstruidas"
    
    # 3. Reiniciar servicios
    echo ""
    echo "3. Reiniciando servicios..."
    docker-compose -f docker-compose.production.yml up -d --force-recreate
    print_success "Servicios reiniciados"
    
    # 4. Limpiar imágenes antiguas
    echo ""
    echo "4. Limpiando imágenes antiguas..."
    docker image prune -f
    print_success "Limpieza completada"
    
    echo ""
    print_success "Actualización completada!"
}

# Función para crear backup de base de datos
backup_database() {
    echo ""
    echo "Creando backup de base de datos..."
    
    BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).sql"
    BACKUP_PATH="./database/backups/$BACKUP_FILE"
    
    mkdir -p ./database/backups
    
    docker-compose -f docker-compose.production.yml exec -T db pg_dump -U untels_user untels_db > "$BACKUP_PATH"
    
    if [ -f "$BACKUP_PATH" ]; then
        print_success "Backup creado: $BACKUP_PATH"
    else
        print_error "Error al crear backup"
        exit 1
    fi
}

# Función para restaurar backup
restore_database() {
    echo ""
    echo "Backups disponibles:"
    ls -lh ./database/backups/*.sql 2>/dev/null || echo "No hay backups disponibles"
    echo ""
    read -p "Ingresa el nombre del archivo de backup: " BACKUP_FILE
    
    if [ ! -f "./database/backups/$BACKUP_FILE" ]; then
        print_error "Backup no encontrado"
        exit 1
    fi
    
    print_warning "ADVERTENCIA: Esto sobrescribirá la base de datos actual"
    read -p "¿Estás seguro? (yes/no): " CONFIRM
    
    if [ "$CONFIRM" = "yes" ]; then
        docker-compose -f docker-compose.production.yml exec -T db psql -U untels_user -d untels_db < "./database/backups/$BACKUP_FILE"
        print_success "Backup restaurado"
    else
        echo "Operación cancelada"
    fi
}

# Menú principal
echo ""
echo "Selecciona una opción:"
echo ""
echo "  1) Deployment completo (primera vez)"
echo "  2) Actualizar deployment existente"
echo "  3) Crear backup de base de datos"
echo "  4) Restaurar backup"
echo "  5) Ver logs"
echo "  6) Detener servicios"
echo "  7) Reiniciar servicios"
echo "  8) Salir"
echo ""
read -p "Opción: " OPTION

case $OPTION in
    1)
        full_deploy
        ;;
    2)
        update_deploy
        ;;
    3)
        backup_database
        ;;
    4)
        restore_database
        ;;
    5)
        echo "Mostrando logs (Ctrl+C para salir)..."
        docker-compose -f docker-compose.production.yml logs -f
        ;;
    6)
        echo "Deteniendo servicios..."
        docker-compose -f docker-compose.production.yml down
        print_success "Servicios detenidos"
        ;;
    7)
        echo "Reiniciando servicios..."
        docker-compose -f docker-compose.production.yml restart
        print_success "Servicios reiniciados"
        ;;
    8)
        echo "Saliendo..."
        exit 0
        ;;
    *)
        print_error "Opción inválida"
        exit 1
        ;;
esac
