"""
Shift rotation logic. Supports 7x7, 14x14, and custom N-day cycles.
"""
from __future__ import annotations

from datetime import date, datetime
import pytz


def turno_activo(config_turnos: dict, zona_horaria: str = "America/Argentina/Buenos_Aires") -> str | None:
    """
    Returns the active shift key ('turno_a' or 'turno_b') for today,
    or None if the reference date is not configured yet.
    """
    tipo = config_turnos.get("tipo_turno", "7x7")
    turno_a_cfg = config_turnos.get("turno_a", {})
    fecha_ref_str = turno_a_cfg.get("fecha_inicio_referencia", "")

    if not fecha_ref_str or "COMPLETAR" in fecha_ref_str:
        print(
            "⚠️  Fecha de referencia del Turno A no configurada.\n"
            "   Editá turnos.json y completá 'fecha_inicio_referencia' (formato YYYY-MM-DD)."
        )
        return None

    try:
        fecha_inicio_a = date.fromisoformat(fecha_ref_str)
    except ValueError:
        print(f"⚠️  Formato de fecha inválido: '{fecha_ref_str}'. Usá YYYY-MM-DD.")
        return None

    tz = pytz.timezone(zona_horaria)
    hoy = datetime.now(tz).date()
    dias = (hoy - fecha_inicio_a).days

    if tipo == "7x7":
        duracion, ciclo = 7, 14
    elif tipo == "14x14":
        duracion, ciclo = 14, 28
    else:
        ciclo = int(config_turnos.get("dias_ciclo", 14))
        duracion = ciclo // 2

    posicion = dias % ciclo
    return "turno_a" if posicion < duracion else "turno_b"


def empleados_en_turno(config_turnos: dict, turno: str) -> list[str]:
    """Returns list of employee IDs assigned to the given shift."""
    if turno == "turno_a":
        jefe = config_turnos.get("turno_a", {}).get("jefe", "")
        personal = config_turnos.get("personal_turno_a", [])
    elif turno == "turno_b":
        jefe = config_turnos.get("turno_b", {}).get("jefe", "")
        personal = config_turnos.get("personal_turno_b", [])
    else:
        return []

    return ([jefe] if jefe else []) + personal


def dias_para_cambio(config_turnos: dict, zona_horaria: str = "America/Argentina/Buenos_Aires") -> int:
    """Days until next shift change. Returns -1 if not configured."""
    tipo = config_turnos.get("tipo_turno", "7x7")
    fecha_ref_str = config_turnos.get("turno_a", {}).get("fecha_inicio_referencia", "")

    if not fecha_ref_str or "COMPLETAR" in fecha_ref_str:
        return -1

    try:
        fecha_inicio_a = date.fromisoformat(fecha_ref_str)
    except ValueError:
        return -1

    tz = pytz.timezone(zona_horaria)
    hoy = datetime.now(tz).date()
    dias = (hoy - fecha_inicio_a).days

    if tipo == "7x7":
        duracion, ciclo = 7, 14
    elif tipo == "14x14":
        duracion, ciclo = 14, 28
    else:
        ciclo = int(config_turnos.get("dias_ciclo", 14))
        duracion = ciclo // 2

    posicion = dias % ciclo
    return (duracion - posicion - 1) if posicion < duracion else (ciclo - posicion - 1)
