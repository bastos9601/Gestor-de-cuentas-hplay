#!/usr/bin/env python3
"""
Archivo de inicialización para Render
Configura variables de entorno ANTES de importar cualquier módulo
"""

import os
import sys

print("🚀 Inicializando entorno de Render...")

# Configurar variables de entorno críticas
os.environ['DISPLAY'] = ':0'
os.environ['RENDER'] = 'true'
os.environ['PYTHONPATH'] = os.getcwd()

# Configurar variables para evitar errores de PyWhatKit
os.environ['PYAUTOGUI_SAFEMODE'] = 'true'
os.environ['PYAUTOGUI_FAILSAFE'] = 'false'

print("✅ Variables de entorno configuradas:")
print(f"   - DISPLAY: {os.environ.get('DISPLAY', 'No definido')}")
print(f"   - RENDER: {os.environ.get('RENDER', 'No definido')}")
print(f"   - PYTHONPATH: {os.environ.get('PYTHONPATH', 'No definido')}")

# Verificar que estamos en Render
if 'RENDER' in os.environ:
    print("🎯 Detectado entorno de Render")
else:
    print("💻 Entorno local detectado")

print("🚀 Entorno inicializado correctamente")
