#!/usr/bin/env bash
# Builds the standalone Linux app (no Python needed to run it).
#
#   ./build_linux.sh
#
# Needs: Python 3.10+, internet (to install PySide6/PyInstaller), and a
# .env file with SUPABASE_URL and SUPABASE_KEY (publishable key only).
# Output: dist/FinanceTracker-<version>-linux-x86_64.tar.gz
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -f .env ]; then
  echo "Missing .env (needs SUPABASE_URL and SUPABASE_KEY)." >&2
  exit 1
fi

python3 -m venv .venv-build
# shellcheck disable=SC1091
source .venv-build/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt pyinstaller

# Bake the Supabase settings into the app for this build only,
# then put the empty template back so the key never reaches git.
BACKUP="$(mktemp)"
cp app/bundled_config.py "$BACKUP"
trap 'cp "$BACKUP" app/bundled_config.py; rm -f "$BACKUP"' EXIT

set -a
# shellcheck disable=SC1091
source .env
set +a
python tools/write_bundled_config.py

rm -rf build dist
pyinstaller packaging/FinanceTracker.spec --noconfirm

VERSION="$(python -c 'from app.version import __version__; print(__version__)')"
cp assets/icon.png dist/FinanceTracker/icon.png
OUT="dist/FinanceTracker-${VERSION}-linux-x86_64.tar.gz"
tar -C dist -czf "$OUT" FinanceTracker

# Also make a .zip of the same folder (extract, then open "FinanceTracker").
ZIP_OUT="dist/FinanceTracker-${VERSION}-linux-x86_64.zip"
if command -v zip >/dev/null 2>&1; then
  (cd dist && zip -qr "../$ZIP_OUT" FinanceTracker)
else
  ZIP_OUT="(install 'zip' to also get a .zip)"
fi

echo
echo "Done. Run it with:   ./dist/FinanceTracker/FinanceTracker"
echo "Share ONE of these (the app + _internal folder, nothing else):"
echo "  $OUT"
echo "  $ZIP_OUT"
