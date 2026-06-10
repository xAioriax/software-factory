#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT_NAME="${1:-}"
PROJECT_DIR="$ROOT/projects/$PROJECT_NAME"
DIST_DIR="$PROJECT_DIR/dist"

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

rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

cp "$PROJECT_DIR/index.html" "$DIST_DIR/index.html"
if [[ -d "$PROJECT_DIR/src" ]]; then
  mkdir -p "$DIST_DIR/src"
  cp -a "$PROJECT_DIR/src"/. "$DIST_DIR/src"/
fi

if [[ ! -s "$DIST_DIR/index.html" ]]; then
  echo "Error: no se genero index.html" >&2
  exit 1
fi

echo "$DIST_DIR"
