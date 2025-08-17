# 🚀 WhatsApp Automático con Retraso Configurable

## 📋 Descripción
Esta funcionalidad permite que cuando se agrega una nueva cuenta, se envíe automáticamente un mensaje de WhatsApp al cliente después de un tiempo de retraso configurable.

## ⚙️ Configuración
El tiempo de retraso se puede configurar en el archivo `config.py`:

```python
WHATSAPP_CONFIG = {
    'retraso_automatico': 30  # Segundos de retraso (por defecto: 30)
}
```

## 🔄 Flujo de Funcionamiento

### 1. **Agregar Cuenta**
- El usuario agrega una nueva cuenta con número de teléfono
- Se crea una notificación de "WhatsApp Programado"
- Se inicia un thread en segundo plano

### 2. **Retraso Configurable**
- El sistema espera el tiempo configurado (por defecto 30 segundos)
- Muestra logs cada 5 segundos del tiempo restante
- Permite cancelar el envío durante el retraso

### 3. **Envío Automático**
- Después del retraso, se envía el WhatsApp automáticamente
- Se crea una notificación del resultado (Exitoso/Fallido)

## 📱 Mensaje Enviado
El mensaje incluye:
- 🎬 Título de HPLAY
- 👤 Información del cliente
- 📺 Detalles del servicio
- 🔑 Credenciales de acceso
- 📅 Fechas de inicio y fin
- 📱 Información de soporte

## 🎯 Características

### ✅ **Funcionalidades**
- Retraso configurable (por defecto 30 segundos)
- Envío automático en segundo plano
- Logs detallados del proceso
- Notificaciones de estado
- Posibilidad de cancelar durante el retraso

### 🔧 **Configuración**
- Tiempo de retraso personalizable
- Mensajes personalizables
- Número de soporte configurable

### 📊 **Monitoreo**
- Dashboard muestra WhatsApp programados
- Notificaciones de estado
- Logs en consola para debugging

## 🚫 Cancelación
Los usuarios pueden cancelar WhatsApp programado:
- Ruta: `/cancelar_whatsapp_programado/<notif_id>`
- Solo funciona durante el retraso
- Actualiza el estado a "Cancelado por usuario"

## 📝 Logs de Debug
El sistema muestra logs detallados:
- Inicio del proceso
- Tiempo restante cada 5 segundos
- Estado del envío
- Resultado final

## 🔍 Solución de Problemas

### **WhatsApp no se envía:**
1. Verificar que el teléfono esté configurado
2. Revisar logs en consola
3. Verificar notificaciones en dashboard

### **Error de configuración:**
1. Verificar archivo `config.py`
2. Asegurar que `retraso_automatico` esté definido
3. Reiniciar la aplicación

### **Problemas de base de datos:**
1. Verificar que las tablas estén creadas
2. Revisar permisos de escritura
3. Verificar conexión a la base de datos

## 🎉 Beneficios
- ✅ Envío automático sin intervención manual
- ⏱️ Tiempo configurable para preparación
- 📱 Mensajes profesionales y consistentes
- 🔄 Proceso en segundo plano
- 📊 Monitoreo completo del estado
- 🚫 Posibilidad de cancelación

## 🔮 Futuras Mejoras
- [ ] Interfaz para cambiar tiempo de retraso
- [ ] Programación de envíos a horas específicas
- [ ] Plantillas de mensajes personalizables
- [ ] Historial de WhatsApp enviados
- [ ] Estadísticas de envíos exitosos/fallidos
