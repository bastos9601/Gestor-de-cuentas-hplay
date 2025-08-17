from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
from datetime import datetime, timedelta
import threading
import time
import pywhatkit as pwk

# Importar configuración personalizada
try:
    from config import WHATSAPP_CONFIG, APP_CONFIG, MENSAJES
except ImportError:
    # Configuración por defecto si no existe el archivo
    WHATSAPP_CONFIG = {
        'numero_soporte': '+51 999 999 999',
        'tiempo_espera': 15,
        'cerrar_tab': True,
        'tiempo_cierre': 30
    }
    APP_CONFIG = {
        'nombre': 'HPLAY - Gestor de Cuentas',
        'version': '2.0'
    }
    MENSAJES = {
        'nueva_cuenta': {
            'titulo': '🎬 HPLAY - Nueva Cuenta Activada 🎬',
            'saludo': '¡Hola {cliente}! Tu cuenta ha sido activada exitosamente.',
            'despedida': 'Saludos, Equipo HPLAY 🎬',
            'soporte': '📱 Para soporte: {numero_soporte}'
        }
    }

app = Flask(__name__)
app.secret_key = 'hplay_secret_key_2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hplay_gestor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de base de datos
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    es_admin = db.Column(db.Boolean, default=False)

class Cuenta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    servicio = db.Column(db.String(100), nullable=False)
    cliente = db.Column(db.String(100), nullable=False)
    num_cliente = db.Column(db.String(50))
    metodo = db.Column(db.String(50))
    precio = db.Column(db.String(50))
    telefono = db.Column(db.String(20))
    fecha_inicio = db.Column(db.String(20))
    fecha_fin = db.Column(db.String(20))
    usuario = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    vencida = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

class Notificacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    servicio = db.Column(db.String(100), nullable=False)
    cliente = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

# Crear tablas
with app.app_context():
    db.create_all()
    
    # Crear usuario admin por defecto si no existe
    if not Usuario.query.filter_by(username='admin').first():
        admin = Usuario(
            username='admin',
            password_hash=generate_password_hash('admin123'),
            es_admin=True
        )
        db.session.add(admin)
        db.session.commit()

# Función para verificar vencimientos
def verificar_vencimientos():
    """Verifica cuentas vencidas y actualiza su estado"""
    with app.app_context():
        cuentas = Cuenta.query.all()
        for cuenta in cuentas:
            if cuenta.fecha_fin:
                try:
                    fecha_fin = datetime.strptime(cuenta.fecha_fin, '%Y-%m-%d')
                    if fecha_fin < datetime.now():
                        cuenta.vencida = True
                    else:
                        cuenta.vencida = False
                except:
                    pass
        db.session.commit()

