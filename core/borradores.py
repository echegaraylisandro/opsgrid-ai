"""
Generates the daily draft file for a given client.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import pytz

from .config_loader import cargar_config_cliente
from .mensajes import generar_mensajes, fecha_local, mensaje_consulta_turno
from .turnos import turno_activo

BASE_DIR = Path(__file__).parent.parent


def generar_borradores(cliente_id: str) -> Path:
    """
    Generate the draft message file for today. Returns the path to the file.
    """
    config = cargar_config_cliente(cliente_id)
    empresa = config["empresa"]

    zona = empresa.get("zona_horaria", "America/Argentina/Buenos_Aires")
    tz = pytz.timezone(zona)
    ahora = datetime.now(tz)

    fecha = fecha_local(zona)
    turno_hoy = turno_activo(config["turnos"], zona)

    borradores_dir = BASE_DIR / "borradores" / cliente_id
    borradores_dir.mkdir(parents=True, exist_ok=True)

    bloques = []
    bloques.append("=" * 60)
    bloques.append(f"BORRADORES DEL DÍA — {empresa.get('nombre', cliente_id)}")
    bloques.append(f"Fecha: {fecha}")
    turno_label = turno_hoy.upper().replace("_", " ") if turno_hoy else "NO CONFIGURADO"
    bloques.append(f"Turno activo: {turno_label}")
    bloques.append("=" * 60)
    bloques.append("")
    bloques.append(
        "Instrucciones: copiá cada mensaje y pegalo en el chat de WhatsApp "
        "del contacto indicado. Revisá lo que haga falta antes de enviar."
    )
    bloques.append("")

    if turno_hoy is None:
        supervisores = [
            e for e in config["empleados"]
            if e.get("rol") in ("gerente_operativo", "supervisor_turno", "jefe_operaciones")
            and e.get("activo", True)
            and "COMPLETAR" not in e.get("whatsapp", "COMPLETAR")
        ]
        if supervisores:
            s = supervisores[0]
            bloques.append("-" * 60)
            bloques.append(f"Para: {s['nombre']} {s.get('apellido', '')} | {s['whatsapp']}")
            bloques.append("(Consulta de turno activo)")
            bloques.append("-" * 60)
            bloques.append(mensaje_consulta_turno(config))
            bloques.append("")

    mensajes = generar_mensajes(config)
    if not mensajes:
        bloques.append("No hay mensajes para enviar hoy.")
    else:
        for m in mensajes:
            emp = m["empleado"]
            nombre_completo = f"{emp['nombre']} {emp.get('apellido', '')}".strip()
            bloques.append("-" * 60)
            bloques.append(f"Para: {nombre_completo} | {m['whatsapp']}")
            bloques.append("-" * 60)
            bloques.append(m["mensaje"])
            bloques.append("")

    contenido = "\n".join(bloques)

    timestamp = ahora.strftime("%Y-%m-%d_%H-%M")
    archivo = borradores_dir / f"borradores_{timestamp}.txt"
    archivo.write_text(contenido, encoding="utf-8")

    return archivo
