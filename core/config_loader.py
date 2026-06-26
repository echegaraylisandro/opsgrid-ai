"""
Multi-tenant configuration loader.
Each client lives under clientes/<cliente_id>/ with their own JSON files.
"""
from __future__ import annotations

import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CLIENTES_DIR = BASE_DIR / "clientes"


def cargar_config_cliente(cliente_id: str) -> dict:
    """Load all config files for a given client."""
    cliente_dir = CLIENTES_DIR / cliente_id
    if not cliente_dir.exists():
        raise FileNotFoundError(
            f"Cliente '{cliente_id}' no encontrado.\n"
            f"  Carpeta esperada: {cliente_dir}\n"
            f"  Ejecutá: python3 scripts/setup_cliente.py --cliente {cliente_id}"
        )

    def leer(nombre: str) -> dict | list:
        path = cliente_dir / nombre
        if not path.exists():
            raise FileNotFoundError(
                f"Falta '{nombre}' en la configuración del cliente '{cliente_id}'.\n"
                f"  Copiá y completá la plantilla desde templates/{nombre}"
            )
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    return {
        "empresa": leer("empresa.json"),
        "empleados": leer("empleados.json"),
        "turnos": leer("turnos.json"),
        "mensajes": leer("mensajes_por_rol.json"),
    }


def listar_clientes() -> list[str]:
    """Return list of configured client IDs."""
    if not CLIENTES_DIR.exists():
        return []
    return sorted(
        d.name for d in CLIENTES_DIR.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    )
