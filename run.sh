#!/bin/bash

# Verificar si Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "Python 3 no está instalado. Por favor, instálalo para continuar."
    exit 1
fi

# Crear un entorno virtual en una carpeta llamada .venv si no existe
if [ ! -d ".venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv .venv
fi

# Activar el entorno virtual
echo "Activando entorno virtual..."
source .venv/bin/activate

# Instalar dependencias desde requirements.txt
echo "Instalando dependencias..."
pip install -r requirements.txt

# Verificar si el juego ya se está ejecutando y, si es así, terminar el proceso
PROCESO=$(pgrep -f "python3 src/main.py" || true)
if [ -n "$PROCESO" ]; then
    echo "El juego ya está en ejecución. Terminando proceso anterior..."
    kill $PROCESO
    sleep 1
fi

# Ejecutar el juego
echo "Iniciando el generador de laberintos..."
python3 src/main.py
