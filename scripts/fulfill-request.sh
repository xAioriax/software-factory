#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REQUEST_FILE="${1:-}"
PROJECT_NAME="${2:-}"

if [[ -z "$REQUEST_FILE" || -z "$PROJECT_NAME" ]]; then
  echo "Uso: $0 <request-json> <nombre-proyecto>"
  exit 2
fi

if [[ ! -f "$REQUEST_FILE" ]]; then
  echo "Error: no existe $REQUEST_FILE" >&2
  exit 1
fi

REQUEST="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8"))["request"])' "$REQUEST_FILE")"

python3 "$ROOT/scripts/generate-app.py" "$REQUEST" "$PROJECT_NAME" >/dev/null
"$ROOT/scripts/validate-project.sh" "$PROJECT_NAME"
"$ROOT/scripts/build-static.sh" "$PROJECT_NAME"

echo "Proyecto listo: $PROJECT_NAME"
