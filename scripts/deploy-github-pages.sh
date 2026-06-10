#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT_NAME="${1:-}"
BRANCH="${2:-gh-pages}"
PROJECT_DIR="$ROOT/projects/$PROJECT_NAME"
DIST_DIR="$PROJECT_DIR/dist"

usage() {
  echo "Uso: $0 <nombre-proyecto> [rama-gh-pages]"
  echo ""
  echo "Requiere GITHUB_TOKEN y un repo remoto ya configurado para el proyecto."
}

if [[ -z "$PROJECT_NAME" ]]; then
  usage
  exit 2
fi

if [[ -z "${GITHUB_TOKEN:-}" ]]; then
  echo "Error: falta GITHUB_TOKEN" >&2
  exit 1
fi

if [[ ! -d "$DIST_DIR" ]]; then
  echo "Error: primero corre scripts/build-static.sh $PROJECT_NAME" >&2
  exit 1
fi

if ! git -C "$PROJECT_DIR" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git -C "$PROJECT_DIR" init
  git -C "$PROJECT_DIR" config user.name "Hermes Software Factory"
  git -C "$PROJECT_DIR" config user.email "software-factory@local"
fi

git -C "$PROJECT_DIR" fetch origin "$BRANCH" >/dev/null 2>&1 || true

current_branch="$(git -C "$PROJECT_DIR" branch --show-current 2>/dev/null || true)"
git -C "$PROJECT_DIR" worktree add -B "$BRANCH" "$PROJECT_DIR/.gh-pages" "origin/$BRANCH" >/dev/null 2>&1 || git -C "$PROJECT_DIR" worktree add -B "$BRANCH" "$PROJECT_DIR/.gh-pages" >/dev/null 2>&1 || true

rm -rf "$PROJECT_DIR/.gh-pages"/*
cp -a "$DIST_DIR"/. "$PROJECT_DIR/.gh-pages"/

git -C "$PROJECT_DIR" -C "$PROJECT_DIR/.gh-pages" add .
if git -C "$PROJECT_DIR" -C "$PROJECT_DIR/.gh-pages" diff --cached --quiet; then
  echo "No hay cambios para publicar."
else
  git -C "$PROJECT_DIR" -C "$PROJECT_DIR/.gh-pages" commit -m "Deploy $PROJECT_NAME"
  git -C "$PROJECT_DIR" push origin "$BRANCH"
fi

echo "Publicado en la rama $BRANCH."

if [[ -n "$current_branch" ]]; then
  git -C "$PROJECT_DIR" checkout "$current_branch" >/dev/null 2>&1 || true
fi
