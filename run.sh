#!/bin/bash

#######################################################
# Script de inicialización para el Generador de Laberintos
# Autor: github.com/686f6c61
# Versión: 0.2 - Abril 2025
#
# Este script automatiza el proceso de configuración del entorno
# y ejecución del juego, garantizando que todas las dependencias
# estén correctamente instaladas y gestionando posibles instancias
# duplicadas del proceso.
#######################################################

# Verificar si Python 3 está instalado
# Utilizamos command -v para comprobar si el ejecutable existe en PATH
# La redirección &> /dev/null suprime tanto la salida estándar como los errores
if ! command -v python3 &> /dev/null; then
    echo "Python 3 no está instalado. Por favor, instálalo para continuar."
    exit 1  # Código de salida 1 indica error de dependencia no satisfecha
fi

# Crear un entorno virtual en una carpeta llamada .venv si no existe
# Esta implementación es idempotente: se puede ejecutar múltiples veces
# sin efectos secundarios no deseados
if [ ! -d ".venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv .venv  # Utiliza el módulo venv de Python 3 para crear el entorno
fi

# Activar el entorno virtual
# source modifica el entorno de la shell actual para utilizar
# los binarios y librerías del entorno virtual
echo "Activando entorno virtual..."
source .venv/bin/activate

# Instalar dependencias desde requirements.txt
# El flag -r permite instalar todas las dependencias listadas en el archivo
# Esto garantiza que todas las bibliotecas necesarias estén disponibles
echo "Instalando dependencias..."
pip install -r requirements.txt

# Verificar si el juego ya se está ejecutando y, si es así, terminar el proceso
# pgrep busca procesos por su nombre o patrón en la línea de comandos
# El flag -f permite buscar en la línea de comandos completa
# || true evita que el script falle si no se encuentra ningún proceso
PROCESO=$(pgrep -f "python3 src/main.py" || true)
if [ -n "$PROCESO" ]; then  # -n comprueba si la variable no está vacía
    echo "El juego ya está en ejecución. Terminando proceso anterior..."
    kill $PROCESO  # Envía señal SIGTERM al proceso existente
    sleep 1  # Espera 1 segundo para que el proceso termine correctamente
fi

# Ejecutar el juego
# Iniciamos el programa principal con el intérprete de Python 3
# Esto garantiza que se utilice la versión correcta de Python
echo "Iniciando el generador de laberintos..."
python3 src/main.py
