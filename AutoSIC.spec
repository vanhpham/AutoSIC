# -*- mode: python ; coding: utf-8 -*-

import os
import sys

# Đường dẫn gốc của project
basedir = os.path.abspath('.')

a = Analysis(
    ['Src/main.py'],
    pathex=[basedir],
    binaries=[],
    datas=[
        ('Assets', 'Assets'),  # Thêm thư mục Assets vào build
    ],
    hiddenimports=[
        'cv2',
        'numpy',
        'PIL',
        'pyautogui',
        'keyboard',
        'tkinter',
        'tkinter.ttk',
        'tkinter.scrolledtext',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AutoSIC',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Không hiển thị console window trên Windows
    disable_windowed_traceback=False,
    icon='Assets/icon.ico' if os.path.exists('Assets/icon.ico') else None,
)
