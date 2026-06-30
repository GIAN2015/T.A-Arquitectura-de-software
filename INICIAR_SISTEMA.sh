#!/bin/bash

set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
VENV_PYTHON="$BACKEND_DIR/venv/bin/python"

if [ ! -d "$BACKEND_DIR" ]; then
    echo "No se encontró la carpeta backend/."
    read -r -p "Presiona Enter para cerrar..."
    exit 1
fi

cd "$BACKEND_DIR"

echo "=========================================="
echo " Sistema UNTELS - Inicio Automatico"
echo "=========================================="
echo ""

if [ ! -x "$VENV_PYTHON" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
    "$VENV_PYTHON" -m pip install --upgrade pip
    "$VENV_PYTHON" -m pip install -r requirements.txt
fi

echo "Aplicando migraciones..."
"$VENV_PYTHON" manage.py migrate --noinput

echo "Verificando sistema..."
"$VENV_PYTHON" manage.py check

echo ""
echo "Servidor listo para iniciar."
echo "Estudiantes: http://127.0.0.1:8000/"
echo "Docentes:    http://127.0.0.1:8000/docente/login/"
echo ""

if command -v xdg-open >/dev/null 2>&1; then
    (sleep 3 && xdg-open "http://127.0.0.1:8000/" >/dev/null 2>&1) &
fi

exec "$VENV_PYTHON" manage.py runserver
