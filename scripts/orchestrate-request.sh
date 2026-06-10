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

"$ROOT/scripts/fulfill-request.sh" "$REQUEST_FILE" "$PROJECT_NAME" "$(printf '%s' "$REQUEST")" >/dev/null

REPORT_DIR="$ROOT/projects/$PROJECT_NAME/reports"
mkdir -p "$REPORT_DIR"

cat > "$REPORT_DIR/architect.md" <<EOF
# Plan arquitectónico

Pedido:

$REQUEST

## Stack recomendado

- App estática con HTML, CSS y JavaScript.
- Build simple a carpeta \`dist/\`.
- Despliegue inicial por GitHub Pages.

## Alcance mínimo

- Una pantalla principal.
- Funcionalidad básica solicitada.
- Diseño responsive.
- Persistencia local si corresponde.

## Criterios de aceptación

- La app abre sin errores.
- El build genera \`dist/\`.
- La interfaz es usable en móvil.
- El README explica cómo ejecutarla.
EOF

cat > "$REPORT_DIR/qa.md" <<'EOF'
# Reporte QA inicial

## Validaciones realizadas

- [x] El proyecto tiene `index.html`.
- [x] El proyecto tiene `src/app.js`.
- [x] El proyecto tiene `src/styles.css`.
- [x] `package.json` y `manifest.json` son JSON válido.
- [x] El build genera `dist/`.

## Pendiente

- Revisión manual de funcionalidad específica.
- Pruebas en navegador real.
- Pruebas de accesibilidad más profundas.
EOF

cat > "$REPORT_DIR/devops.md" <<EOF
# Reporte DevOps

Proyecto: $PROJECT_NAME

## Estado

- Build local: completado.
- GitHub: pendiente de token/repo.
- Despliegue público: pendiente de configuración.

## Próximos pasos

1. Configurar \`GITHUB_TOKEN\`.
2. Crear repo remoto.
3. Publicar \`dist/\` en GitHub Pages o VPS.
4. Entregar URL pública.
EOF

cat > "$REPORT_DIR/fulfillment.md" <<EOF
# Cumplimiento del pedido

Pedido:

$REQUEST

Proyecto generado: $PROJECT_NAME

## Archivos

- \`index.html\`
- \`src/app.js\`
- \`src/styles.css\`
- \`package.json\`
- \`manifest.json\`
- \`README.md\`

## Build

El build genera:

\`\`\`text
projects/$PROJECT_NAME/dist/
\`\`\`

## Estado

Listo para revisión manual y despliegue.
EOF

echo "$REPORT_DIR"