# Función para enviar WhatsApp
def enviar_whatsapp(telefono, mensaje):
    """Envía mensaje por WhatsApp usando PyWhatKit"""
    print(f"🔍 DEBUG: Función enviar_whatsapp llamada con:")
    print(f"   - Teléfono: {telefono}")
    print(f"   - Mensaje: {mensaje[:100]}...")
    
    try:
        # Limpiar y formatear número de teléfono
        telefono_limpio = str(telefono).strip()
        print(f"🔍 DEBUG: Teléfono limpio: {telefono_limpio}")
        
        # Remover espacios, guiones y paréntesis
        telefono_limpio = ''.join(c for c in telefono_limpio if c.isdigit() or c == '+')
        print(f"🔍 DEBUG: Teléfono sin caracteres especiales: {telefono_limpio}")
        
        # Si empieza con +51, removerlo
        if telefono_limpio.startswith('+51'):
            telefono_limpio = telefono_limpio[3:]
            print(f"🔍 DEBUG: Removido +51: {telefono_limpio}")
        elif telefono_limpio.startswith('51'):
            telefono_limpio = telefono_limpio[2:]
            print(f"🔍 DEBUG: Removido 51: {telefono_limpio}")
        
        # Verificar que tenga al menos 9 dígitos
        if len(telefono_limpio) < 9:
            print(f"❌ ERROR: Número de teléfono muy corto: {telefono_limpio}")
            return False
        
        # Si no empieza con 9, agregarlo (formato peruano)
        if not telefono_limpio.startswith('9'):
            telefono_limpio = '9' + telefono_limpio
            print(f"🔍 DEBUG: Agregado 9 al inicio: {telefono_limpio}")
        
        # Formatear para envío
        numero_final = f"+51{telefono_limpio}"
        print(f"🔍 DEBUG: Número final formateado: {numero_final}")
        
        print(f"🔍 DEBUG: Iniciando envío con PyWhatKit...")
        
        # Enviar mensaje con PyWhatKit
        pwk.sendwhatmsg_instantly(
            numero_final, 
            mensaje, 
            wait_time=WHATSAPP_CONFIG.get('tiempo_espera', 15),
            tab_close=WHATSAPP_CONFIG.get('cerrar_tab', True),
            close_time=WHATSAPP_CONFIG.get('tiempo_cierre', 3)
        )
        
        print(f"✅ WhatsApp enviado exitosamente a {numero_final}")
        return True
        
    except Exception as e:
        print(f"❌ ERROR enviando WhatsApp: {e}")
        print(f"🔍 DEBUG: Tipo de error: {type(e).__name__}")
        import traceback
        print(f"🔍 DEBUG: Traceback completo:")
        traceback.print_exc()
        return False

