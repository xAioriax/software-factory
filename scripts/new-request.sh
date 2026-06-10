#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REQUEST="$*"

if [[ -z "$REQUEST" ]]; then
  echo "Uso: $0 <pedido>"
  echo "Ejemplo: $0 crear una app de lista de tareas"
  exit 2
fi

slug="$(echo "$REQUEST" | iconv -f utf-8 -t ascii//TRANSLIT | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+|-+$//g' | cut -c1-60)"
if [[ -z "$slug" ]]; then
  slug="app-$(date +%Y%m%d%H%M%S)"
fi

mkdir -p "$ROOT/runs"
REQUEST_FILE="$ROOT/runs/request-$slug.json"

cat > "$REQUEST_FILE" <<EOF
{
  "created_at": "$(date -Iseconds)",
  "request": $(python3 -c 'import json,sys; print(json.dumps(sys.argv[1]))' "$REQUEST")
}
EOF

echo "$REQUEST_FILE"
