# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=['.'],
    binaries=[],
    datas=[('.env', '.')],
    hiddenimports=[
        'altgraph',
        'blinker',
        'certifi',
        'cffi',
        'charset_normalizer',
        'click',
        'colorama',
        'cryptography',
        'Deprecated',
        'flask',
        'flask_cors',
        'idna',
        'importlib_metadata',
        'itsdangerous',
        'jinja2',
        'markupsafe',
        'packaging',
        'pefile',
        'pycparser',
        'PyGithub',
        'pyinstaller',
        'pyinstaller_hooks_contrib',
        'PyJWT',
        'PyNaCl',
        'python_dotenv',
        'pywin32_ctypes',
        'requests',
        'typing_extensions',
        'urllib3',
        'waitress',
        'werkzeug',
        'wrapt',
        'zipp',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MyFlaskApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MyFlaskApp',
)