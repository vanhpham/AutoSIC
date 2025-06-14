# -*- mode: python ; coding: utf-8 -*-

import os
import sys

# Đường dẫn gốc của project
basedir = os.path.abspath('.')
src_dir = os.path.join(basedir, 'Src')

a = Analysis(
    ['Src/main.py'],
    pathex=[basedir, src_dir],
    binaries=[],
    datas=[
        ('Assets', 'Assets'),  # Thêm thư mục Assets vào build
        ('Src/components', 'components'),  # Thêm components folder
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
        'components.ui_components',
        'components.automation_core',
        'components.stats_manager',
        'components.loop_detector',
        'components.image_detector',
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
