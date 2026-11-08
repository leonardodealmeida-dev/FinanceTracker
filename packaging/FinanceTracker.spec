
# FinanceTracker - PyInstaller Specification
# Version 1.1.5

import sys
from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules

# --------------------------------------------------
# ROOT DIRECTORY
# --------------------------------------------------

ROOT = Path(SPECPATH).resolve().parent
sys.path.insert(0, str(ROOT))

from app.version import __version__  # noqa: E402

# --------------------------------------------------
# HIDDEN IMPORTS
# --------------------------------------------------

# Explicit application imports
hidden = [
    "app",
    "app.config",
    "app.version",
    "app.bundled_config",
    "app.analytics",
    "app.tutorial_state",
    "app.i18n",
    "app.auth_errors",
    "app.recurrence",
    "app.logging_setup",
    "app.services",
    "app.services.account_manager",
    "app.services.supabase_service",
    "app.ui",
    "app.ui.dashboard",
    "app.ui.login_window",
    "app.ui.reset_password",
    "app.ui.charts",
    "app.ui.theme",
    "app.ui.tutorial",
    "app.ui.settings",
    "app.database",
]

# Collect every FinanceTracker module
hidden += collect_submodules("app")

# Supabase dependencies
packages = [
    "supabase",
    "supabase_auth",
    "gotrue",
    "postgrest",
    "realtime",
    "storage3",
    "supabase_functions",
    "httpx",
    "httpcore",
    "websockets",
    "websocket",
    "keyring",
    "pydantic",
    "pydantic_core",
    "anyio",
    "h11",
    "certifi",
    "jwt",
]

for package in packages:
    try:
        hidden += collect_submodules(package)
    except Exception:
        pass

# Remove duplicates
hidden = sorted(set(hidden))

# --------------------------------------------------
# APPLICATION ICON
# --------------------------------------------------

if sys.platform == "win32":
    icon = str(ROOT / "assets" / "icon.ico")

elif sys.platform == "darwin":
    icon = str(ROOT / "assets" / "icon.icns")

else:
    icon = str(ROOT / "assets" / "icon.png")

# --------------------------------------------------
# ANALYSIS
# --------------------------------------------------

a = Analysis(
    [str(ROOT / "main.py")],
    pathex=[str(ROOT)],
    binaries=[],
    datas=[
        (str(ROOT / "assets"), "assets"),
    ],
    hiddenimports=hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "tkinter",
        "matplotlib",
        "pytest",
    ],
    noarchive=False,
)

# --------------------------------------------------
# PYZ
# --------------------------------------------------

pyz = PYZ(a.pure)

# --------------------------------------------------
# EXECUTABLE
# --------------------------------------------------

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="FinanceTracker",
    debug=False,
    strip=False,
    upx=True,
    console=False,
    icon=icon,
)

# --------------------------------------------------
# COLLECT
# --------------------------------------------------

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    name="FinanceTracker",
)

# --------------------------------------------------
# MACOS APP BUNDLE
# --------------------------------------------------

if sys.platform == "darwin":

    app = BUNDLE(
        coll,
        name="FinanceTracker.app",
        icon=icon,
        bundle_identifier="com.usaleonardo.financetracker",
        version=__version__,
        info_plist={
            "CFBundleDisplayName": "FinanceTracker",
            "CFBundleShortVersionString": __version__,
            "NSHighResolutionCapable": True,
        },
    )
