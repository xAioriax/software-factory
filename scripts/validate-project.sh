#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT_NAME="${1:-}"
PROJECT_DIR="$ROOT/projects/$PROJECT_NAME"

usage() {
  echo "Uso: $0 <nombre-proyecto>"
}

if [[ -z "$PROJECT_NAME" ]]; then
  usage
  exit 2
fi

if [[ ! -d "$PROJECT_DIR" ]]; then
  echo "Error: no existe $PROJECT_DIR" >&2
  exit 1
fi

missing=0

for file in index.html src/styles.css src/app.js package.json manifest.json README.md; do
  if [[ ! -f "$PROJECT_DIR/$file" ]]; then
    echo "Falta: $file" >&2
    missing=1
  fi
done

if [[ ! -s "$PROJECT_DIR/index.html" ]]; then
  echo "Error: index.html está vacío" >&2
  missing=1
fi

if ! grep -qi '<!DOCTYPE html>' "$PROJECT_DIR/index.html" 2>/dev/null; then
  echo "Error: index.html no tiene doctype HTML" >&2
  missing=1
fi

if ! grep -q '<script' "$PROJECT_DIR/index.html" 2>/dev/null; then
  echo "Advertencia: index.html no referencia JavaScript." >&2
fi

if ! grep -q '<link' "$PROJECT_DIR/index.html" 2>/dev/null; then
  echo "Advertencia: index.html no referencia CSS." >&2
fi

if command -v node >/dev/null 2>&1; then
  (cd "$PROJECT_DIR" && node -e "const fs=require('fs'); JSON.parse(fs.readFileSync('package.json','utf8')); JSON.parse(fs.readFileSync('manifest.json','utf8')); console.log('JSON OK')")
else
  echo "Advertencia: node no está disponible; se saltea validación JSON." >&2
fi

if [[ "$missing" -ne 0 ]]; then
  exit 1
fi

echo "Validación OK para $PROJECT_NAME"
