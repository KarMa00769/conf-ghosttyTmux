#!/bin/sh
set -eu
project_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if ! command -v python3 >/dev/null 2>&1; then
  printf '%s\n' 'Se necesita Python 3. Instálalo con: brew install python' >&2
  exit 1
fi
exec python3 "$project_dir/scripts/install.py" "$@"
