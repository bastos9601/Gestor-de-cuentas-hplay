#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar el envío de WhatsApp
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app import enviar_whatsapp, WHATSAPP_CONFIG, MENSAJES
    print("✅ Módulos importados correctamente")
    print(f"🔧 Configuración WhatsApp: {WHATSAPP_CONFIG}")
    print(f"📱 Mensajes disponibles: {list(MENSAJES.keys())}")
    
    # Número de prueba (cambia este número por uno real)
    numero_prueba = "936185088"  # Número de ejemplo
    
    # Mensaje de prueba
    mensaje_prueba = """🎬 *HPLAY - Prueba de WhatsApp* 🎬

Este es un mensaje de prueba para verificar que el sistema funciona correctamente.

✅ Si recibes este mensaje, el sistema está funcionando perfectamente.

Saludos, Equipo HPLAY 🎬"""
    
    print(f"\n🔍 Iniciando prueba de WhatsApp...")
    print(f"📱 Número: {numero_prueba}")
    print(f"💬 Mensaje: {mensaje_prueba[:100]}...")
    
    # Intentar enviar WhatsApp
    resultado = enviar_whatsapp(numero_prueba, mensaje_prueba)
    
    if resultado:
        print("✅ WhatsApp enviado exitosamente")
    else:
        print("❌ Error enviando WhatsApp")
        
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
except Exception as e:
    print(f"❌ Error general: {e}")
    import traceback
    traceback.print_exc()
