# -*- mode: python ; coding: utf-8 -*-
# auralalchemy.spec - Windows single-file build

import os

from PyInstaller.utils.hooks import collect_data_files, collect_submodules, copy_metadata

datas = []
datas += collect_data_files("streamlit")
datas += collect_data_files("altair")
datas += copy_metadata("streamlit")
datas += [("app.py", ".")]
datas += [(".streamlit", ".streamlit")]
datas += [("assets", "assets")]

hiddenimports = []
hiddenimports += collect_submodules("streamlit")
hiddenimports += collect_submodules("pretty_midi")
hiddenimports += collect_submodules("mido")
hiddenimports += collect_submodules("altair")
hiddenimports += [
    "streamlit.runtime.scriptrunner.magic_funcs",
    "streamlit.web.cli",
    "click",
    "numpy",
    "pandas",
    "PIL",
    "pretty_midi",
    "mido",
]

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
        "notebook",
        "jupyter",
    ],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="AuralAlchemy MIDI Generator",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    icon=os.path.join(SPECPATH, "assets", "icon.ico"),
)
