@echo off
title HPLAY - Instalador del Gestor de Cuentas
color 0A

echo.
echo ========================================
echo    INSTALADOR HPLAY - GESTOR DE CUENTAS
echo ========================================
echo.

echo Verificando archivos...
if not exist "GestorCuentasHPLAY.exe" (
    echo ❌ ERROR: No se encontró el ejecutable principal
    echo Asegúrate de que todos los archivos estén en la misma carpeta
    pause
    exit /b 1
)

if not exist "config.json" (
    echo ❌ ERROR: No se encontró el archivo de configuración
    echo Asegúrate de que todos los archivos estén en la misma carpeta
    pause
    exit /b 1
)

echo ✅ Todos los archivos están presentes
echo.

echo Creando acceso directo en el escritorio...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Gestor HPLAY.lnk'); $Shortcut.TargetPath = '%CD%\GestorCuentasHPLAY.exe'; $Shortcut.WorkingDirectory = '%CD%'; $Shortcut.Description = 'Gestor de Cuentas Streaming HPLAY'; $Shortcut.Save()"

if exist "%USERPROFILE%\Desktop\Gestor HPLAY.lnk" (
    echo ✅ Acceso directo creado en el escritorio
) else (
    echo ⚠️ No se pudo crear el acceso directo automáticamente
    echo Puedes crear uno manualmente
)

echo.
echo ========================================
echo    INSTALACIÓN COMPLETADA EXITOSAMENTE
echo ========================================
echo.
echo 🎉 ¡Tu Gestor de Cuentas HPLAY está listo!
echo.
echo 📋 INFORMACIÓN IMPORTANTE:
echo - Clave por defecto: admin123
echo - Puedes cambiar la clave desde la aplicación
echo - Todos los archivos deben permanecer en esta carpeta
echo.
echo 🚀 Para usar la aplicación:
echo 1. Haz doble clic en "GestorCuentasHPLAY.exe"
echo 2. O usa el acceso directo del escritorio
echo.
echo Presiona cualquier tecla para abrir la aplicación...
pause >nul

echo.
echo Abriendo la aplicación...
start "" "GestorCuentasHPLAY.exe"

echo.
echo ¡Disfruta de tu Gestor de Cuentas HPLAY! 🎬
pause
