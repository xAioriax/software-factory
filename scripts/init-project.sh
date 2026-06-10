#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT_NAME="${1:-}"
DESCRIPTION="${2:-Proyecto generado por Software Factory}"
TEMPLATE_DIR="$ROOT/templates/static-app"
PROJECT_DIR="$ROOT/projects/$PROJECT_NAME"

usage() {
  echo "Uso: $0 <nombre-proyecto> [descripcion]"
  echo "Ejemplo: $0 tateti 'Juego de tateti 3x3'"
}

if [[ -z "$PROJECT_NAME" ]]; then
  usage
  exit 2
fi

if [[ ! "$PROJECT_NAME" =~ ^[a-z0-9][a-z0-9-]*$ ]]; then
  echo "Error: el nombre solo puede tener letras minusculas, numeros y guiones, y debe empezar con letra o numero." >&2
  exit 2
fi

if [[ -e "$PROJECT_DIR" ]]; then
  echo "Error: ya existe $PROJECT_DIR" >&2
  exit 1
fi

mkdir -p "$PROJECT_DIR"
cp -a "$TEMPLATE_DIR"/. "$PROJECT_DIR"/

cat > "$PROJECT_DIR/README.md" <<EOF
# $PROJECT_NAME

$DESCRIPTION

## Estructura

- \`index.html\`: interfaz principal.
- \`src/styles.css\`: estilos.
- \`src/app.js\`: lógica de la app.

## Desarrollo

\`\`\`bash
cd projects/$PROJECT_NAME
npm start
\`\`\`

## Build

\`\`\`bash
cd ../..
./scripts/build-static.sh $PROJECT_NAME
\`\`\`
EOF

cat > "$PROJECT_DIR/package.json" <<EOF
{
  "name": "$PROJECT_NAME",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "start": "npx serve .",
    "build": "bash ../../scripts/build-static.sh $PROJECT_NAME"
  }
}
EOF

cat > "$PROJECT_DIR/manifest.json" <<EOF
{
  "name": "$PROJECT_NAME",
  "description": "$DESCRIPTION",
  "type": "static",
  "created_by": "software-factory",
  "entrypoint": "index.html"
}
EOF

echo "$PROJECT_DIR"
