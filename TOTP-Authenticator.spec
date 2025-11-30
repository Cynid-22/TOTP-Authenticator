# -*- mode: python ; coding: utf-8 -*-
import sys
import os
import customtkinter
from PyInstaller.utils.hooks import collect_data_files

# Get the location of customtkinter to include its assets
ctk_path = os.path.dirname(customtkinter.__file__)

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        (os.path.join(ctk_path, 'assets'), os.path.join('customtkinter', 'assets')),
        ('assets', 'assets'),
        ('core', 'core'),
        ('ui', 'ui'),
    ],
    hiddenimports=['PIL', 'PIL._tkinter_finder'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Test frameworks
        'pytest', 'unittest', 'doctest', '_pytest', 'py',
        # Documentation and help
        'pydoc', 'pydoc_data', 'sphinx',
        # Development tools (removed 'packaging' as CustomTkinter needs it)
        'pip', 'setuptools', 'wheel', 'distutils',
        # Unused standard library modules
        'lib2to3', 'tkinter.test', 'test', 'xmlrpc',
        # Optional large modules
        'matplotlib', 'numpy', 'pandas', 'scipy',
        'IPython', 'jupyter', 'notebook',
        # Encodings we don't need (keeping common ones)
        'encodings.bz2_codec', 'encodings.rot_13',
        # Other unused modules
        'pdb', 'profile', 'cProfile', 'timeit',
        'asyncio', 'concurrent', 'multiprocessing',
        'email', 'ftplib', 'telnetlib', 'poplib', 'imaplib',
        'smtplib', 'nntplib', 'http.server', 'wsgiref',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],  # No binaries bundled in EXE for one-folder mode
    exclude_binaries=True,  # Critical: exclude binaries from EXE
    name='TOTP-Authenticator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico'
)

# COLLECT step for one-folder distribution
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TOTP-Authenticator'
)
