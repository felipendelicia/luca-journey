#!/usr/bin/env bash
#
# setup.sh — Preparador del entorno del Curso de Python con Pokémon 🔴⚪
#
# Este script:
#   1. Verifica que tengas Python 3.10 o superior.
#   2. Crea un entorno virtual (venv) para aislar las dependencias.
#   3. Instala las librerías necesarias (requests, flask, pytest).
#
# Cómo usarlo:
#   bash setup.sh
#
# Está comentado línea por línea para que entiendas qué hace cada parte.
# (¡La semana 2 te enseña a escribir scripts como este!)

# 'set -e' hace que el script se detenga si algún comando falla.
# Así no seguimos adelante con un error a medias.
set -e

# Colores para que los mensajes se vean lindos en la terminal.
# \033[...m son "códigos de escape" que cambian el color del texto.
VERDE='\033[0;32m'
ROJO='\033[0;31m'
AMARILLO='\033[1;33m'
AZUL='\033[0;34m'
SIN_COLOR='\033[0m'  # Vuelve al color normal.

# Función para imprimir títulos bonitos.
titulo() {
    echo -e "${AZUL}========================================${SIN_COLOR}"
    echo -e "${AZUL} $1${SIN_COLOR}"
    echo -e "${AZUL}========================================${SIN_COLOR}"
}

titulo "🔴⚪ Setup del Curso de Python con Pokémon"

# ----------------------------------------------------------------------
# PASO 1: Buscar un Python válido.
# ----------------------------------------------------------------------
# Algunos sistemas usan 'python3', otros 'python'. Probamos cuál existe.
echo -e "${AMARILLO}➤ Buscando Python en tu sistema...${SIN_COLOR}"

PYTHON_CMD=""
# 'command -v' devuelve la ruta de un comando si existe; si no, no devuelve nada.
if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
else
    # Si no encontramos ninguno, avisamos y cortamos.
    echo -e "${ROJO}✗ No se encontró Python instalado.${SIN_COLOR}"
    echo -e "${ROJO}  Instalalo desde https://www.python.org/downloads/${SIN_COLOR}"
    echo -e "${ROJO}  En Ubuntu/Debian: sudo apt install python3 python3-venv python3-pip${SIN_COLOR}"
    exit 1
fi

echo -e "${VERDE}✓ Python encontrado: usando '$PYTHON_CMD'${SIN_COLOR}"

# ----------------------------------------------------------------------
# PASO 2: Verificar que sea 3.10 o superior.
# ----------------------------------------------------------------------
echo -e "${AMARILLO}➤ Verificando la versión de Python (necesitamos 3.10+)...${SIN_COLOR}"

# Le pedimos a Python que nos diga su versión y compare contra 3.10.
# Si la versión es vieja, Python sale con código 1 y el 'if' lo detecta.
if $PYTHON_CMD -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)'; then
    # Mostramos la versión exacta para que el usuario la vea.
    VERSION=$($PYTHON_CMD --version)
    echo -e "${VERDE}✓ Versión OK: $VERSION${SIN_COLOR}"
else
    VERSION=$($PYTHON_CMD --version)
    echo -e "${ROJO}✗ Tu versión es $VERSION, pero necesitás Python 3.10 o superior.${SIN_COLOR}"
    echo -e "${ROJO}  Actualizá Python antes de seguir.${SIN_COLOR}"
    exit 1
fi

# ----------------------------------------------------------------------
# PASO 3: Crear el entorno virtual (venv).
# ----------------------------------------------------------------------
# Un 'venv' es una cajita aislada donde se instalan las librerías del curso,
# sin ensuciar el Python de tu sistema. (Lo ves en detalle en la semana 10.)
echo -e "${AMARILLO}➤ Creando el entorno virtual en la carpeta 'venv'...${SIN_COLOR}"

if [ -d "venv" ]; then
    # Si la carpeta 'venv' ya existe, no la recreamos.
    echo -e "${VERDE}✓ Ya existe un venv. Lo reutilizamos.${SIN_COLOR}"
else
    $PYTHON_CMD -m venv venv
    echo -e "${VERDE}✓ Entorno virtual creado.${SIN_COLOR}"
fi

# ----------------------------------------------------------------------
# PASO 4: Activar el venv e instalar las dependencias.
# ----------------------------------------------------------------------
echo -e "${AMARILLO}➤ Activando el venv e instalando dependencias...${SIN_COLOR}"

# 'source' activa el entorno virtual en esta sesión del script.
# A partir de acá, 'pip' y 'python' apuntan al venv.
# shellcheck disable=SC1091
source venv/bin/activate

# Actualizamos pip (el instalador de paquetes) a la última versión.
pip install --upgrade pip >/dev/null

# Instalamos las librerías que el curso usa en las semanas finales y proyectos.
pip install requests flask pytest

echo -e "${VERDE}✓ Dependencias instaladas.${SIN_COLOR}"

# ----------------------------------------------------------------------
# ¡Listo!
# ----------------------------------------------------------------------
titulo "🎉 ¡Setup completo, Entrenador!"
echo ""
echo -e "Para empezar a trabajar, activá el entorno cada vez con:"
echo -e "  ${VERDE}source venv/bin/activate${SIN_COLOR}"
echo ""
echo -e "Para correr los tests:"
echo -e "  ${VERDE}pytest${SIN_COLOR}"
echo ""
echo -e "Cuando termines, desactivás el entorno con:"
echo -e "  ${VERDE}deactivate${SIN_COLOR}"
echo ""
echo -e "${AZUL}¡A atraparlos a todos! 🔴⚪${SIN_COLOR}"
