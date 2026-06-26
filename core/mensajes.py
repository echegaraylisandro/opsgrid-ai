"""
Message generation engine — role-based, date-aware, multi-tenant.
"""
from __future__ import annotations

from datetime import datetime
import pytz

from .turnos import turno_activo, empleados_en_turno

DIAS_ES = {
    "Monday": "lunes", "Tuesday": "martes", "Wednesday": "miércoles",
    "Thursday": "jueves", "Friday": "viernes", "Saturday": "sábado", "Sunday": "domingo",
}
MESES_ES = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril", 5: "mayo", 6: "junio",
    7: "julio", 8: "agosto", 9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre",
}


def fecha_local(zona_horaria: str) -> str:
    tz = pytz.timezone(zona_horaria)
    ahora = datetime.now(tz)
    dia = DIAS_ES[ahora.strftime("%A")]
    return f"{dia} {ahora.day} de {MESES_ES[ahora.month]} de {ahora.year}"


def _construir_mensaje(plantilla: dict, nombre: str, fecha: str, empresa: str) -> str:
    ctx = {"nombre": nombre, "fecha": fecha, "empresa": empresa}
    lineas = [
        plantilla["saludo"].format(**ctx),
        "",
        plantilla["intro"].format(**ctx),
        "",
        "Por favor informame:",
        "",
    ]
    for item in plantilla.get("items", []):
        lineas.append(item.format(**ctx))
    lineas.append("")
    lineas.append(plantilla["cierre"].format(**ctx))
    return "\n".join(lineas)


def generar_mensajes(config: dict) -> list[dict]:
    """
    Generate all daily messages for a client.
    Returns list of {empleado, whatsapp, mensaje} dicts.
    """
    empresa = config["empresa"]
    empleados_lista = config["empleados"]
    config_turnos = config["turnos"]
    plantillas = config["mensajes"]

    zona = empresa.get("zona_horaria", "America/Argentina/Buenos_Aires")
    nombre_empresa = empresa.get("nombre", "")

    fecha = fecha_local(zona)
    turno_hoy = turno_activo(config_turnos, zona)
    ids_en_turno = empleados_en_turno(config_turnos, turno_hoy) if turno_hoy else []

    resultado = []

    for emp in empleados_lista:
        if not emp.get("activo", True):
            continue

        turno_emp = emp.get("turno", "")
        rol = emp.get("rol", "")

        if turno_emp == "gerencia":
            debe_recibir = True
        elif turno_hoy is None:
            continue
        else:
            debe_recibir = emp["id"] in ids_en_turno

        if not debe_recibir:
            continue

        if rol not in plantillas:
            print(f"⚠️  Rol '{rol}' sin plantilla de mensaje: {emp['nombre']}")
            continue

        whatsapp = emp.get("whatsapp", "")
        if not whatsapp or "COMPLETAR" in whatsapp:
            print(f"⚠️  WhatsApp no configurado: {emp['nombre']}")
            continue

        mensaje = _construir_mensaje(plantillas[rol], emp["nombre"], fecha, nombre_empresa)
        resultado.append({"empleado": emp, "whatsapp": whatsapp, "mensaje": mensaje})

    return resultado


def mensaje_consulta_turno(config: dict) -> str:
    """Generate the daily shift-confirmation message for the operations manager."""
    empresa = config["empresa"]
    nombre_empresa = empresa.get("nombre", "")

    supervisores = [
        e for e in config["empleados"]
        if e.get("rol") in ("gerente_operativo", "supervisor_turno", "jefe_operaciones")
        and e.get("activo", True)
    ]

    nombre = supervisores[0]["nombre"] if supervisores else "Hola"

    return (
        f"Buenos días, {nombre}! 👋\n\n"
        f"Soy de administración de {nombre_empresa}. "
        f"¿Podés confirmarme qué turno está activo hoy en campo? "
        f"Necesito saberlo para coordinar los informes del día. Gracias! 🙏"
    )
