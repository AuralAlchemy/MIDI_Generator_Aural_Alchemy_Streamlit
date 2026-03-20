# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files, collect_submodules, copy_metadata

datas = []
datas += collect_data_files("streamlit")
datas += collect_data_files("altair")
datas += copy_metadata("streamlit")
datas += [("app.py", ".")]

hiddenimports = []
hiddenimports += collect_submodules("streamlit")
hiddenimports += collect_submodules("pretty_midi")
hiddenimports += collect_submodules("mido")
hiddenimports += ["streamlit.runtime.scriptrunner.magic_funcs"]

a = Analysis(
    ["launcher.py"],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "matplotlib",
        "scipy",
        "IPython",
        "jedi",
        "tkinter",
        "pytest",
    ],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="AuralAlchemy MIDI Generator",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    icon="assets/icon.icns",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="AuralAlchemy MIDI Generator",
)

app = BUNDLE(
    coll,
    name="AuralAlchemy MIDI Generator.app",
    icon="assets/icon.icns",
    bundle_identifier="com.auralchemy.midigenerator",
)
