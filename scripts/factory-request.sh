#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REQUEST="${1:-}"
PROJECT_NAME="${2:-}"

if [[ -z "$REQUEST" ]]; then
  echo "Uso: $0 '<pedido de app>' [nombre-proyecto]" >&2
  echo "Ejemplo: $0 'crear una calculadora de propinas' calculadora-propinas" >&2
  exit 2
fi

cd "$ROOT"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Error: no estoy dentro de un repo Git." >&2
  exit 1
fi

if [[ -z "$(git remote get-url origin 2>/dev/null || true)" ]]; then
  echo "Error: no hay remote 'origin' configurado." >&2
  exit 1
fi

if [[ -z "$PROJECT_NAME" ]]; then
  PROJECT_NAME="$(python3 - "$REQUEST" <<'PY'
import re, sys
text = sys.argv[1].lower().strip()
replacements = {
    'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ñ': 'n', 'ü': 'u',
}
for src, dst in replacements.items():
    text = text.replace(src, dst)
text = re.sub(r'[^a-z0-9]+', '-', text)
text = re.sub(r'-+', '-', text).strip('-')[:60]
print(text or 'app')
PY
)"
fi

PROJECT_NAME="$(echo "$PROJECT_NAME" | iconv -f utf-8 -t ascii//TRANSLIT | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+|-+$//g' | cut -c1-60)"

if [[ -z "$PROJECT_NAME" ]]; then
  PROJECT_NAME="app-$(date +%Y%m%d%H%M%S)"
fi

if [[ -d "$ROOT/projects/$PROJECT_NAME" ]]; then
  PROJECT_NAME="${PROJECT_NAME}-$(date +%H%M%S)"
fi

RUN_ID="$(date +%Y%m%d%H%M%S)"
REQUEST_FILE="$ROOT/runs/request-${PROJECT_NAME}-${RUN_ID}.json"
mkdir -p "$ROOT/runs"

python3 - "$REQUEST_FILE" "$REQUEST" <<'PY'
import json, sys
path, request = sys.argv[1], sys.argv[2]
with open(path, 'w', encoding='utf-8') as f:
    json.dump({'created_at': __import__('datetime').datetime.now().isoformat(), 'request': request}, f, ensure_ascii=False, indent=2)
    f.write('\n')
PY

"$ROOT/scripts/orchestrate-request.sh" "$REQUEST_FILE" "$PROJECT_NAME" >/dev/null

git add "projects/$PROJECT_NAME" "$REQUEST_FILE"
if git diff --cached --quiet; then
  echo "No hay cambios nuevos para commitear."
else
  git commit -m "feat($PROJECT_NAME): generate app from request"
fi

git push origin main

PAGES_URL="https://xaioriax.github.io/software-factory/projects/$PROJECT_NAME/"
REPO_URL="https://github.com/xAioriax/software-factory/tree/main/projects/$PROJECT_NAME"

echo "Pedido registrado: $REQUEST_FILE"
echo "Proyecto: $PROJECT_NAME"
echo "Repo: $REPO_URL"
echo "URL esperada: $PAGES_URL"
echo "GitHub Actions puede tardar unos segundos en publicar."
