#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 /path/to/new-repo"
  exit 1
fi

target_dir="$1"

if [[ -e "$target_dir" && -n "$(find "$target_dir" -mindepth 1 -maxdepth 1 2>/dev/null)" ]]; then
  echo "Target directory '$target_dir' already exists and is not empty."
  exit 1
fi

mkdir -p "$target_dir"

# Copy backend API package and project docs.
cp -R backend "$target_dir/backend"
cp README.md "$target_dir/README.md"
cp .gitignore "$target_dir/.gitignore" 2>/dev/null || true

# Add backend runtime files if they exist.
[[ -f backend/requirements.txt ]] && cp backend/requirements.txt "$target_dir/backend/requirements.txt"
[[ -f backend/.env.example ]] && cp backend/.env.example "$target_dir/backend/.env.example"

(
  cd "$target_dir"
  git init -b main >/dev/null
  git add .
  git commit -m "Initial import of blood-smear backend and docs" >/dev/null
)

echo "New repository created at: $target_dir"
echo "Next step: add a remote and push"
