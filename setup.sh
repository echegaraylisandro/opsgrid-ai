#!/bin/bash
set -e

echo "=== OpsGrid AI — Instalación ==="
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "ERROR: Python 3 no encontrado. Instalalo desde https://python.org"
    exit 1
fi

PYTHON_VER=$(python3 -c "import sys; print(sys.version_info.minor)")
if [ "$PYTHON_VER" -lt 10 ]; then
    echo "ERROR: Se requiere Python 3.10 o superior."
    exit 1
fi

# Install dependencies
echo "Instalando dependencias Python..."
pip3 install -r requirements.txt --quiet

# Create required directories
mkdir -p clientes borradores logs

echo ""
echo "✅ Instalación completada."
echo ""
echo "Próximos pasos:"
echo "  1. Creá tu primer cliente:"
echo "     python3 scripts/setup_cliente.py --cliente nombre_empresa"
echo ""
echo "  2. Completá los 4 archivos JSON en clientes/nombre_empresa/"
echo ""
echo "  3. Generá los borradores del día:"
echo "     python3 scripts/generar_borradores.py --cliente nombre_empresa"
