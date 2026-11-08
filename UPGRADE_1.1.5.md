# FinanceTracker desktop v1.1.5 — upgrade notes

## Before replacing files
Keep a backup of your current FinanceTracker folder. Preserve your local `.env`
file (it is intentionally not included in this source package).

## Install the update
Extract this archive into the directory that contains your `FinanceTracker`
folder, allowing it to overwrite updated source files. The archive contains a
`FinanceTracker/` top-level directory.

On Linux:
```bash
cd ~/Desktop/Projects
tar -xzf FinanceTracker-pyside-1.1.5.tar.gz
cd FinanceTracker
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

If you do not already have a virtual environment, create one and install the
requirements first:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Supabase custom categories
Run `migrations/003_custom_categories.sql` once in the Supabase SQL Editor.
It is safe to re-run. This is the same `custom_categories` table used by the
FinanceTracker React website, so custom categories are shared between clients.

The existing `migrations/001_add_recurrence.sql` and
`migrations/002_rls_and_account_deletion.sql` are retained.

## Account sessions
Account passwords are never stored. Session tokens use the OS credential
store through `keyring` when a supported backend is available. If the OS
credential store is unavailable, accounts can still be used during the
current app run, but may need signing in again after restarting.
