#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Clear screen and show a beautiful header
clear || true
echo "=========================================================="
echo "          ModelFit - Gestor de Compatibilidad de IA        "
echo "=========================================================="
echo "Configurando el entorno de ejecución..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 no está instalado. Por favor instálalo e intenta de nuevo."
    exit 1
fi

# Determine project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
cd "$PROJECT_DIR"

# Check if virtual environment exists, if not, create it
if [ ! -d ".venv" ]; then
    echo "Creando entorno virtual (.venv)..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activando entorno virtual..."
source .venv/bin/activate

# Install/upgrade dependencies
echo "Instalando dependencias desde requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

echo "=========================================================="
echo "Servidor listo. Iniciando aplicación..."
echo "Abre tu navegador en: http://127.0.0.1:5000"
echo "Presiona Ctrl+C para detener el servidor."
echo "=========================================================="

# Run the Flask app
python app.py
