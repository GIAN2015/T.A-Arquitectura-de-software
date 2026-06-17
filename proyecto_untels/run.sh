#!/bin/bash
# Script de ayuda para ejecutar el proyecto

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Activar entorno virtual
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo -e "${YELLOW}⚠️  Entorno virtual no encontrado. Creando...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

# Función para mostrar menú
show_menu() {
    echo ""
    echo -e "${GREEN}=== Sistema de Validación UNTELS ===${NC}"
    echo "1) Iniciar servidor de desarrollo"
    echo "2) Ejecutar tests"
    echo "3) Ejecutar migraciones"
    echo "4) Crear superusuario"
    echo "5) Recopilar archivos estáticos"
    echo "6) Abrir shell de Django"
    echo "7) Limpiar base de datos y reiniciar"
    echo "8) Salir"
    echo ""
}

# Loop del menú
while true; do
    show_menu
    read -p "Selecciona una opción: " option
    
    case $option in
        1)
            echo -e "${GREEN}Iniciando servidor...${NC}"
            python manage.py runserver
            ;;
        2)
            echo -e "${GREEN}Ejecutando tests...${NC}"
            python manage.py test --verbosity=2
            ;;
        3)
            echo -e "${GREEN}Aplicando migraciones...${NC}"
            python manage.py makemigrations
            python manage.py migrate
            ;;
        4)
            echo -e "${GREEN}Creando superusuario...${NC}"
            python manage.py createsuperuser
            ;;
        5)
            echo -e "${GREEN}Recopilando archivos estáticos...${NC}"
            python manage.py collectstatic --noinput
            ;;
        6)
            echo -e "${GREEN}Abriendo shell...${NC}"
            python manage.py shell
            ;;
        7)
            echo -e "${YELLOW}⚠️  ADVERTENCIA: Esto eliminará todos los datos${NC}"
            read -p "¿Estás seguro? (s/n): " confirm
            if [ "$confirm" = "s" ]; then
                rm -f db.sqlite3
                find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
                find . -path "*/migrations/*.pyc" -delete
                python manage.py makemigrations
                python manage.py migrate
                echo -e "${GREEN}Base de datos reiniciada${NC}"
            fi
            ;;
        8)
            echo -e "${GREEN}¡Hasta luego!${NC}"
            exit 0
            ;;
        *)
            echo -e "${YELLOW}Opción inválida${NC}"
            ;;
    esac
done
