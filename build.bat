@echo off
echo ========================================
echo    CONSTRUYENDO EJECUTABLE HPLAY
echo ========================================
echo.

echo Limpiando archivos anteriores...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del "*.spec"

echo.
echo Construyendo ejecutable con PyInstaller...
pyinstaller --onefile --windowed --name="GestorCuentasHPLAY" --add-data "config.json;." --add-data "clave.key;." --add-data "cuentas.enc;." --add-data "notificaciones.json;." --add-data "PyWhatKit_DB.txt;." --add-data "README_WHATSAPP.md;." gestor_gui.py

echo.
echo ========================================
echo    CONSTRUCCION COMPLETADA
echo ========================================
echo.
echo El ejecutable se encuentra en: dist\GestorCuentasHPLAY.exe
echo.
echo Presiona cualquier tecla para abrir la carpeta...
pause >nul
explorer dist
