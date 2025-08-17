# Configuración de HPLAY Gestor de Cuentas
# Archivo de configuración personalizable

# Configuración de WhatsApp
WHATSAPP_CONFIG = {
    'numero_soporte': '+51 936185088',  # Cambia este número por el tuyo
    'mensaje_soporte': 'Para soporte técnico, contacta a:',
    'tiempo_espera': 20,  # Segundos de espera para envío
    'cerrar_tab': True,   # Cerrar pestaña después del envío
    'tiempo_cierre': 30,   # Segundos antes de cerrar
    'retraso_automatico': 30  # Segundos de retraso para envío automático
}

# Configuración de la aplicación
APP_CONFIG = {
    'nombre': 'HPLAY - Gestor de Cuentas',
    'version': '2.0',
    'empresa': 'HPLAY',
    
    'slogan': 'Tu entretenimiento, nuestra pasión',
    'puerto': 5000,
    'host': '0.0.0.0'
}

# Configuración de la base de datos
DB_CONFIG = {
    'nombre': 'hplay_gestor.db',
    'backup_automatico': True,
    'max_cuentas': 1000
}

# Configuración de notificaciones
NOTIFICACION_CONFIG = {
    'verificacion_automatica': True,
    'intervalo_verificacion': 3600,  # Segundos (1 hora)
    'notificar_vencimientos': True,
    'dias_antes_vencimiento': 3
}

# Configuración de mensajes personalizados
MENSAJES = {
    'nueva_cuenta': {
        'titulo': '🎬 HPLAY - Nueva Cuenta Activada 🎬',
        'saludo': '¡Hola {cliente}! Tu cuenta ha sido activada exitosamente.',
        'despedida': 'Saludos, Equipo HPLAY 🎬',
        'soporte': '📱 Para soporte: {numero_soporte}'
    },
    'recordatorio': {
        'titulo': '🎬 HPLAY - Recordatorio de Cuenta 🎬',
        'mensaje': 'Tu cuenta vence pronto. Por favor, renueva tu suscripción.',
        'despedida': 'Saludos, Equipo HPLAY 🎬'
    }
}
