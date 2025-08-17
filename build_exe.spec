# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['gestor_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.json', '.'),
        ('clave.key', '.'),
        ('cuentas.enc', '.'),
        ('notificaciones.json', '.'),
        ('PyWhatKit_DB.txt', '.'),
        ('README_WHATSAPP.md', '.')
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.messagebox',
        'tkinter.simpledialog',
        'cryptography.fernet',
        'pywhatkit',
        'threading',
        'json',
        'os',
        'datetime',
        'time'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GestorCuentasHPLAY',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
    version='file_version_info.txt',
    uac_admin=False,
    uac_uiaccess=False,
)