# Rutas de la aplicación
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = Usuario.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['es_admin'] = user.es_admin
            flash('¡Bienvenido!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cuentas = Cuenta.query.all()
    total_cuentas = len(cuentas)
    
    # Obtener WhatsApp programados
    whatsapp_programados = Notificacion.query.filter(
        Notificacion.tipo == 'WhatsApp Programado - Nueva Cuenta',
        Notificacion.estado.like('Programado (%s)')
    ).all()
    
    # Estadísticas
    metodos = {}
    clientes = {}
    precio_total = 0
    cuentas_vencidas = 0
    
    for cuenta in cuentas:
        # Contar métodos
        metodo = cuenta.metodo or 'Sin método'
        metodos[metodo] = metodos.get(metodo, 0) + 1
        
        # Contar clientes
        cliente = cuenta.cliente or 'Sin cliente'
        clientes[cliente] = clientes.get(cliente, 0) + 1
        
        # Calcular precio total
        try:
            precio_str = cuenta.precio or '0'
            precio_limpio = ''.join(c for c in precio_str if c.isdigit() or c == '.')
            if precio_limpio:
                precio_total += float(precio_limpio)
        except:
            continue
        
        # Contar cuentas vencidas
        if cuenta.vencida:
            cuentas_vencidas += 1
    
    stats = {
        'total_cuentas': total_cuentas,
        'clientes_unicos': len(clientes),
        'metodos': len(metodos),
        'precio_total': f"S/. {precio_total:.2f}",
        'cuentas_vencidas': cuentas_vencidas,
        'whatsapp_programados': len(whatsapp_programados)
    }
    
    return render_template('dashboard.html', cuentas=cuentas, stats=stats, whatsapp_programados=whatsapp_programados)

@app.route('/agregar_cuenta', methods=['GET', 'POST'])
def agregar_cuenta():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        print("🔍 DEBUG: Iniciando proceso de agregar cuenta...")
        
        nueva_cuenta = Cuenta(
            servicio=request.form['servicio'],
            cliente=request.form['cliente'],
            num_cliente=request.form['num_cliente'],
            metodo=request.form['metodo'],
            precio=request.form['precio'],
            telefono=request.form['telefono'],
            fecha_inicio=request.form['fecha_inicio'],
            fecha_fin=request.form['fecha_fin'],
            usuario=request.form['usuario'],
            password=request.form['password']
        )
        
        print(f"🔍 DEBUG: Cuenta creada - Teléfono: {nueva_cuenta.telefono}")
        
        db.session.add(nueva_cuenta)
        db.session.commit()
        
        print("🔍 DEBUG: Cuenta guardada en base de datos")
        
        # ENVÍO AUTOMÁTICO DE WHATSAPP
        if nueva_cuenta.telefono:
            print(f"🔍 DEBUG: Teléfono encontrado: {nueva_cuenta.telefono}")
            print(f"🔍 DEBUG: Configuración disponible: {WHATSAPP_CONFIG}")
            print(f"🔍 DEBUG: Mensajes disponibles: {MENSAJES}")
            
            try:
                # Crear mensaje detallado usando configuración personalizada
                mensaje = f"""{MENSAJES['nueva_cuenta']['titulo']}

{MENSAJES['nueva_cuenta']['saludo'].format(cliente=nueva_cuenta.cliente)}

📺 *SERVICIO:* {nueva_cuenta.servicio}
👤 *CLIENTE:* {nueva_cuenta.cliente}
🔢 *N° CLIENTE:* {nueva_cuenta.num_cliente or 'No especificado'}
💳 *MÉTODO DE PAGO:* {nueva_cuenta.metodo or 'No especificado'}
💰 *PRECIO:* {nueva_cuenta.precio or 'No especificado'}

🔑 *ACCESO:*
• Usuario: `{nueva_cuenta.usuario}`
• Contraseña: `{nueva_cuenta.password}`

📅 *FECHAS:*
• Inicio: {nueva_cuenta.fecha_inicio or 'No especificada'}
• Fin: {nueva_cuenta.fecha_fin or 'No especificada'}

✅ Tu cuenta está lista para usar.
🎉 ¡Disfruta del servicio!

{MENSAJES['nueva_cuenta']['despedida']}
{MENSAJES['nueva_cuenta']['soporte'].format(numero_soporte=WHATSAPP_CONFIG['numero_soporte'])}"""
                
                print(f"🔍 DEBUG: Mensaje creado: {mensaje[:200]}...")
                
                # Enviar WhatsApp en segundo plano con retraso configurable
                retraso_segundos = WHATSAPP_CONFIG.get('retraso_automatico', 30)
                
                # Capturar las variables necesarias para el thread
                telefono_cuenta = nueva_cuenta.telefono
                servicio_cuenta = nueva_cuenta.servicio
                cliente_cuenta = nueva_cuenta.cliente
                
                def enviar_whatsapp_automatico():
                    try:
                        print(f"🔍 DEBUG: Esperando {retraso_segundos} segundos antes de enviar WhatsApp a {telefono_cuenta}")
                        
                        # Contador regresivo con logs cada 5 segundos
                        for i in range(retraso_segundos, 0, -1):
                            if i % 5 == 0:  # Log cada 5 segundos
                                print(f"🔍 DEBUG: Tiempo restante: {i} segundos")
                            
                            # Verificar si fue cancelado
                            try:
                                notif_actual = Notificacion.query.filter_by(
                                    servicio=servicio_cuenta,
                                    cliente=cliente_cuenta,
                                    tipo='WhatsApp Programado - Nueva Cuenta',
                                    estado=f'Programado ({retraso_segundos}s)'
                                ).first()
                                
                                if not notif_actual or notif_actual.estado != f'Programado ({retraso_segundos}s)':
                                    print("🔍 DEBUG: WhatsApp cancelado por usuario")
                                    return
                            except Exception as e:
                                print(f"🔍 DEBUG: Error verificando cancelación: {e}")
                                pass
                            
                            time.sleep(1)
                        
                        print(f"🔍 DEBUG: Iniciando envío de WhatsApp a {telefono_cuenta}")
                        resultado = enviar_whatsapp(telefono_cuenta, mensaje)
                        print(f"🔍 DEBUG: Resultado del envío: {resultado}")
                        
                        # Crear notificación del resultado
                        if resultado:
                            notif = Notificacion(
                                servicio=servicio_cuenta,
                                cliente=cliente_cuenta,
                                tipo='WhatsApp Automático - Nueva Cuenta (30s retraso)',
                                estado='Exitoso'
                            )
                        else:
                            notif = Notificacion(
                                servicio=servicio_cuenta,
                                cliente=cliente_cuenta,
                                tipo='WhatsApp Automático - Nueva Cuenta (30s retraso)',
                                estado='Fallido'
                            )
                        
                        db.session.add(notif)
                        db.session.commit()
                        print("🔍 DEBUG: Notificación guardada en base de datos")
                    except Exception as e:
                        print(f"❌ ERROR en thread de WhatsApp: {str(e)}")
                        # Crear notificación de error
                        try:
                            notif_error = Notificacion(
                                servicio=servicio_cuenta,
                                cliente=cliente_cuenta,
                                tipo='WhatsApp Automático - Nueva Cuenta',
                                estado=f'Error en thread: {str(e)}'
                            )
                            db.session.add(notif_error)
                            db.session.commit()
                        except:
                            pass
                
                # Crear notificación de WhatsApp programado
                notif_programado = Notificacion(
                    servicio=nueva_cuenta.servicio,
                    cliente=nueva_cuenta.cliente,
                    tipo='WhatsApp Programado - Nueva Cuenta',
                    estado=f'Programado ({retraso_segundos}s)'
                )
                db.session.add(notif_programado)
                db.session.commit()
                
                # Ejecutar en segundo plano
                thread = threading.Thread(target=enviar_whatsapp_automatico)
                thread.start()
                print(f"🔍 DEBUG: Thread de WhatsApp iniciado con retraso de {retraso_segundos}s")
                
                flash(f'Cuenta agregada exitosamente. WhatsApp se enviará automáticamente a {nueva_cuenta.telefono} en {retraso_segundos} segundos.', 'success')
                
            except Exception as e:
                print(f"❌ ERROR en envío automático: {str(e)}")
                # Si falla el WhatsApp, solo mostrar error en la notificación
                notif = Notificacion(
                    servicio=nueva_cuenta.servicio,
                    cliente=nueva_cuenta.cliente,
                    tipo='WhatsApp Automático - Nueva Cuenta',
                    estado=f'Error: {str(e)}'
                )
                db.session.add(notif)
                db.session.commit()
                
                flash(f'Cuenta agregada exitosamente, pero hubo un error enviando WhatsApp: {str(e)}', 'warning')
        else:
            print("🔍 DEBUG: No hay teléfono, no se envía WhatsApp")
            flash('Cuenta agregada exitosamente (sin envío de WhatsApp - no hay teléfono)', 'success')
        
        return redirect(url_for('dashboard'))
    
    return render_template('agregar_cuenta.html')

@app.route('/editar_cuenta/<int:id>', methods=['GET', 'POST'])
def editar_cuenta(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cuenta = Cuenta.query.get_or_404(id)
    
    if request.method == 'POST':
        cuenta.servicio = request.form['servicio']
        cuenta.cliente = request.form['cliente']
        cuenta.num_cliente = request.form['num_cliente']
        cuenta.metodo = request.form['metodo']
        cuenta.precio = request.form['precio']
        cuenta.telefono = request.form['telefono']
        cuenta.fecha_inicio = request.form['fecha_inicio']
        cuenta.fecha_fin = request.form['fecha_fin']
        cuenta.usuario = request.form['usuario']
        cuenta.password = request.form['password']
        
        db.session.commit()
        flash('Cuenta actualizada exitosamente', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('editar_cuenta.html', cuenta=cuenta)

@app.route('/eliminar_cuenta/<int:id>')
def eliminar_cuenta(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cuenta = Cuenta.query.get_or_404(id)
    db.session.delete(cuenta)
    db.session.commit()
    
    flash('Cuenta eliminada exitosamente', 'success')
    return redirect(url_for('dashboard'))

@app.route('/buscar_cuentas')
def buscar_cuentas():
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'})
    
    termino = request.args.get('q', '').lower()
    
    if not termino:
        cuentas = Cuenta.query.all()
    else:
        cuentas = Cuenta.query.filter(
            db.or_(
                Cuenta.servicio.ilike(f'%{termino}%'),
                Cuenta.cliente.ilike(f'%{termino}%'),
                Cuenta.num_cliente.ilike(f'%{termino}%'),
                Cuenta.metodo.ilike(f'%{termino}%'),
                Cuenta.usuario.ilike(f'%{termino}%')
            )
        ).all()
    
    resultado = []
    for cuenta in cuentas:
        resultado.append({
            'id': cuenta.id,
            'servicio': cuenta.servicio,
            'cliente': cuenta.cliente,
            'num_cliente': cuenta.num_cliente,
            'metodo': cuenta.metodo,
            'precio': cuenta.precio,
            'telefono': cuenta.telefono,
            'fecha_inicio': cuenta.fecha_inicio,
            'fecha_fin': cuenta.fecha_fin,
            'usuario': cuenta.usuario,
            'password': cuenta.password,
            'vencida': cuenta.vencida
        })
    
    return jsonify(resultado)

@app.route('/cambiar_clave', methods=['GET', 'POST'])
def cambiar_clave():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        clave_actual = request.form['clave_actual']
        nueva_clave = request.form['nueva_clave']
        confirmar_clave = request.form['confirmar_clave']
        
        user = Usuario.query.get(session['user_id'])
        
        if not check_password_hash(user.password_hash, clave_actual):
            flash('Clave actual incorrecta', 'error')
        elif nueva_clave != confirmar_clave:
            flash('Las claves no coinciden', 'error')
        else:
            user.password_hash = generate_password_hash(nueva_clave)
            db.session.commit()
            flash('Clave cambiada exitosamente', 'success')
            return redirect(url_for('dashboard'))
    
    return render_template('cambiar_clave.html')

# NUEVAS FUNCIONALIDADES

@app.route('/verificar_vencimientos')
def verificar_vencimientos_route():
    """Ruta para verificar vencimientos manualmente"""
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'})
    
    try:
        verificar_vencimientos()
        cuentas_vencidas = Cuenta.query.filter_by(vencida=True).count()
        
        # Crear notificación
        notif = Notificacion(
            servicio='Sistema',
            cliente='Automático',
            tipo='Verificación de Vencimientos',
            estado=f'Completada - {cuentas_vencidas} cuentas vencidas'
        )
        db.session.add(notif)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Verificación completada. {cuentas_vencidas} cuentas vencidas encontradas.',
            'cuentas_vencidas': cuentas_vencidas
        })
    except Exception as e:
        return jsonify({'error': f'Error en verificación: {str(e)}'})

@app.route('/enviar_whatsapp/<int:id>')
def enviar_whatsapp_route(id):
    """Envía mensaje de WhatsApp para una cuenta específica"""
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'})
    
    cuenta = Cuenta.query.get_or_404(id)
    
    if not cuenta.telefono:
        return jsonify({'error': 'Esta cuenta no tiene número de teléfono'})
    
    # Crear mensaje
    mensaje = f"""🎬 HPLAY - Recordatorio de Cuenta

Servicio: {cuenta.servicio}
Cliente: {cuenta.cliente}
Usuario: {cuenta.usuario}
Contraseña: {cuenta.password}

Fecha de vencimiento: {cuenta.fecha_fin or 'No especificada'}

Por favor, renueva tu suscripción para continuar disfrutando del servicio.

Saludos, Equipo HPLAY 🎬"""
    
    try:
        # Enviar en segundo plano
        def enviar_en_segundo_plano():
            resultado = enviar_whatsapp(cuenta.telefono, mensaje)
            if resultado:
                # Crear notificación de éxito
                notif = Notificacion(
                    servicio=cuenta.servicio,
                    cliente=cuenta.cliente,
                    tipo='WhatsApp Enviado',
                    estado='Exitoso'
                )
                db.session.add(notif)
                db.session.commit()
            else:
                # Crear notificación de error
                notif = Notificacion(
                    servicio=cuenta.servicio,
                    cliente=cuenta.cliente,
                    tipo='WhatsApp Error',
                    estado='Fallido'
                )
                db.session.add(notif)
                db.session.commit()
        
        thread = threading.Thread(target=enviar_en_segundo_plano)
        thread.start()
        
        return jsonify({
            'success': True,
            'message': f'Enviando WhatsApp a {cuenta.telefono}...',
            'telefono': cuenta.telefono
        })
        
    except Exception as e:
        return jsonify({'error': f'Error enviando WhatsApp: {str(e)}'})

@app.route('/refrescar_datos')
def refrescar_datos():
    """Refresca los datos del dashboard"""
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'})
    
    try:
        verificar_vencimientos()
        cuentas = Cuenta.query.all()
        
        resultado = []
        for cuenta in cuentas:
            resultado.append({
                'id': cuenta.id,
                'servicio': cuenta.servicio,
                'cliente': cuenta.cliente,
                'num_cliente': cuenta.num_cliente,
                'metodo': cuenta.metodo,
                'precio': cuenta.precio,
                'telefono': cuenta.telefono,
                'fecha_inicio': cuenta.fecha_inicio,
                'fecha_fin': cuenta.fecha_fin,
                'usuario': cuenta.usuario,
                'password': cuenta.password,
                'vencida': cuenta.vencida
            })
        
        return jsonify({
            'success': True,
            'cuentas': resultado,
            'total': len(resultado)
        })
        
    except Exception as e:
        return jsonify({'error': f'Error refrescando datos: {str(e)}'})

@app.route('/notificaciones')
def ver_notificaciones():
    """Muestra el historial de notificaciones"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    notificaciones = Notificacion.query.order_by(Notificacion.fecha.desc()).all()
    return render_template('notificaciones.html', notificaciones=notificaciones)

@app.route('/estadisticas')
def estadisticas_detalladas():
    """Muestra estadísticas detalladas"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cuentas = Cuenta.query.all()
    
    # Estadísticas por servicio
    servicios = {}
    for cuenta in cuentas:
        servicio = cuenta.servicio
        if servicio not in servicios:
            servicios[servicio] = {'total': 0, 'vencidas': 0, 'activas': 0}
        
        servicios[servicio]['total'] += 1
        if cuenta.vencida:
            servicios[servicio]['vencidas'] += 1
        else:
            servicios[servicio]['activas'] += 1
    
    # Estadísticas por método de pago
    metodos = {}
    for cuenta in cuentas:
        metodo = cuenta.metodo or 'Sin método'
        if metodo not in metodos:
            metodos[metodo] = 0
        metodos[metodo] += 1
    
    return render_template('estadisticas.html', 
                         servicios=servicios, 
                         metodos=metodos, 
                         total_cuentas=len(cuentas))

@app.route('/cancelar_whatsapp_programado/<int:notif_id>')
def cancelar_whatsapp_programado(notif_id):
    """Ruta para cancelar WhatsApp programado"""
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'})
    
    try:
        # Buscar la notificación
        notif = Notificacion.query.get_or_404(notif_id)
        
        # Solo permitir cancelar si está programado
        if 'Programado (' in notif.estado and 's)' in notif.estado:
            notif.estado = 'Cancelado por usuario'
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'WhatsApp programado cancelado exitosamente'
            })
        else:
            return jsonify({
                'error': 'No se puede cancelar esta notificación'
            })
            
    except Exception as e:
        return jsonify({'error': f'Error cancelando WhatsApp: {str(e)}'})

if __name__ == '__main__':
    # Iniciar verificación automática de vencimientos
    def verificar_automaticamente():
        while True:
            verificar_vencimientos()
            time.sleep(3600)  # Verificar cada hora
    
    thread_auto = threading.Thread(target=verificar_automaticamente, daemon=True)
    thread_auto.start()
    
    # Para Vercel, usar configuración por defecto
    app.run(debug=False)
