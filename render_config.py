# Configuración específica para Render
import os

# Configurar variables de entorno para evitar errores de PyWhatKit
os.environ['DISPLAY'] = ':0'
os.environ['RENDER'] = 'true'

# Configuración de WhatsApp para entorno de servidor
WHATSAPP_CONFIG = {
    'numero_soporte': '+51 999 999 999',
    'tiempo_espera': 15,
    'cerrar_tab': True,
    'tiempo_cierre': 30,
    'modo_servidor': True  # Indica que estamos en un servidor
}

APP_CONFIG = {
    'nombre': 'HPLAY - Gestor de Cuentas',
    'version': '2.0',
    'entorno': 'Render'
}

MENSAJES = {
    'nueva_cuenta': {
        'titulo': '🎬 HPLAY - Nueva Cuenta Activada 🎬',
        'saludo': '¡Hola {cliente}! Tu cuenta ha sido activada exitosamente.',
        'despedida': 'Saludos, Equipo HPLAY 🎬',
        'soporte': '📱 Para soporte: {numero_soporte}'
    }
}
