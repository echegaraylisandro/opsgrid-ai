# OpsGrid AI

**AI Operations Automation for Mining & Oil/Gas Services Companies**

Automatización de informes diarios, gestión de turnos y comunicación operativa para empresas de servicios que trabajan en entornos mineros y de oil & gas.

---

## Qué hace

- Genera mensajes diarios personalizados por rol para todo el personal
- Maneja rotaciones de turno automáticamente (7x7, 14x14, personalizado)
- Multi-tenant: un sistema, múltiples clientes, cada uno con su configuración
- WhatsApp-nativo: borradores listos para copiar y pegar
- Integración Gmail opcional para resúmenes ejecutivos

## Inicio rápido

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar un nuevo cliente
python3 scripts/setup_cliente.py --cliente mi_empresa

# 3. Editar la configuración en clientes/mi_empresa/ (4 archivos JSON)

# 4. Generar los borradores del día
python3 scripts/generar_borradores.py --cliente mi_empresa

# 5. Ver todos los clientes configurados
python3 scripts/generar_borradores.py --listar
```

## Estructura

```
opsgrid-ai/
├── core/                    # Motor principal (genérico, multi-tenant)
│   ├── config_loader.py     # Carga la config del cliente
│   ├── turnos.py            # Lógica de rotación de turnos
│   ├── mensajes.py          # Generación de mensajes
│   └── borradores.py        # Genera el archivo de borradores
├── scripts/
│   ├── generar_borradores.py  # CLI principal
│   ├── setup_cliente.py       # Alta de nuevo cliente
│   └── ejecutar_diario.sh     # Wrapper para cron/launchd
├── templates/               # Plantillas de configuración para nuevos clientes
├── clientes/                # Un directorio por cliente (privado, en .gitignore)
│   └── ejemplo_catering_srl/ # Cliente de ejemplo con datos ficticios
├── landing/                 # Landing page del producto
└── propuesta/               # Plantilla de propuesta comercial
```

## Configuración del cliente

Cada cliente tiene 4 archivos JSON en `clientes/<id>/`:

| Archivo | Qué contiene |
|---------|-------------|
| `empresa.json` | Nombre, zona horaria, datos de contacto |
| `empleados.json` | Lista de empleados con rol, turno y WhatsApp |
| `turnos.json` | Tipo de rotación y fecha de inicio del Turno A |
| `mensajes_por_rol.json` | Plantillas de mensaje para cada rol |

## Sistemas de turno soportados

- `7x7`: 7 días en campo, 7 días de descanso
- `14x14`: 14 días en campo, 14 días de descanso
- `custom`: configurar `dias_ciclo` en `turnos.json`

## Automatización diaria

```bash
# Configurar ejecución automática en Linux (cron)
export OPSGRID_CLIENTE=mi_empresa
bash scripts/ejecutar_diario.sh
```

Para automatizar vía cron:
```
30 8 * * * OPSGRID_CLIENTE=mi_empresa /ruta/al/proyecto/scripts/ejecutar_diario.sh
```

---

Producto de [OpsGrid AI](https://opsgrid.ai) · Hecho en Argentina 🇦🇷
