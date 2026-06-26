"""
Onboarding script: set up a new client by copying config templates.

Usage:
    python3 scripts/setup_cliente.py --cliente <id>
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
CLIENTES_DIR = BASE_DIR / "clientes"
ARCHIVOS = ["empresa.json", "empleados.json", "turnos.json", "mensajes_por_rol.json"]


def main():
    parser = argparse.ArgumentParser(description="OpsGrid AI — Configurar nuevo cliente")
    parser.add_argument("--cliente", required=True, help="ID del cliente (ej: catering_minera_xyz)")
    args = parser.parse_args()

    cliente_id = args.cliente.lower().replace(" ", "_")
    destino = CLIENTES_DIR / cliente_id

    if destino.exists():
        print(f"El cliente '{cliente_id}' ya existe en {destino}")
        sys.exit(0)

    destino.mkdir(parents=True)

    for nombre in ARCHIVOS:
        origen = TEMPLATES_DIR / nombre
        if not origen.exists():
            print(f"⚠️  Plantilla faltante: {origen}")
            continue
        shutil.copy(origen, destino / nombre)

    print(f"✅ Cliente '{cliente_id}' creado en: {destino}")
    print()
    print("Próximos pasos:")
    print(f"  1. Editá {destino}/empresa.json      → nombre, zona horaria, datos de la empresa")
    print(f"  2. Editá {destino}/empleados.json     → lista de empleados con WhatsApp y rol")
    print(f"  3. Editá {destino}/turnos.json        → fecha de inicio del turno A")
    print(f"  4. Editá {destino}/mensajes_por_rol.json → personalizá los mensajes si querés")
    print()
    print("Cuando esté todo listo:")
    print(f"  python3 scripts/generar_borradores.py --cliente {cliente_id}")


if __name__ == "__main__":
    main()
