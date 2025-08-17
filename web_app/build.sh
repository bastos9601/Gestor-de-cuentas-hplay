#!/bin/bash
echo "🚀 Iniciando build de HPLAY Gestor..."
echo "📦 Actualizando pip..."
pip install --upgrade pip

echo "🔧 Instalando dependencias..."
pip install -r requirements.txt

echo "✅ Build completado exitosamente!"
echo "📋 Dependencias instaladas:"
pip list
