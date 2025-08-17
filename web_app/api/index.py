from app import app

# Para Vercel serverless
app.debug = False

# Exportar la aplicación para Vercel
handler = app
