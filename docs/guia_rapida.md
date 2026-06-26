# Guía Rápida — OpsGrid AI

## Alta de nuevo cliente (10 minutos)

### 1. Crear la carpeta del cliente

```bash
python3 scripts/setup_cliente.py --cliente nombre_empresa
```

Esto crea `clientes/nombre_empresa/` con los 4 archivos de configuración.

### 2. Completar `empresa.json`

```json
{
  "nombre": "Tu Empresa SRL",
  "zona_horaria": "America/Argentina/Buenos_Aires",
  "contacto_supervisor": "Juan Pérez",
  "whatsapp_supervisor": "+5492640000001",
  "sitio_operacion": "Mina XYZ"
}
```

### 3. Completar `empleados.json`

Roles disponibles:
- `gerente_operativo` — recibe informe operativo todos los días
- `gerente_comercial` — recibe informe comercial todos los días
- `gerente_administrativo` — recibe informe financiero todos los días
- `asistente_gerencia` — recibe informe de asistencia todos los días
- `jefe_turno` — recibe informe de turno (solo cuando está en campo)
- `personal_operativo` — recibe reporte diario (solo cuando está en campo)
- `personal_gastronomico` — variante para servicios de catering en mina (solo cuando está en campo)

Tipos de turno:
- `"turno": "gerencia"` → recibe mensajes TODOS los días
- `"turno": "turno_a"` o `"turno": "turno_b"` → recibe mensajes solo cuando está en campo

### 4. Completar `turnos.json`

El campo más importante es `fecha_inicio_referencia` del Turno A. 
Ponés cualquier fecha en que el Turno A haya estado (o esté) en campo. 
El sistema calcula automáticamente todos los días futuros desde ahí.

```json
{
  "tipo_turno": "7x7",
  "turno_a": {
    "jefe": "id_jefe_turno_a",
    "fecha_inicio_referencia": "2026-06-23"
  },
  "personal_turno_a": ["id_empleado_1", "id_empleado_2"]
}
```

### 5. Probar

```bash
python3 scripts/generar_borradores.py --cliente nombre_empresa
```

---

## Automatización diaria (opcional)

Para que los borradores se generen solos cada mañana sin intervención:

**Linux / VPS (cron):**
```bash
# Ejecutar a las 8:30 todos los días
crontab -e
# Agregar:
30 8 * * * OPSGRID_CLIENTE=nombre_empresa /ruta/proyecto/scripts/ejecutar_diario.sh >> /ruta/proyecto/logs/cron.log 2>&1
```

**macOS (launchd):**
Ver `setup/setup_launchd_mac.sh`

---

## Personalizar los mensajes

Editá `clientes/<id>/mensajes_por_rol.json`. 
Variables disponibles en las plantillas:
- `{nombre}` — nombre del empleado
- `{fecha}` — fecha del día en español
- `{empresa}` — nombre de la empresa

---

## Solución de problemas

**"Turno no configurado"**: revisá `fecha_inicio_referencia` en `turnos.json` — debe ser YYYY-MM-DD.

**"WhatsApp no configurado para X"**: el campo `whatsapp` del empleado dice "COMPLETAR" — completalo con el número real.

**"Rol sin plantilla"**: el rol del empleado no tiene entrada en `mensajes_por_rol.json` — agregala.
