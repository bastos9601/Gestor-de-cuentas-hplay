#!/bin/bash
echo "🚀 Iniciando HPLAY Gestor de Cuentas..."

# Verificar que gunicorn esté instalado
if ! command -v gunicorn &> /dev/null; then
    echo "❌ ERROR: gunicorn no está instalado"
    echo "📦 Instalando gunicorn..."
    pip install gunicorn==21.2.0
fi

echo "🔧 Configurando base de datos..."
python -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('✅ Base de datos configurada')
"

echo "🌐 Iniciando servidor con gunicorn..."
gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120
