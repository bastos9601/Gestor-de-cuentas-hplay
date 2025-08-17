#!/bin/bash
echo "🚀 Iniciando HPLAY Gestor de Cuentas..."
echo "📦 Instalando dependencias..."
pip install -r requirements.txt
echo "🔧 Configurando base de datos..."
python -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('✅ Base de datos configurada')
"
echo "🌐 Iniciando servidor..."
gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120
