# 🚀 HPLAY - Gestor de Cuentas para Vercel

## 📋 Descripción
Aplicación web Flask para gestionar cuentas de servicios de streaming, con envío automático de WhatsApp y dashboard responsive.

## 🛠️ Tecnologías
- **Backend:** Flask + SQLAlchemy
- **Frontend:** HTML + CSS + JavaScript + Bootstrap
- **Base de datos:** SQLite
- **WhatsApp:** PyWhatKit
- **Despliegue:** Vercel

## 📁 Estructura del Proyecto
```
web_app/
├── app.py                 # Aplicación principal Flask
├── wsgi.py               # Archivo WSGI para Vercel
├── vercel.json           # Configuración de Vercel
├── requirements-vercel.txt # Dependencias para Vercel
├── templates/            # Plantillas HTML
├── static/              # Archivos estáticos (CSS, JS, imágenes)
└── instance/            # Base de datos SQLite
```

## 🚀 Despliegue en Vercel

### **Paso 1: Preparar el Repositorio**
1. Asegúrate de que todos los archivos estén en la carpeta `web_app/`
2. Haz commit y push de los cambios a GitHub

### **Paso 2: Conectar con Vercel**
1. Ve a [vercel.com](https://vercel.com) y crea una cuenta
2. Haz clic en "New Project"
3. Importa tu repositorio de GitHub
4. Selecciona la carpeta `web_app/`

### **Paso 3: Configuración Automática**
Vercel detectará automáticamente que es una aplicación Flask gracias a:
- `vercel.json` - Configuración del proyecto
- `requirements-vercel.txt` - Dependencias Python
- `wsgi.py` - Punto de entrada WSGI

### **Paso 4: Variables de Entorno (Opcional)**
Si necesitas configuraciones específicas, agrega variables de entorno en Vercel:
- `FLASK_ENV=production`
- `SECRET_KEY=tu_clave_secreta`

### **Paso 5: Desplegar**
1. Haz clic en "Deploy"
2. Vercel construirá y desplegará tu aplicación
3. Obtendrás una URL como: `https://tu-app.vercel.app`

## 🔧 Configuración del Proyecto

### **Archivos Clave:**
- **`vercel.json`** - Configuración de rutas y build
- **`requirements-vercel.txt`** - Dependencias mínimas para producción
- **`wsgi.py`** - Punto de entrada para servidores WSGI

### **Base de Datos:**
- La aplicación usa SQLite que se crea automáticamente
- Los datos se almacenan en `instance/hplay_gestor.db`
- **Nota:** En Vercel, la base de datos se reinicia en cada deploy

## 📱 Características
- ✅ Dashboard responsive para móviles
- ✅ Gestión completa de cuentas
- ✅ Envío automático de WhatsApp
- ✅ Sistema de notificaciones
- ✅ Estadísticas en tiempo real
- ✅ Búsqueda y filtrado
- ✅ Interfaz moderna y intuitiva

## 🚨 Limitaciones de Vercel
- **Base de datos:** SQLite se reinicia en cada deploy
- **Archivos:** No hay almacenamiento persistente
- **Procesos en segundo plano:** No disponibles en Vercel

## 💡 Soluciones Recomendadas
Para una aplicación en producción, considera:
- **Base de datos:** PostgreSQL (Supabase, PlanetScale)
- **Almacenamiento:** AWS S3, Cloudinary
- **Procesos en segundo plano:** Celery + Redis

## 🔄 Actualizaciones
Para actualizar tu aplicación:
1. Haz cambios en tu repositorio local
2. Haz commit y push a GitHub
3. Vercel detectará automáticamente los cambios
4. Se desplegará la nueva versión automáticamente

## 📞 Soporte
Si tienes problemas con el despliegue:
1. Revisa los logs en Vercel
2. Verifica que todos los archivos estén en la carpeta correcta
3. Asegúrate de que las dependencias estén en `requirements-vercel.txt`

---
**¡Tu aplicación HPLAY estará disponible en la web en minutos! 🎉**
