# 📱 Configuración de WhatsApp Automático - HPLAY

## 🎯 Funcionalidad Implementada

Cuando agregues una nueva cuenta en la aplicación web, **automáticamente se enviará un WhatsApp** al cliente con todos los datos de la cuenta:

✅ **Servicio** (Netflix, Disney+, etc.)  
✅ **Cliente** (Nombre del cliente)  
✅ **N° Cliente** (Número de cliente)  
✅ **Método de Pago** (Efectivo, Yape, etc.)  
✅ **Precio** (Costo del servicio)  
✅ **Usuario** (Usuario de la cuenta)  
✅ **Contraseña** (Contraseña de la cuenta)  
✅ **Fecha de Inicio** (Cuándo empieza)  
✅ **Fecha de Fin** (Cuándo vence)  

## ⚙️ Configuración Personalizada

### **1. Editar Número de Soporte**

Abre el archivo `config.py` y cambia el número de soporte:

```python
WHATSAPP_CONFIG = {
    'numero_soporte': '+51 999 999 999',  # ← CAMBIA ESTE NÚMERO
    'tiempo_espera': 15,
    'cerrar_tab': True,
    'tiempo_cierre': 3
}
```

### **2. Personalizar Mensajes**

Puedes cambiar los mensajes que se envían:

```python
MENSAJES = {
    'nueva_cuenta': {
        'titulo': '🎬 HPLAY - Nueva Cuenta Activada 🎬',
        'saludo': '¡Hola {cliente}! Tu cuenta ha sido activada exitosamente.',
        'despedida': 'Saludos, Equipo HPLAY 🎬',
        'soporte': '📱 Para soporte: {numero_soporte}'
    }
}
```

## 🔧 Requisitos para WhatsApp

### **1. Instalar Dependencias**
```bash
pip install pywhatkit==5.4
```

### **2. Tener WhatsApp Web Abierto**
- Abre WhatsApp Web en tu navegador
- Escanea el código QR con tu celular
- **MANTÉN LA PESTAÑA ABIERTA**

### **3. Formato de Números de Teléfono**
La aplicación acepta estos formatos:
- `+51 999 999 999`
- `51 999 999 999`
- `999 999 999`
- `999999999`

## 📱 Cómo Funciona

### **1. Agregar Cuenta**
1. Llena el formulario con los datos del cliente
2. **Asegúrate de incluir el teléfono**
3. Haz clic en "Guardar Cuenta"

### **2. Envío Automático**
- Se envía WhatsApp automáticamente
- El mensaje incluye TODOS los datos de la cuenta
- Se crea una notificación del resultado

### **3. Verificación**
- Revisa la pestaña "Notificaciones" para ver el estado
- El cliente recibirá el mensaje en su WhatsApp

## 🧪 Probar el Sistema

### **Botón "Probar Verificación"**
1. En el dashboard, haz clic en "Probar Verificación"
2. Se enviará un mensaje de prueba
3. Verifica que llegue correctamente

### **Mensaje de Prueba**
```
🎬 HPLAY - Prueba de WhatsApp 🎬

Este es un mensaje de prueba para verificar que el sistema de WhatsApp funciona correctamente.

✅ Si recibes este mensaje, el sistema está funcionando perfectamente.

Saludos, Equipo HPLAY 🎬
```

## ⚠️ Solución de Problemas

### **Error: "No se pudo enviar WhatsApp"**
1. Verifica que WhatsApp Web esté abierto
2. Asegúrate de que el número sea válido
3. Revisa la consola para mensajes de error

### **Error: "Número de teléfono muy corto"**
1. El número debe tener al menos 9 dígitos
2. Incluye el código de país (+51)
3. Verifica el formato del número

### **WhatsApp no se envía**
1. Cierra y vuelve a abrir WhatsApp Web
2. Escanea el código QR nuevamente
3. Verifica que no haya bloqueos de seguridad

## 🎉 Ventajas del Sistema

✅ **Automático** - No necesitas enviar manualmente  
✅ **Completo** - Incluye todos los datos importantes  
✅ **Profesional** - Mensaje bien formateado  
✅ **Rastreable** - Historial de envíos en notificaciones  
✅ **Personalizable** - Puedes cambiar mensajes y números  
✅ **Confiable** - Funciona en segundo plano  

## 📞 Soporte

Si tienes problemas con el envío de WhatsApp:
1. Revisa las notificaciones del sistema
2. Verifica la configuración en `config.py`
3. Asegúrate de que WhatsApp Web esté funcionando
4. Prueba con el botón "Probar Verificación"

---

**¡Tu sistema HPLAY ahora envía WhatsApp automáticamente con todos los datos de las cuentas! 🎬📱**
