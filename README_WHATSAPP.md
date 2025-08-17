# 📱 Configuración de WhatsApp Automático

## 🚀 Instalación de Dependencias

Antes de usar la funcionalidad de WhatsApp, instala las librerías necesarias:

```bash
pip install -r requirements.txt
```

## ⚙️ Configuración de WhatsApp Web

### 1. Preparar WhatsApp Web
- **Abre WhatsApp Web** en tu navegador: https://web.whatsapp.com
- **Escanea el código QR** con tu teléfono
- **Mantén la pestaña abierta** y **NO la cierres**
- **Asegúrate de que esté conectado** (debe mostrar "Conectado")

### 2. Configurar Números de Teléfono
- **Formato recomendado:** 999888777 (sin código de país)
- **El sistema automáticamente agrega:** +51 (Perú)
- **Si quieres otro país:** Edita la línea en el código:
  ```python
  numero_telefono = '+51' + telefono  # Cambia +51 por tu código
  ```

## �� Cómo Funciona

### 📤 Mensajes Automáticos al Agregar/Editar Cuentas
- **Al agregar cuenta nueva:** Envía confirmación con TODOS los detalles
- **Al editar cuenta:** Envía información actualizada
- **Incluye:** Servicio, cliente, correo, contraseña, fechas, método de pago

### ⏰ Verificación Automática de Vencimientos
- **Se ejecuta cada 24 horas** automáticamente
- **Verifica cuentas próximas a vencer** (3 días antes)
- **Envía recordatorios automáticos** por WhatsApp
- **Marca cuentas vencidas** cuando expiran

### 📱 Mensajes Automáticos por Tipo
- **Cuenta nueva:** "¡CUENTA ACTIVADA EXITOSAMENTE!"
- **Cuenta editada:** "¡CUENTA ACTUALIZADA EXITOSAMENTE!"
- **Recordatorio:** "Tu cuenta vence en X días"
- **Vencimiento:** "TU CUENTA HA VENCIDO"

## 🧪 Pruebas y Verificación

### Botón "🧪 Probar Verificación"
- **Ejecuta la verificación inmediatamente**
- **No espera 24 horas**
- **Perfecto para probar la funcionalidad**
- **Muestra logs en la consola**

### Botón "📱 Enviar WhatsApp"
- **Envía mensaje manual** a cuenta seleccionada
- **Útil para contacto general** con clientes
- **Verifica que el número esté configurado**

### Botón "📤 Reenviar Info"
- **Reenvía información completa** de cuenta seleccionada
- **Incluye todos los detalles** (correo, contraseña, fechas)
- **Perfecto para recordar** datos a clientes

## 📋 Requisitos del Sistema

### Software
- **Python 3.7+**
- **Navegador web** (Chrome recomendado)
- **WhatsApp Web** funcionando

### Hardware
- **Conexión a internet estable**
- **Teléfono con WhatsApp** para escanear QR
- **Monitor** para mantener WhatsApp Web abierto

## 🚨 Solución de Problemas

### WhatsApp no se abre
- **Verifica que WhatsApp Web esté conectado**
- **Revisa que la pestaña esté abierta**
- **Asegúrate de que el código QR esté escaneado**

### Mensajes no se envían
- **Verifica el formato del número de teléfono**
- **Asegúrate de que el número sea válido**
- **Revisa los logs en la consola**

### Error de pywhatkit
- **Reinstala la librería:** `pip install --upgrade pywhatkit`
- **Verifica la versión:** `pip show pywhatkit`
- **Asegúrate de tener Chrome instalado**

## 📊 Monitoreo

### Logs en Consola
- **Verificación automática:** Cada 24 horas
- **Mensajes enviados:** Confirmación de envío
- **Errores:** Detalles de problemas

### Archivo de Notificaciones
- **`notificaciones.json`:** Historial completo
- **Estado de envío:** Enviado, Fallido, Manual
- **Fecha y hora:** De cada notificación

## 🔒 Seguridad

### Datos del Cliente
- **Números de teléfono** se almacenan localmente
- **Mensajes** se registran para auditoría
- **No se comparten** con terceros

### Verificación
- **Solo envía a números configurados**
- **Valida formato** antes de enviar
- **Maneja errores** de forma segura

## 💡 Consejos de Uso

### Para Mejor Funcionamiento
1. **Mantén WhatsApp Web abierto** siempre
2. **Verifica números** antes de agregar cuentas
3. **Prueba la funcionalidad** con el botón de prueba
4. **Revisa logs** regularmente para monitorear

### Personalización
- **Edita mensajes** en las funciones de WhatsApp
- **Cambia códigos de país** según tu ubicación
- **Ajusta tiempos** de espera si es necesario

## 📞 Soporte

Si tienes problemas:
1. **Revisa los logs** en la consola
2. **Verifica la configuración** de WhatsApp Web
3. **Prueba con el botón** de verificación manual
4. **Revisa el archivo** de notificaciones

---

**¡Con esta configuración, tu gestor de cuentas enviará mensajes de WhatsApp automáticamente con TODA la información de las cuentas!** 🎉 