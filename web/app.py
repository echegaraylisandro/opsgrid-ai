"""
OpsGrid AI — Panel web
Uso: python3 web/app.py
Abrir: http://localhost:5000
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from flask import Flask, redirect, render_template, url_for

from core.borradores import generar_borradores
from core.config_loader import cargar_config_cliente, listar_clientes
from core.mensajes import fecha_local, generar_mensajes
from core.turnos import dias_para_cambio, turno_activo

app = Flask(__name__, template_folder="templates")


@app.route("/")
def index():
    clientes = listar_clientes()
    if len(clientes) == 1:
        return redirect(url_for("dashboard", cliente_id=clientes[0]))
    return render_template("index.html", clientes=clientes)


@app.route("/<cliente_id>")
def dashboard(cliente_id):
    try:
        config = cargar_config_cliente(cliente_id)
    except FileNotFoundError as e:
        return f"<pre style='font-family:monospace;padding:2rem'>{e}</pre>", 404

    empresa = config["empresa"]
    zona = empresa.get("zona_horaria", "America/Argentina/Buenos_Aires")

    turno_hoy = turno_activo(config["turnos"], zona)
    dias_cambio = dias_para_cambio(config["turnos"], zona)
    fecha = fecha_local(zona)
    mensajes = generar_mensajes(config)

    turno_label = None
    if turno_hoy:
        turno_label = config["turnos"].get(turno_hoy, {}).get(
            "nombre", turno_hoy.upper().replace("_", " ")
        )

    return render_template(
        "dashboard.html",
        empresa=empresa,
        cliente_id=cliente_id,
        turno_hoy=turno_hoy,
        turno_label=turno_label,
        dias_cambio=dias_cambio,
        fecha=fecha,
        mensajes=mensajes,
        total=len(mensajes),
    )


@app.route("/<cliente_id>/generar", methods=["POST"])
def generar(cliente_id):
    generar_borradores(cliente_id)
    return redirect(url_for("dashboard", cliente_id=cliente_id))


if __name__ == "__main__":
    print("\n  OpsGrid AI corriendo en: http://localhost:8080\n")
    app.run(debug=False, port=8080, host="0.0.0.0")
