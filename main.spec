# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

a.datas += [('img/buttons/cadencia.png','/home/agu/Code/Dino Survivors/img/buttons/cadencia.png', "DATA")]
a.datas += [('img/buttons/continuar.png','/home/agu/Code/Dino Survivors/img/buttons/continuar.png', "DATA")]
a.datas += [('img/buttons/daño.png','/home/agu/Code/Dino Survivors/img/buttons/daño.png', "DATA")]
a.datas += [('img/buttons/empezar.png','/home/agu/Code/Dino Survivors/img/buttons/empezar.png', "DATA")]
a.datas += [('img/buttons/salir.png','/home/agu/Code/Dino Survivors/img/buttons/salir.png', "DATA")]
a.datas += [('img/buttons/volver a jugar.png','/home/agu/Code/Dino Survivors/img/buttons/volver a jugar.png', "DATA")]
a.datas += [('img/buttons/volver al menu.png','/home/agu/Code/Dino Survivors/img/buttons/volver al menu.png', "DATA")]

a.datas += [('img/enemy/moving/0.png','/home/agu/Code/Dino Survivors/img/enemy/moving/0.png', "DATA")]
a.datas += [('img/enemy/moving/1.png','/home/agu/Code/Dino Survivors/img/enemy/moving/1.png', "DATA")]
a.datas += [('img/enemy/moving/2.png','/home/agu/Code/Dino Survivors/img/enemy/moving/2.png', "DATA")]
a.datas += [('img/enemy/moving/3.png','/home/agu/Code/Dino Survivors/img/enemy/moving/3.png', "DATA")]


a.datas += [('img/icons/xp.png','/home/agu/Code/Dino Survivors/img/icons/xp.png', "DATA")]
a.datas += [('img/icons/xp2.png','/home/agu/Code/Dino Survivors/img/icons/xp2.png', "DATA")]
a.datas += [('img/icons/bullet.png','/home/agu/Code/Dino Survivors/img/icons/bullet.png', "DATA")]

a.datas += [('img/map/map.png','/home/agu/Code/Dino Survivors/img/map/map.png', "DATA")]

a.datas += [('img/menus/fondo.png','/home/agu/Code/Dino Survivors/img/menus/fondo.png', "DATA")]
a.datas += [('img/menus/ganaste.png','/home/agu/Code/Dino Survivors/img/menus/ganaste.png', "DATA")]
a.datas += [('img/menus/levelup.png','/home/agu/Code/Dino Survivors/img/menus/levelup.png', "DATA")]
a.datas += [('img/menus/perdiste.png','/home/agu/Code/Dino Survivors/img/menus/perdiste.png', "DATA")]

a.datas += [('img/player/idle/0.png','/home/agu/Code/Dino Survivors/img/player/idle/0.png', "DATA")]
a.datas += [('img/player/idle/1.png','/home/agu/Code/Dino Survivors/img/player/idle/1.png', "DATA")]
a.datas += [('img/player/idle/2.png','/home/agu/Code/Dino Survivors/img/player/idle/2.png', "DATA")]

a.datas += [('img/player/moving/0.png','/home/agu/Code/Dino Survivors/img/player/moving/0.png', "DATA")]
a.datas += [('img/player/moving/1.png','/home/agu/Code/Dino Survivors/img/player/moving/1.png', "DATA")]
a.datas += [('img/player/moving/2.png','/home/agu/Code/Dino Survivors/img/player/moving/2.png', "DATA")]

a.datas += [('img/strongie/moving/0.png','/home/agu/Code/Dino Survivors/img/strongie/moving/0.png', "DATA")]
a.datas += [('img/strongie/moving/1.png','/home/agu/Code/Dino Survivors/img/strongie/moving/1.png', "DATA")]
a.datas += [('img/strongie/moving/2.png','/home/agu/Code/Dino Survivors/img/strongie/moving/2.png', "DATA")]
a.datas += [('img/strongie/moving/3.png','/home/agu/Code/Dino Survivors/img/strongie/moving/3.png', "DATA")]
a.datas += [('img/strongie/moving/4.png','/home/agu/Code/Dino Survivors/img/strongie/moving/4.png', "DATA")]



pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='main',
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
)
