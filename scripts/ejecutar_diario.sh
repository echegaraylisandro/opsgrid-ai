#!/bin/bash
# Wrapper for daily execution via cron or launchd.
# Set OPSGRID_CLIENTE in the cron/launchd job or export it here.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

if [ -z "$OPSGRID_CLIENTE" ]; then
    echo "ERROR: OPSGRID_CLIENTE no definido. Editá este script o exportá la variable."
    exit 1
fi

cd "$PROJECT_DIR"
python3 scripts/generar_borradores.py --cliente "$OPSGRID_CLIENTE"
