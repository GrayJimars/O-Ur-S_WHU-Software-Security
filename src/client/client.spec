# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs
from PyInstaller.utils.hooks import copy_metadata

block_cipher = None

# 收集数据文件
datas = [
    ('client.ui', '.'),           # 包含 UI 文件
    ('client.qrc', '.'),          # 包含资源文件
    # ('gui_icon.ico', '.'),        # 包含图标文件（确保已转换为 .ico 格式）
    # 如果有其他资源文件，请在这里添加，例如：
    # ('resources/*.png', 'resources'),
]

# 收集 opencv 的动态库
opencv_dlls = collect_dynamic_libs('cv2')

# 收集 PyAudio 的数据文件（如果有）
pyaudio_datas = collect_data_files('PyAudio')

# 收集 pynput 的数据文件（如果有）
pynput_datas = collect_data_files('pynput')

# 合并所有数据文件
datas += opencv_dlls + pyaudio_datas + pynput_datas

# 收集隐藏导入
hidden_imports = [
    'PyQt5',
    'PyQt5.QtCore',
    'PyQt5.QtGui',
    'PyQt5.QtWidgets',
    'PyQt5.sip',
    'qasync',
    'cv2',  # OpenCV
    'pyaudio',
    'pynput',
    # 如果有其他动态导入的模块，请在这里添加
]

# 收集 PyQt5 的资源文件
pyqt5_datas = collect_data_files('PyQt5')
datas += pyqt5_datas

a = Analysis(
    ['client.py'],
    pathex=['.'],  # 当前目录
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# 如果有需要包含的二进制文件，可以在这里添加
binaries = a.binaries

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='O-Ur-S_WHU-Software-Security',  # 可执行文件名称
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # 对于 GUI 应用，设置为 False 以隐藏控制台
    # icon='gui_icon.ico',  # 设置应用程序图标
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='O-Ur-S_WHU-Software-Security',  # 最终生成的文件夹名称
)
