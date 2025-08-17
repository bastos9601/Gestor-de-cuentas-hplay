@echo off
title HPLAY - Instalador de Aplicación Web
color 0A

echo.
echo ========================================
echo    INSTALADOR HPLAY - APLICACIÓN WEB
echo ========================================
echo.

echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python no está instalado
    echo Por favor instala Python 3.8 o superior desde python.org
    pause
    exit /b 1
)

echo ✅ Python detectado
echo.

echo Instalando dependencias...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ ERROR: No se pudieron instalar las dependencias
    echo Verifica tu conexión a internet y permisos de administrador
    pause
    exit /b 1
)

echo ✅ Dependencias instaladas correctamente
echo.

echo ========================================
echo    INSTALACIÓN COMPLETADA EXITOSAMENTE
echo ========================================
echo.
echo 🎉 ¡Tu aplicación web HPLAY está lista!
echo.
echo 📋 INFORMACIÓN IMPORTANTE:
echo - Usuario por defecto: admin
echo - Contraseña: admin123
echo - La aplicación se ejecutará en: http://localhost:5000
echo.
echo 🚀 Para iniciar la aplicación:
echo 1. Ejecuta: python app.py
echo 2. Abre tu navegador en: http://localhost:5000
echo 3. Inicia sesión con admin/admin123
echo.
echo 🌐 Para acceder desde otros dispositivos:
echo - Asegúrate de que estén en la misma red WiFi
echo - Usa la IP de tu computadora: http://[TU_IP]:5000
echo.
echo Presiona cualquier tecla para iniciar la aplicación...
pause >nul

echo.
echo Iniciando aplicación web...
start http://localhost:5000
python app.py
