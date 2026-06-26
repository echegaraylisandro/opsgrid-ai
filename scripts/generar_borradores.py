"""
Generate daily WhatsApp draft messages for a specific client.

Usage:
    python3 scripts/generar_borradores.py --cliente <id>
    python3 scripts/generar_borradores.py --listar
"""
from __future__ import annotations

import argparse
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.borradores import generar_borradores
from core.config_loader import listar_clientes


def main():
    parser = argparse.ArgumentParser(
        description="OpsGrid AI — Generador de borradores diarios"
    )
    parser.add_argument("--cliente", help="ID del cliente (carpeta bajo clientes/)")
    parser.add_argument("--listar", action="store_true", help="Listar clientes configurados")
    args = parser.parse_args()

    if args.listar:
        clientes = listar_clientes()
        if not clientes:
            print("No hay clientes configurados todavía.")
            print("Ejecutá: python3 scripts/setup_cliente.py --cliente <id>")
        else:
            print("Clientes configurados:")
            for c in clientes:
                print(f"  • {c}")
        return

    cliente_id = args.cliente or os.environ.get("OPSGRID_CLIENTE")
    if not cliente_id:
        print("ERROR: Indicá el cliente con --cliente <id> o la variable OPSGRID_CLIENTE")
        sys.exit(1)

    print(f"Generando borradores para: {cliente_id}")
    archivo = generar_borradores(cliente_id)
    print(f"\nBorradores guardados en: {archivo}")
    print("\n" + "=" * 60)
    print(archivo.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
