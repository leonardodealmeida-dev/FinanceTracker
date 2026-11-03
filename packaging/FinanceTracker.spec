# -*- mode: python ; coding: utf-8 -*-
# Build with:  pyinstaller packaging/FinanceTracker.spec --noconfirm
import sys
from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules

ROOT = Path(SPECPATH).parent
sys.path.insert(0, str(ROOT))
from app.version import __version__  # noqa: E402

# supabase pulls in several sub-packages that PyInstaller can miss.
hidden = ["app.bundled_config"]
for package in (
    "supabase", "supabase_auth", "gotrue", "postgrest", "realtime",
    "storage3", "supabase_functions", "httpx", "websockets",
):
    try:
        hidden += collect_submodules(package)
    except Exception:
        pass  # package not installed in this version of supabase

if sys.platform == "win32":
    icon = str(ROOT / "assets" / "icon.ico")
elif sys.platform == "darwin":
    icon = str(ROOT / "assets" / "icon.icns")
else:
    icon = str(ROOT / "assets" / "icon.png")

a = Analysis(
    [str(ROOT / "main.py")],
    pathex=[str(ROOT)],
    datas=[(str(ROOT / "assets" / "icon.png"), "assets")],
    hiddenimports=hidden,
    excludes=["tkinter", "matplotlib", "PIL", "pytest"],
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,   # one-folder build: faster start, fewer AV flags
    name="FinanceTracker",
    console=False,           # no terminal window
    icon=icon,
)
coll = COLLECT(
    exe, a.binaries, a.datas,
    name="FinanceTracker",
)

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
