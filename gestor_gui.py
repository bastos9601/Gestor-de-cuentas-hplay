import tkinter as tk
from tkinter import messagebox, simpledialog
from cryptography.fernet import Fernet
import os
import json
from datetime import datetime, timedelta
import pywhatkit as pwk
import threading
import time

# ---------- Sistema de Login ----------
def mostrar_login():
    """Muestra la ventana de login"""
    login_window = tk.Tk()
    login_window.title("🔐 Acceso al Sistema HPLAY")
    login_window.geometry("400x300")
    login_window.configure(bg='#2c3e50')
    login_window.resizable(False, False)
    
    # Centrar la ventana
    login_window.geometry("+%d+%d" % (login_window.winfo_screenwidth()//2 - 200, 
                                      login_window.winfo_screenheight()//2 - 150))
    
    # Frame principal
    frame_login = tk.Frame(login_window, bg='#2c3e50')
    frame_login.pack(padx=40, pady=40, fill=tk.BOTH, expand=True)
    
    # Título
    titulo_login = tk.Label(frame_login, 
                           text="🔐 ACCESO AL SISTEMA ", 
                           font=('Arial', 18, 'bold'), 
                           fg='#ecf0f1', 
                           bg='#2c3e50')
    titulo_login.pack(pady=(0, 20))
    
    subtitulo_login = tk.Label(frame_login, 
                              text="Ingresa tu clave de acceso", 
                              font=('Arial', 10), 
                              fg='#bdc3c7', 
                              bg='#2c3e50')
    subtitulo_login.pack(pady=(0, 30))
    
    # Campo de contraseña
    frame_password = tk.Frame(frame_login, bg='#2c3e50')
    frame_password.pack(fill=tk.X, pady=(0, 20))
    
    label_password = tk.Label(frame_password, 
                             text="🔑 Clave:", 
                             font=('Arial', 11, 'bold'),
                             fg='#ecf0f1', 
                             bg='#2c3e50')
    label_password.pack(anchor=tk.W, pady=(0, 5))
    
    # Variable para almacenar la contraseña
    password_var = tk.StringVar()
    
    # Campo de entrada de contraseña
    campo_password = tk.Entry(frame_password, 
                             show="*", 
                             width=30,
                             font=('Arial', 12),
                             relief=tk.FLAT,
                             bd=0,
                             bg='#ecf0f1',
                             fg='#2c3e50',
                             insertbackground='#3498db')
    campo_password.pack(fill=tk.X, pady=(0, 10))
    campo_password.focus()
    
    # Función para obtener el valor del campo
    def obtener_clave():
        return campo_password.get()
    
    # Botón de acceso
    def verificar_acceso():
        clave = obtener_clave()
        print(f"🔍 DEBUG: Verificando acceso con clave: '{clave}'")
        
        # Verificación directa para debug
        if clave == "admin123":
            print("🔍 DEBUG: Clave correcta detectada")
            login_window.destroy()
            iniciar_aplicacion()
        else:
            print(f"🔍 DEBUG: Clave incorrecta. Esperada: 'admin123', Recibida: '{clave}'")
            messagebox.showerror("❌ Error", "Clave incorrecta. Intenta nuevamente.")
            campo_password.delete(0, tk.END)
            campo_password.focus()
    
    btn_acceder = tk.Button(frame_login, 
                            text="🚀 ACCEDER", 
                            font=('Arial', 12, 'bold'),
                            command=verificar_acceso,
                            bg='#27ae60',
                            fg='white',
                            relief=tk.FLAT,
                            bd=0,
                            padx=30,
                            pady=10,
                            cursor='hand2')
    btn_acceder.pack(pady=(10, 0))
    
    # Botón para salir
    btn_salir = tk.Button(frame_login, 
                          text="❌ SALIR", 
                          font=('Arial', 10),
                          command=login_window.quit,
                          bg='#e74c3c',
                          fg='white',
                          relief=tk.FLAT,
                          bd=0,
                          padx=20,
                          pady=5,
                          cursor='hand2')
    btn_salir.pack(pady=(20, 0))
    
    # Bind Enter key
    campo_password.bind('<Return>', lambda e: verificar_acceso())
    
    # Centrar el cursor en el campo de contraseña
    campo_password.focus()
    
    return login_window

def verificar_clave(clave):
    """Verifica si la clave es correcta"""
    # Clave por defecto: "admin123" (puedes cambiarla)
    CLAVE_DEFAULT = "admin123"
    
    print(f"🔍 DEBUG: Clave ingresada: '{clave}'")
    print(f"🔍 DEBUG: Longitud de clave ingresada: {len(clave)}")
    
    # Si existe un archivo de configuración, leer la clave desde ahí
    if os.path.exists("config.json"):
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
                clave_guardada = config.get("clave_acceso", CLAVE_DEFAULT)
                print(f"🔍 DEBUG: Clave guardada en config.json: '{clave_guardada}'")
        except Exception as e:
            print(f"🔍 DEBUG: Error leyendo config.json: {e}")
            clave_guardada = CLAVE_DEFAULT
    else:
        print(f"🔍 DEBUG: No existe config.json, usando clave por defecto")
        clave_guardada = CLAVE_DEFAULT
    
    print(f"🔍 DEBUG: Clave guardada final: '{clave_guardada}'")
    print(f"🔍 DEBUG: Longitud de clave guardada: {len(clave_guardada)}")
    print(f"🔍 DEBUG: ¿Son iguales?: {clave == clave_guardada}")
    
    return clave == clave_guardada

def cambiar_clave():
    """Permite cambiar la clave de acceso"""
    clave_actual = simpledialog.askstring("Cambiar Clave", 
                                         "Ingresa la clave actual:", 
                                         show="*")
    if clave_actual and verificar_clave(clave_actual):
        nueva_clave = simpledialog.askstring("Cambiar Clave", 
                                           "Ingresa la nueva clave:", 
                                           show="*")
        if nueva_clave:
            confirmar_clave = simpledialog.askstring("Cambiar Clave", 
                                                   "Confirma la nueva clave:", 
                                                   show="*")
            if nueva_clave == confirmar_clave:
                # Guardar nueva clave
                config = {"clave_acceso": nueva_clave}
                with open("config.json", "w") as f:
                    json.dump(config, f)
                messagebox.showinfo("✅ Éxito", "Clave cambiada correctamente")
            else:
                messagebox.showerror("❌ Error", "Las claves no coinciden")
        else:
            messagebox.showwarning("⚠️ Advertencia", "No se ingresó nueva clave")
    else:
        messagebox.showerror("❌ Error", "Clave actual incorrecta")

def iniciar_aplicacion():
    """Inicia la aplicación principal después del login exitoso"""
    global ventana, fernet, cuentas
    
    # Generar o cargar clave de encriptación
    if not os.path.exists("clave.key"):
        generar_clave()
    
    fernet = Fernet(cargar_clave())
    cuentas = cargar_cuentas(fernet)
    
    # Crear ventana principal
    ventana = tk.Tk()
    ventana.title("🎬 Gestor de Cuentas Streaming Pro HPLAY")
    ventana.geometry("1100x500")
    ventana.configure(bg='#2c3e50')
    ventana.resizable(True, True)
    
    # Configurar estilo de la ventana
    ventana.option_add('*Font', 'Arial 9')
    
    # Frame principal con padding
    frame_principal = tk.Frame(ventana, bg='#2c3e50')
    frame_principal.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
    
    # Título principal
    titulo_frame = tk.Frame(frame_principal, bg='#2c3e50')
    titulo_frame.pack(fill=tk.X, pady=(0, 20))
    
    titulo = tk.Label(titulo_frame, 
                     text="🎬 GESTOR DE CUENTAS STREAMING HPLAY", 
                     font=('Arial', 24, 'bold'), 
                     fg='#ecf0f1', 
                     bg='#2c3e50')
    titulo.pack()
    
    subtitulo = tk.Label(titulo_frame, 
                        text="Administra tus suscripciones de streaming de forma segura", 
                        font=('Arial', 10), 
                        fg='#bdc3c7', 
                        bg='#2c3e50')
    subtitulo.pack()
    
    # Botón para cambiar clave
    btn_cambiar_clave = tk.Button(titulo_frame, 
                                 text="🔐 Cambiar Clave", 
                                 font=('Arial', 9),
                                 command=cambiar_clave,
                                 bg='#8e44ad',
                                 fg='white',
                                 relief=tk.FLAT,
                                 bd=0,
                                 padx=10,
                                 pady=2,
                                 cursor='hand2')
    btn_cambiar_clave.pack(pady=(10, 0))
    
    # Continuar con el resto de la interfaz...
    crear_interfaz_principal(frame_principal)
    
    # Iniciar verificación automática en segundo plano
    thread_verificacion = threading.Thread(target=verificar_vencimientos, daemon=True)
    thread_verificacion.start()
    
    ventana.mainloop()

def estilo_boton(frame_destino, texto, comando, color_bg, color_fg='white'):
    """Crea un botón con estilo moderno"""
    btn = tk.Button(frame_destino, 
                    text=texto, 
                    command=comando,
                    font=('Arial', 10, 'bold'),
                    bg=color_bg,
                    fg=color_fg,
                    relief=tk.FLAT,
                    bd=0,
                    padx=20,
                    pady=10,
                    cursor='hand2',
                    activebackground=color_bg,
                    activeforeground=color_fg)
    
    # Efectos hover
    def on_enter(e):
        btn['bg'] = color_bg
        btn['fg'] = 'white'
    
    def on_leave(e):
        btn['bg'] = color_bg
        btn['fg'] = color_fg
    
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    
    return btn

def actualizar_estadisticas():
    """Actualiza las estadísticas mostradas en la interfaz"""
    global label_stats
    if 'label_stats' in globals() and label_stats:
        total_cuentas = len(cuentas)
        if total_cuentas == 0:
            stats_text = "No hay cuentas registradas"
        else:
            # Contar por método de pago
            metodos = {}
            for datos in cuentas.values():
                metodo = datos.get('metodo', 'Sin método')
                metodos[metodo] = metodos.get(metodo, 0) + 1
            
            # Contar por cliente
            clientes = {}
            for datos in cuentas.values():
                cliente = datos.get('cliente', 'Sin cliente')
                clientes[cliente] = clientes.get(cliente, 0) + 1
            
            # Calcular precio total
            precio_total = 0
            for datos in cuentas.values():
                precio_str = datos.get('precio', '0')
                try:
                    # Extraer solo números del precio (ej: "S/. 25.00" -> 25.00)
                    precio_limpio = ''.join(c for c in precio_str if c.isdigit() or c == '.')
                    if precio_limpio:
                        precio_total += float(precio_limpio)
                except:
                    continue
            
            stats_text = f"Total: {total_cuentas} cuentas | Clientes únicos: {len(clientes)} | Métodos: {len(metodos)} | Precio total: S/. {precio_total:.2f}"
        
        label_stats.config(text=stats_text)

def crear_interfaz_principal(frame_principal):
    """Crea la interfaz principal de la aplicación"""
    global lista, label_stats, campo_busqueda
    
    # Frame para el buscador con estilo moderno
    frame_busqueda = tk.Frame(frame_principal, bg='#34495e', relief=tk.RAISED, bd=2)
    frame_busqueda.pack(fill=tk.X, pady=(0, 20))
    
    etiqueta_buscar = tk.Label(frame_busqueda, 
                               text="🔍 Buscar:", 
                               font=('Arial', 11, 'bold'),
                               fg='#ecf0f1', 
                               bg='#34495e')
    etiqueta_buscar.pack(side=tk.LEFT, padx=(15, 10), pady=10)
    
    campo_busqueda = tk.Entry(frame_busqueda, 
                              width=60, 
                              font=('Arial', 10),
                              relief=tk.FLAT,
                              bd=0,
                              bg='#ecf0f1',
                              fg='#2c3e50',
                              insertbackground='#3498db')
    campo_busqueda.pack(side=tk.LEFT, padx=(0, 10), pady=10)
    campo_busqueda.bind('<KeyRelease>', buscar_cuentas)
    
    btn_limpiar = tk.Button(frame_busqueda, 
                            text="❌", 
                            font=('Arial', 10, 'bold'),
                            command=lambda: [campo_busqueda.delete(0, tk.END), mostrar_cuentas()],
                            bg='#e74c3c',
                            fg='white',
                            relief=tk.FLAT,
                            bd=0,
                            padx=15,
                            cursor='hand2')
    btn_limpiar.pack(side=tk.LEFT, padx=(0, 15), pady=10)
    
    # Frame para la lista con estilo moderno
    frame_lista = tk.Frame(frame_principal, bg='#34495e', relief=tk.RAISED, bd=2)
    frame_lista.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
    
    # Título de la lista
    titulo_lista = tk.Label(frame_lista, 
                            text="📋 CUENTAS REGISTRADAS", 
                            font=('Arial', 12, 'bold'),
                            fg='#ecf0f1', 
                            bg='#34495e')
    titulo_lista.pack(pady=(10, 5))
    
    # Frame para la lista y scrollbars
    frame_lista_interno = tk.Frame(frame_lista, bg='#34495e')
    frame_lista_interno.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
    
    lista = tk.Listbox(frame_lista_interno, 
                       width=120, 
                       height=15,
                       font=('Consolas', 9),
                       bg='#ecf0f1',
                       fg='#2c3e50',
                       relief=tk.FLAT,
                       bd=0,
                       selectbackground='#3498db',
                       selectforeground='white')
    
    # Scrollbars
    scrollbar_y = tk.Scrollbar(frame_lista_interno, orient=tk.VERTICAL, command=lista.yview)
    scrollbar_x = tk.Scrollbar(frame_lista_interno, orient=tk.HORIZONTAL, command=lista.xview)
    lista.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    
    # Grid layout para lista y scrollbars
    lista.grid(row=0, column=0, sticky='nsew')
    scrollbar_y.grid(row=0, column=1, sticky='ns')
    scrollbar_x.grid(row=1, column=0, sticky='ew')
    
    frame_lista_interno.grid_rowconfigure(0, weight=1)
    frame_lista_interno.grid_columnconfigure(0, weight=1)
    
    # Frame para botones
    frame_botones = tk.Frame(frame_principal, bg='#34495e', relief=tk.RAISED, bd=2)
    frame_botones.pack(fill=tk.X, pady=(0, 20))
    
    # Crear botones con estilo
    btn_agregar = estilo_boton(frame_botones, "➕ Agregar Cuenta", agregar_cuenta, '#27ae60')
    btn_agregar.pack(side=tk.LEFT, padx=5, pady=10)
    
    btn_editar = estilo_boton(frame_botones, "✏️ Editar Cuenta", editar_cuenta, '#f39c12')
    btn_editar.pack(side=tk.LEFT, padx=5, pady=10)
    
    btn_eliminar = estilo_boton(frame_botones, "🗑️ Eliminar Cuenta", eliminar_cuenta, '#e74c3c')
    btn_eliminar.pack(side=tk.LEFT, padx=5, pady=10)
    
    btn_refrescar = estilo_boton(frame_botones, "🔄 Refrescar", mostrar_cuentas, '#3498db')
    btn_refrescar.pack(side=tk.LEFT, padx=5, pady=10)
    
    # Botones adicionales para WhatsApp
    btn_whatsapp = estilo_boton(frame_botones, "📱 Enviar WhatsApp", enviar_whatsapp_manual, '#25d366')
    btn_whatsapp.pack(side=tk.LEFT, padx=5, pady=10)
    
    btn_verificar = estilo_boton(frame_botones, "⏰ Verificar Vencimientos", verificar_vencimientos_manual, '#e67e22')
    btn_verificar.pack(side=tk.LEFT, padx=5, pady=10)
    
    # Botón para probar verificación inmediata
    btn_probar = estilo_boton(frame_botones, "🧪 Probar Verificación", probar_verificacion_inmediata, '#9b59b6')
    btn_probar.pack(side=tk.LEFT, padx=5, pady=10)
    
    # Botón para reenviar información de cuenta
    btn_reenviar = estilo_boton(frame_botones, "📤 Reenviar Info", reenviar_info_cuenta, '#1abc9c')
    btn_reenviar.pack(side=tk.LEFT, padx=5, pady=10)
    
    # Botón para probar funciones
    btn_test = estilo_boton(frame_botones, "🧪 Test Funciones", probar_funciones_basicas, '#e74c3c')
    btn_test.pack(side=tk.LEFT, padx=5, pady=10)
    
    # Frame de estadísticas
    frame_stats = tk.Frame(frame_principal, bg='#34495e', relief=tk.RAISED, bd=2)
    frame_stats.pack(fill=tk.X, pady=(20, 0))
    
    titulo_stats = tk.Label(frame_stats, 
                           text="📊 ESTADÍSTICAS", 
                           font=('Arial', 11, 'bold'),
                           fg='#ecf0f1', 
                           bg='#34495e')
    titulo_stats.pack(pady=(10, 5))
    
    # Frame para las estadísticas
    stats_interno = tk.Frame(frame_stats, bg='#34495e')
    stats_interno.pack(pady=(0, 10))
    
    label_stats = tk.Label(stats_interno, 
                          text="Cargando estadísticas...", 
                          font=('Arial', 9),
                          fg='#bdc3c7', 
                          bg='#34495e')
    label_stats.pack()
    
    mostrar_cuentas()

# ---------- Seguridad ----------
def generar_clave():
    clave = Fernet.generate_key()
    with open("clave.key", "wb") as archivo_clave:
        archivo_clave.write(clave)

def cargar_clave():
    return open("clave.key", "rb").read()

def cargar_cuentas(fernet):
    if os.path.exists("cuentas.enc"):
        with open("cuentas.enc", "rb") as archivo:
            datos_cifrados = archivo.read()
        datos = fernet.decrypt(datos_cifrados).decode()
        return json.loads(datos)
    else:
        return {}

def guardar_cuentas(fernet, cuentas):
    datos = json.dumps(cuentas).encode()
    datos_cifrados = fernet.encrypt(datos)
    with open("cuentas.enc", "wb") as archivo:
        archivo.write(datos_cifrados)

# ---------- WhatsApp y Notificaciones ----------
def verificar_vencimientos():
    """Verifica cuentas próximas a vencer y envía recordatorios"""
    print("🔍 Iniciando verificación automática de vencimientos...")
    
    while True:
        try:
            fecha_actual = datetime.now()
            cuentas_vencidas = []
            cuentas_proximas = []
            
            print(f"⏰ Verificando vencimientos - {fecha_actual.strftime('%d/%m/%Y %H:%M')}")
            
            for servicio, datos in cuentas.items():
                fecha_fin_str = datos.get('fecha_fin', 'Sin fecha')
                if fecha_fin_str != 'Sin fecha':
                    try:
                        fecha_fin = datetime.strptime(fecha_fin_str, "%d/%m/%Y")
                        dias_restantes = (fecha_fin - fecha_actual).days
                        
                        if dias_restantes < 0:
                            cuentas_vencidas.append((servicio, datos, dias_restantes))
                            print(f"🚨 {servicio} - VENCIDA hace {abs(dias_restantes)} días")
                        elif dias_restantes <= 3:
                            cuentas_proximas.append((servicio, datos, dias_restantes))
                            print(f"⚠️ {servicio} - Vence en {dias_restantes} días")
                    except ValueError:
                        continue
            
            # Enviar recordatorios para cuentas próximas a vencer
            if cuentas_proximas:
                print(f"📱 Enviando {len(cuentas_proximas)} recordatorios...")
                for servicio, datos, dias in cuentas_proximas:
                    try:
                        enviar_recordatorio_whatsapp(servicio, datos, dias)
                        print(f"✅ Recordatorio enviado a {datos.get('cliente', 'Cliente')} - {servicio}")
                    except Exception as e:
                        print(f"❌ Error enviando recordatorio a {servicio}: {e}")
            else:
                print("✅ No hay cuentas próximas a vencer")
            
            # Marcar cuentas vencidas
            if cuentas_vencidas:
                print(f"🚨 Procesando {len(cuentas_vencidas)} cuentas vencidas...")
                for servicio, datos, dias in cuentas_vencidas:
                    try:
                        marcar_cuenta_vencida(servicio, datos)
                        print(f"✅ Cuenta vencida marcada: {servicio}")
                    except Exception as e:
                        print(f"❌ Error marcando cuenta vencida {servicio}: {e}")
            
            print(f"⏳ Esperando 24 horas para la siguiente verificación...")
            # Esperar 24 horas antes de la siguiente verificación
            time.sleep(86400)  # 24 horas en segundos
            
        except Exception as e:
            print(f"❌ Error en verificación automática: {e}")
            print("⏳ Reintentando en 1 hora...")
            time.sleep(3600)  # Esperar 1 hora si hay error

def enviar_recordatorio_whatsapp(servicio, datos, dias_restantes):
    """Envía recordatorio por WhatsApp"""
    try:
        cliente = datos.get('cliente', 'Cliente')
        num_cliente = datos.get('num_cliente', 'Sin número')
        fecha_fin = datos.get('fecha_fin', 'Sin fecha')
        telefono = datos.get('telefono', '')
        
        print(f"📱 Preparando WhatsApp para {cliente} - {servicio}")
        
        # Verificar que tenga teléfono
        if not telefono or telefono == 'Sin teléfono':
            print(f"❌ {cliente} no tiene teléfono configurado")
            return
        
        # Mensaje personalizado
        if dias_restantes == 0:
            mensaje = f"🚨 URGENTE: Tu cuenta de {servicio} vence HOY ({fecha_fin}). Por favor, renueva tu suscripción para evitar interrupciones."
        elif dias_restantes == 1:
            mensaje = f"⚠️ IMPORTANTE: Tu cuenta de {servicio} vence MAÑANA ({fecha_fin}). Te recomendamos renovar tu suscripción."
        else:
            mensaje = f"📱 Recordatorio: Tu cuenta de {servicio} vence en {dias_restantes} días ({fecha_fin}). Cliente: {cliente} - N°: {num_cliente}"
        
        print(f"📝 Mensaje preparado: {mensaje[:50]}...")
        
        # Formatear número para WhatsApp
        if not telefono.startswith('+'):
            numero_telefono = '+51' + telefono  # Código de Perú
        else:
            numero_telefono = telefono
        
        print(f"📞 Enviando a: {numero_telefono}")
        
        # Enviar mensaje usando pywhatkit
        pwk.sendwhatmsg_instantly(
            numero_telefono,
            mensaje,
            wait_time=20,  # Aumentar tiempo de espera
            tab_close=True,
            close_time=5    # Cerrar después de 5 segundos
        )
        
        print(f"✅ WhatsApp enviado exitosamente a {cliente}")
        
        # Registrar el envío
        registrar_notificacion(servicio, cliente, mensaje, "Enviado")
        
    except Exception as e:
        print(f"❌ Error enviando WhatsApp a {cliente}: {e}")
        registrar_notificacion(servicio, datos.get('cliente', 'Cliente'), f"Error: {str(e)}", "Fallido")

def marcar_cuenta_vencida(servicio, datos):
    """Marca una cuenta como vencida"""
    try:
        # Agregar marca de vencida
        datos['vencida'] = True
        datos['fecha_vencimiento'] = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        # Guardar cambios
        guardar_cuentas(fernet, cuentas)
        
        # Enviar mensaje de vencimiento
        enviar_mensaje_vencimiento(servicio, datos)
        
    except Exception as e:
        print(f"Error marcando cuenta vencida {servicio}: {e}")

def enviar_mensaje_vencimiento(servicio, datos):
    """Envía mensaje cuando la cuenta ya venció"""
    try:
        cliente = datos.get('cliente', 'Cliente')
        numero_telefono = datos.get('telefono', datos.get('num_cliente', ''))
        
        if numero_telefono and numero_telefono != 'Sin número':
            if not numero_telefono.startswith('+'):
                numero_telefono = '+51' + numero_telefono
            
            mensaje = f"🚨 TU CUENTA DE {servicio} HA VENCIDO. Por favor, contacta con nosotros para renovar tu suscripción y evitar interrupciones en el servicio."
            
            pwk.sendwhatmsg_instantly(
                numero_telefono,
                mensaje,
                wait_time=15,
                tab_close=True,
                close_time=3
            )
            
            registrar_notificacion(servicio, cliente, mensaje, "Vencimiento")
            
    except Exception as e:
        print(f"Error enviando mensaje de vencimiento: {e}")

def registrar_notificacion(servicio, cliente, mensaje, estado):
    """Registra las notificaciones enviadas"""
    try:
        if not os.path.exists("notificaciones.json"):
            notificaciones = []
        else:
            with open("notificaciones.json", "r", encoding="utf-8") as f:
                notificaciones = json.load(f)
        
        notificacion = {
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "servicio": servicio,
            "cliente": cliente,
            "mensaje": mensaje,
            "estado": estado
        }
        
        notificaciones.append(notificacion)
        
        with open("notificaciones.json", "w", encoding="utf-8") as f:
            json.dump(notificaciones, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"Error registrando notificación: {e}")

def enviar_confirmacion_cuenta_nueva(servicio, cliente, telefono, usuario, password, fecha_inicio, fecha_fin, metodo, num_cliente, precio):
    """Envía confirmación de cuenta nueva por WhatsApp"""
    try:
        print(f"📱 Enviando confirmación de cuenta nueva a {cliente}")
        
        # Formatear número para WhatsApp
        if not telefono.startswith('+'):
            numero_telefono = '+51' + telefono  # Código de Perú
        else:
            numero_telefono = telefono
        
        # Mensaje de confirmación con todos los detalles
        mensaje = f"""🎉 ¡CUENTA ACTIVADA EXITOSAMENTE!

📺 Servicio: {servicio}
👤 Cliente: {cliente}
🔢 Número de Cliente: {num_cliente}
💳 Método de Pago: {metodo}
💰 Precio: {precio}

📧 Correo/Usuario: {usuario}
🔑 Contraseña: {password}

📅 Fecha de Inicio: {fecha_inicio}
⏰ Fecha de Vencimiento: {fecha_fin}

✅ Tu cuenta está lista para usar
📱 Cualquier consulta, contáctanos

¡Disfruta de tu suscripción! 🎬"""
        
        print(f"📝 Mensaje de confirmación preparado")
        print(f"📞 Enviando a: {numero_telefono}")
        
        # Enviar mensaje usando pywhatkit
        pwk.sendwhatmsg_instantly(
            numero_telefono,
            mensaje,
            wait_time=20,
            tab_close=True,
            close_time=5
        )
        
        print(f"✅ Confirmación enviada exitosamente a {cliente}")
        
        # Registrar la notificación
        registrar_notificacion(servicio, cliente, "Confirmación de cuenta nueva", "Enviado")
        
    except Exception as e:
        print(f"❌ Error enviando confirmación a {cliente}: {e}")
        registrar_notificacion(servicio, cliente, f"Error confirmación: {str(e)}", "Fallido")
        raise e

def enviar_whatsapp_manual():
    """Envía WhatsApp manualmente a la cuenta seleccionada"""
    seleccion = lista.curselection()
    if not seleccion:
        messagebox.showwarning("Error", "Selecciona una cuenta para enviar WhatsApp")
        return
    
    linea_seleccionada = lista.get(seleccion[0])
    servicio = extraer_servicio_de_linea(linea_seleccionada)
    
    if servicio in cuentas:
        datos = cuentas[servicio]
        telefono = datos.get('telefono', '')
        
        if not telefono or telefono == 'Sin teléfono':
            messagebox.showwarning("Error", "Esta cuenta no tiene número de teléfono configurado")
            return
        
        # Mensaje personalizado
        mensaje = f"📱 Hola {datos.get('cliente', 'Cliente')}, te recordamos que tu cuenta de {servicio} está activa. Precio: {datos.get('precio', 'Sin precio')}. Si necesitas renovar o tienes alguna consulta, no dudes en contactarnos."
        
        try:
            # Formatear número
            if not telefono.startswith('+'):
                telefono = '+51' + telefono
            
            # Enviar mensaje
            pwk.sendwhatmsg_instantly(
                telefono,
                mensaje,
                wait_time=15,
                tab_close=True,
                close_time=3
            )
            
            registrar_notificacion(servicio, datos.get('cliente', 'Cliente'), mensaje, "Manual")
            messagebox.showinfo("Éxito", f"WhatsApp enviado a {datos.get('cliente', 'Cliente')} ✅")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar WhatsApp: {e}")
    else:
        messagebox.showerror("Error", "No se pudo encontrar la cuenta seleccionada")

def verificar_vencimientos_manual():
    """Verifica vencimientos manualmente"""
    try:
        fecha_actual = datetime.now()
        cuentas_proximas = []
        cuentas_vencidas = []
        
        for servicio, datos in cuentas.items():
            fecha_fin_str = datos.get('fecha_fin', 'Sin fecha')
            if fecha_fin_str != 'Sin fecha':
                try:
                    fecha_fin = datetime.strptime(fecha_fin_str, "%d/%m/%Y")
                    dias_restantes = (fecha_fin - fecha_actual).days
                    
                    if dias_restantes < 0:
                        cuentas_vencidas.append((servicio, datos, dias_restantes))
                    elif dias_restantes <= 3:
                        cuentas_proximas.append((servicio, datos, dias_restantes))
                except ValueError:
                    continue
        
        # Mostrar resumen
        mensaje = f"📊 VERIFICACIÓN DE VENCIMIENTOS\n\n"
        mensaje += f"✅ Cuentas activas: {len(cuentas) - len(cuentas_proximas) - len(cuentas_vencidas)}\n"
        mensaje += f"⚠️ Cuentas próximas a vencer: {len(cuentas_proximas)}\n"
        mensaje += f"🚨 Cuentas vencidas: {len(cuentas_vencidas)}\n\n"
        
        if cuentas_proximas:
            mensaje += "📱 CUENTAS PRÓXIMAS A VENCER:\n"
            for servicio, datos, dias in cuentas_proximas:
                mensaje += f"• {servicio} - {datos.get('cliente', 'Cliente')} - Vence en {dias} días\n"
        
        if cuentas_vencidas:
            mensaje += "\n🚨 CUENTAS VENCIDAS:\n"
            for servicio, datos, dias in cuentas_vencidas:
                mensaje += f"• {servicio} - {datos.get('cliente', 'Cliente')} - Vencida hace {abs(dias)} días\n"
        
        messagebox.showinfo("Verificación de Vencimientos", mensaje)
        
        # Actualizar lista
        mostrar_cuentas()
        
    except Exception as e:
        messagebox.showerror("Error", f"Error en la verificación: {e}")

def probar_verificacion_inmediata():
    """Prueba la verificación inmediatamente sin esperar"""
    try:
        print("🧪 INICIANDO PRUEBA DE VERIFICACIÓN INMEDIATA...")
        
        fecha_actual = datetime.now()
        cuentas_vencidas = []
        cuentas_proximas = []
        
        print(f"⏰ Verificando vencimientos - {fecha_actual.strftime('%d/%m/%Y %H:%M')}")
        
        for servicio, datos in cuentas.items():
            fecha_fin_str = datos.get('fecha_fin', 'Sin fecha')
            if fecha_fin_str != 'Sin fecha':
                try:
                    fecha_fin = datetime.strptime(fecha_fin_str, "%d/%m/%Y")
                    dias_restantes = (fecha_fin - fecha_actual).days
                    
                    if dias_restantes < 0:
                        cuentas_vencidas.append((servicio, datos, dias_restantes))
                        print(f"🚨 {servicio} - VENCIDA hace {abs(dias_restantes)} días")
                    elif dias_restantes <= 3:
                        cuentas_proximas.append((servicio, datos, dias_restantes))
                        print(f"⚠️ {servicio} - Vence en {dias_restantes} días")
                except ValueError:
                    continue
        
        # Enviar recordatorios para cuentas próximas a vencer
        if cuentas_proximas:
            print(f"📱 Enviando {len(cuentas_proximas)} recordatorios...")
            for servicio, datos, dias in cuentas_proximas:
                try:
                    enviar_recordatorio_whatsapp(servicio, datos, dias)
                    print(f"✅ Recordatorio enviado a {datos.get('cliente', 'Cliente')} - {servicio}")
                except Exception as e:
                    print(f"❌ Error enviando recordatorio a {servicio}: {e}")
        else:
            print("✅ No hay cuentas próximas a vencer")
        
        # Marcar cuentas vencidas
        if cuentas_vencidas:
            print(f"🚨 Procesando {len(cuentas_vencidas)} cuentas vencidas...")
            for servicio, datos, dias in cuentas_vencidas:
                try:
                    marcar_cuenta_vencida(servicio, datos)
                    print(f"✅ Cuenta vencida marcada: {servicio}")
                except Exception as e:
                    print(f"❌ Error marcando cuenta vencida {servicio}: {e}")
        
        print("🧪 PRUEBA DE VERIFICACIÓN COMPLETADA")
        messagebox.showinfo("Prueba Completada", "Verificación de prueba ejecutada. Revisa la consola para ver los detalles.")
        
        # Actualizar lista
        mostrar_cuentas()
        
    except Exception as e:
        print(f"❌ Error en prueba de verificación: {e}")
        messagebox.showerror("Error", f"Error en la prueba: {e}")

def reenviar_info_cuenta():
    """Reenvía la información completa de la cuenta seleccionada por WhatsApp"""
    seleccion = lista.curselection()
    if not seleccion:
        messagebox.showwarning("Error", "Selecciona una cuenta para reenviar la información")
        return
    
    linea_seleccionada = lista.get(seleccion[0])
    servicio = extraer_servicio_de_linea(linea_seleccionada)
    
    if servicio in cuentas:
        datos = cuentas[servicio]
        cliente = datos.get('cliente', 'Cliente')
        num_cliente = datos.get('num_cliente', 'Sin número')
        metodo = datos.get('metodo', 'Sin método')
        precio = datos.get('precio', 'Sin precio')
        telefono = datos.get('telefono', 'Sin teléfono')
        usuario = datos.get('usuario', 'Sin usuario')
        password = datos.get('password', 'Sin contraseña')
        fecha_inicio = datos.get('fecha_inicio', 'Sin fecha')
        fecha_fin = datos.get('fecha_fin', 'Sin fecha')

        mensaje = f"""🎉 ¡INFORMACIÓN DE CUENTA!

📺 Servicio: {servicio}
👤 Cliente: {cliente}
🔢 Número de Cliente: {num_cliente}
💳 Método de Pago: {metodo}
💰 Precio: {precio}

📧 Correo/Usuario: {usuario}
🔑 Contraseña: {password}

📅 Fecha de Inicio: {fecha_inicio}
⏰ Fecha de Vencimiento: {fecha_fin}

✅ Tu cuenta está lista para usar
📱 Cualquier consulta, contáctanos

¡Disfruta de tu suscripción! 🎬"""

        try:
            if not telefono or telefono == 'Sin teléfono':
                messagebox.showwarning("Error", f"No se puede reenviar la información para {cliente} - {servicio} porque no tiene número de teléfono configurado.")
                return
            
            if not telefono.startswith('+'):
                numero_telefono = '+51' + telefono
            else:
                numero_telefono = telefono

            pwk.sendwhatmsg_instantly(
                numero_telefono,
                mensaje,
                wait_time=20,
                tab_close=True,
                close_time=5
            )
            messagebox.showinfo("Éxito", f"Información de la cuenta de {servicio} reenviada a {cliente} ✅")
            registrar_notificacion(servicio, cliente, "Información de cuenta reenviada", "Enviado")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo reenviar la información de la cuenta de {servicio}: {e}")
            registrar_notificacion(servicio, cliente, f"Error reenvío: {str(e)}", "Fallido")
    else:
        messagebox.showerror("Error", "No se pudo encontrar la cuenta seleccionada")

def probar_funciones_basicas():
    """Prueba las funciones básicas para verificar que funcionen"""
    try:
        print("🧪 INICIANDO PRUEBA DE FUNCIONES BÁSICAS...")
        print("=" * 60)
        
        # Verificar que hay cuentas
        if not cuentas:
            messagebox.showinfo("Test", "No hay cuentas para probar. Agrega una cuenta primero.")
            return
        
        # Mostrar información de debug
        print(f"📊 Total de cuentas: {len(cuentas)}")
        print(f"🔑 Servicios disponibles: {list(cuentas.keys())}")
        print()
        
        # Verificar formato de visualización
        if lista.size() > 0:
            print("📋 ANÁLISIS DE LA LISTA:")
            print("-" * 40)
            
            for i in range(min(3, lista.size())):  # Mostrar máximo 3 líneas
                linea = lista.get(i)
                print(f"📝 Línea {i+1}: {linea}")
                
                # Probar extracción del servicio
                servicio_extraido = extraer_servicio_de_linea(linea)
                print(f"🔍 Servicio extraído: '{servicio_extraido}'")
                
                # Verificar si existe en cuentas
                if servicio_extraido in cuentas:
                    print(f"✅ Servicio encontrado en cuentas: {servicio_extraido}")
                    datos = cuentas[servicio_extraido]
                    print(f"📋 Datos de la cuenta: {datos}")
                else:
                    print(f"❌ Servicio NO encontrado en cuentas: {servicio_extraido}")
                    print(f"🔍 Comparando con: {list(cuentas.keys())}")
                
                print("-" * 40)
        else:
            print("❌ La lista está vacía")
        
        print("=" * 60)
        messagebox.showinfo("Test Completado", "Prueba de funciones completada. Revisa la consola para ver los detalles.")
        
    except Exception as e:
        print(f"❌ Error en prueba de funciones: {e}")
        messagebox.showerror("Error", f"Error en la prueba: {e}")

# ---------- Interfaz ----------
if not os.path.exists("clave.key"):
    generar_clave()

clave = cargar_clave()
fernet = Fernet(clave)
cuentas = cargar_cuentas(fernet)

def mostrar_cuentas():
    lista.delete(0, tk.END)
    for servicio, datos in cuentas.items():
        cliente = datos.get('cliente', 'Sin cliente')
        metodo = datos.get('metodo', 'Sin método')
        num_cliente = datos.get('num_cliente', 'Sin número')
        precio = datos.get('precio', 'Sin precio')
        telefono = datos.get('telefono', 'Sin teléfono')
        fecha_inicio = datos.get('fecha_inicio', 'Sin fecha')
        fecha_fin = datos.get('fecha_fin', 'Sin fecha')
        vencida = datos.get('vencida', False)
        
        # Formato más legible con espacios consistentes
        estado = "🚨 VENCIDA" if vencida else "✅ ACTIVA"
        
        # Asegurar que el formato sea exactamente el mismo en todas las funciones
        linea_formato = f"{servicio:<20} | Cliente: {cliente:<15} | N°: {num_cliente:<8} | Método: {metodo:<12} | Precio: {precio:<10} | Tel: {telefono:<12} | Inicio: {fecha_inicio:<10} | Fin: {fecha_fin:<10} | {estado} | {datos['usuario']:<25} | {datos['password']}"
        
        lista.insert(tk.END, linea_formato)
        
        # Debug: imprimir el formato para verificar
        print(f"📝 Línea formateada: {linea_formato[:50]}...")
    
    # Actualizar estadísticas
    actualizar_estadisticas()

def agregar_cuenta():
    servicio = simpledialog.askstring("Servicio", "Nombre del servicio (Netflix, Disney+, etc):")
    cliente = simpledialog.askstring("Cliente", "Nombre del cliente (Juan, María, etc):")
    num_cliente = simpledialog.askstring("Número de Cliente", "Número de cliente:")
    metodo = simpledialog.askstring("Método de Pago", "Método de pago (Tarjeta, PayPal, etc):")
    precio = simpledialog.askstring("Precio", "Precio de la suscripción (ej: S/. 25.00):")
    telefono = simpledialog.askstring("Teléfono WhatsApp", "Número de teléfono para WhatsApp (ej: 999888777):")
    usuario = simpledialog.askstring("Usuario", "Correo o usuario:")
    password = simpledialog.askstring("Contraseña", "Contraseña:", show="*")

    if servicio and usuario and password:
        # Fechas automáticas
        fecha_inicio = datetime.now().strftime("%d/%m/%Y")
        fecha_fin = (datetime.now() + timedelta(days=30)).strftime("%d/%m/%Y")
        
        cuentas[servicio] = {
            "cliente": cliente,
            "num_cliente": num_cliente,
            "metodo": metodo,
            "precio": precio,
            "telefono": telefono,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "usuario": usuario,
            "password": password
        }
        guardar_cuentas(fernet, cuentas)
        mostrar_cuentas()
        
        # Enviar mensaje de confirmación por WhatsApp
        if telefono and telefono != 'Sin teléfono':
            try:
                enviar_confirmacion_cuenta_nueva(servicio, cliente, telefono, usuario, password, fecha_inicio, fecha_fin, metodo, num_cliente, precio)
                messagebox.showinfo("Éxito", f"Cuenta de {servicio} guardada ✅\nWhatsApp enviado al cliente 📱")
            except Exception as e:
                messagebox.showinfo("Éxito", f"Cuenta de {servicio} guardada ✅\nError enviando WhatsApp: {e}")
        else:
            messagebox.showinfo("Éxito", f"Cuenta de {servicio} guardada ✅")

def extraer_servicio_de_linea(linea):
    """Extrae el nombre del servicio de una línea de la lista de manera robusta"""
    try:
        # Intentar con el formato estándar primero
        if " | " in linea:
            servicio = linea.split(" | ")[0].strip()
            print(f"🔍 Extraído con formato estándar: '{servicio}'")
            return servicio
        
        # Si no funciona, intentar con otros separadores
        if ":" in linea:
            servicio = linea.split(":")[0].strip()
            print(f"🔍 Extraído con formato alternativo: '{servicio}'")
            return servicio
        
        # Si nada funciona, devolver la línea completa
        print(f"🔍 No se pudo extraer, devolviendo línea completa: '{linea}'")
        return linea.strip()
        
    except Exception as e:
        print(f"❌ Error extrayendo servicio: {e}")
        return linea.strip()

def eliminar_cuenta():
    seleccion = lista.curselection()
    if not seleccion:
        messagebox.showwarning("Error", "Selecciona una cuenta para eliminar")
        return
    
    # Extraer el servicio de manera robusta
    linea_seleccionada = lista.get(seleccion[0])
    servicio = extraer_servicio_de_linea(linea_seleccionada)
    
    print(f"🔍 Intentando eliminar servicio: '{servicio}'")
    print(f"📋 Servicios disponibles: {list(cuentas.keys())}")
    print(f"📝 Línea completa: {linea_seleccionada}")
    
    if servicio in cuentas:
        del cuentas[servicio]
        guardar_cuentas(fernet, cuentas)
        mostrar_cuentas()
        messagebox.showinfo("Eliminado", f"Cuenta de {servicio} eliminada 🗑️")
    else:
        messagebox.showerror("Error", f"No se encontró la cuenta '{servicio}' para eliminar")

def editar_cuenta():
    seleccion = lista.curselection()
    if not seleccion:
        messagebox.showwarning("Error", "Selecciona una cuenta para editar")
        return
    
    # Extraer el servicio de manera robusta
    linea_seleccionada = lista.get(seleccion[0])
    servicio = extraer_servicio_de_linea(linea_seleccionada)
    
    print(f"🔍 Intentando editar servicio: '{servicio}'")
    print(f"📋 Servicios disponibles: {list(cuentas.keys())}")
    print(f"📝 Línea completa: {linea_seleccionada}")
    
    if servicio in cuentas:
        # Obtener datos actuales
        datos_actuales = cuentas[servicio]
        
        # Diálogos para editar
        nuevo_cliente = simpledialog.askstring("Editar Cliente", 
                                             f"Cliente actual: {datos_actuales.get('cliente', 'Sin cliente')}\nNuevo cliente:", 
                                             initialvalue=datos_actuales.get('cliente', ''))
        
        if nuevo_cliente is None:  # Usuario canceló
            return
            
        nuevo_num_cliente = simpledialog.askstring("Editar Número de Cliente", 
                                                 f"Número actual: {datos_actuales.get('num_cliente', 'Sin número')}\nNuevo número:", 
                                                 initialvalue=datos_actuales.get('num_cliente', ''))
        
        if nuevo_num_cliente is None:  # Usuario canceló
            return
            
        nuevo_metodo = simpledialog.askstring("Editar Método de Pago", 
                                            f"Método actual: {datos_actuales.get('metodo', 'Sin método')}\nNuevo método:", 
                                            initialvalue=datos_actuales.get('metodo', ''))
        
        if nuevo_metodo is None:  # Usuario canceló
            return
            
        nuevo_precio = simpledialog.askstring("Editar Precio", 
                                            f"Precio actual: {datos_actuales.get('precio', 'Sin precio')}\nNuevo precio:", 
                                            initialvalue=datos_actuales.get('precio', ''))
        
        if nuevo_precio is None:  # Usuario canceló
            return
            
        nuevo_telefono = simpledialog.askstring("Editar Teléfono WhatsApp", 
                                              f"Teléfono actual: {datos_actuales.get('telefono', 'Sin teléfono')}\nNuevo teléfono:", 
                                              initialvalue=datos_actuales.get('telefono', ''))
        
        if nuevo_telefono is None:  # Usuario canceló
            return
            
        nuevo_usuario = simpledialog.askstring("Editar Usuario", 
                                             f"Usuario actual: {datos_actuales['usuario']}\nNuevo usuario:", 
                                             initialvalue=datos_actuales['usuario'])
        
        if nuevo_usuario is None:  # Usuario canceló
            return
            
        nueva_password = simpledialog.askstring("Editar Contraseña", 
                                               f"Contraseña actual: {'*' * len(datos_actuales['password'])}\nNueva contraseña:", 
                                               show="*", 
                                               initialvalue=datos_actuales['password'])
        
        if nueva_password is None:  # Usuario canceló
            return
        
        # Actualizar datos
        cuentas[servicio] = {
            "cliente": nuevo_cliente,
            "num_cliente": nuevo_num_cliente,
            "metodo": nuevo_metodo,
            "precio": nuevo_precio,
            "telefono": nuevo_telefono,
            "fecha_inicio": datos_actuales.get('fecha_inicio', 'Sin fecha'),
            "fecha_fin": datos_actuales.get('fecha_fin', 'Sin fecha'),
            "usuario": nuevo_usuario,
            "password": nueva_password
        }
        guardar_cuentas(fernet, cuentas)
        mostrar_cuentas()
        
        # Enviar mensaje de actualización por WhatsApp
        if nuevo_telefono and nuevo_telefono != 'Sin teléfono':
            try:
                enviar_actualizacion_cuenta(servicio, nuevo_cliente, nuevo_telefono, nuevo_usuario, nueva_password, 
                                          datos_actuales.get('fecha_inicio', 'Sin fecha'), 
                                          datos_actuales.get('fecha_fin', 'Sin fecha'), 
                                          nuevo_metodo, nuevo_num_cliente, nuevo_precio)
                messagebox.showinfo("Editado", f"Cuenta de {servicio} actualizada ✏️\nWhatsApp de actualización enviado 📱")
            except Exception as e:
                messagebox.showinfo("Editado", f"Cuenta de {servicio} actualizada ✏️\nError enviando WhatsApp: {e}")
        else:
            messagebox.showinfo("Editado", f"Cuenta de {servicio} actualizada ✏️")
    else:
        messagebox.showerror("Error", f"No se encontró la cuenta '{servicio}' para editar")

def enviar_actualizacion_cuenta(servicio, cliente, telefono, usuario, password, fecha_inicio, fecha_fin, metodo, num_cliente, precio):
    """Envía un mensaje de actualización de cuenta por WhatsApp"""
    try:
        print(f"📱 Preparando WhatsApp para actualización de {cliente} - {servicio}")
        
        # Formatear número para WhatsApp
        if not telefono.startswith('+'):
            numero_telefono = '+51' + telefono  # Código de Perú
        else:
            numero_telefono = telefono
        
        # Mensaje de actualización con todos los detalles
        mensaje = f"""🎉 ¡CUENTA ACTUALIZADA EXITOSAMENTE!

📺 Servicio: {servicio}
👤 Cliente: {cliente}
🔢 Número de Cliente: {num_cliente}
💳 Método de Pago: {metodo}
💰 Precio: {precio}

📧 Correo/Usuario: {usuario}
🔑 Contraseña: {password}

📅 Fecha de Inicio: {fecha_inicio}
⏰ Fecha de Vencimiento: {fecha_fin}

✅ Tu cuenta está lista para usar
📱 Cualquier consulta, contáctanos

¡Disfruta de tu suscripción! 🎬"""
        
        print(f"📝 Mensaje de actualización preparado")
        print(f"📞 Enviando a: {numero_telefono}")
        
        # Enviar mensaje usando pywhatkit
        pwk.sendwhatmsg_instantly(
            numero_telefono,
            mensaje,
            wait_time=20,
            tab_close=True,
            close_time=5
        )
        
        print(f"✅ WhatsApp de actualización enviado exitosamente a {cliente}")
        
        # Registrar la notificación
        registrar_notificacion(servicio, cliente, "Actualización de cuenta", "Enviado")
        
    except Exception as e:
        print(f"❌ Error enviando WhatsApp de actualización a {cliente}: {e}")
        registrar_notificacion(servicio, cliente, f"Error actualización: {str(e)}", "Fallido")

def buscar_cuentas(*args):
    global campo_busqueda, lista
    if 'campo_busqueda' not in globals() or 'lista' not in globals():
        return  # Si las variables no están disponibles, salir
    
    termino_busqueda = campo_busqueda.get().lower()
    lista.delete(0, tk.END)
    
    if termino_busqueda == "":
        # Si no hay búsqueda, mostrar todas las cuentas
        for servicio, datos in cuentas.items():
            cliente = datos.get('cliente', 'Sin cliente')
            metodo = datos.get('metodo', 'Sin método')
            num_cliente = datos.get('num_cliente', 'Sin número')
            precio = datos.get('precio', 'Sin precio')
            telefono = datos.get('telefono', 'Sin teléfono')
            fecha_inicio = datos.get('fecha_inicio', 'Sin fecha')
            fecha_fin = datos.get('fecha_fin', 'Sin fecha')
            vencida = datos.get('vencida', False)
            
            # Formato más legible con espacios consistentes
            estado = "🚨 VENCIDA" if vencida else "✅ ACTIVA"
            linea_formato = f"{servicio:<20} | Cliente: {cliente:<15} | N°: {num_cliente:<8} | Método: {metodo:<12} | Precio: {precio:<10} | Tel: {telefono:<12} | Inicio: {fecha_inicio:<10} | Fin: {fecha_fin:<10} | {estado} | {datos['usuario']:<25} | {datos['password']}"
            lista.insert(tk.END, linea_formato)
    else:
        # Filtrar cuentas que coincidan con la búsqueda
        cuentas_encontradas = 0
        for servicio, datos in cuentas.items():
            cliente = datos.get('cliente', 'Sin cliente')
            metodo = datos.get('metodo', 'Sin método')
            num_cliente = datos.get('num_cliente', 'Sin número')
            precio = datos.get('precio', 'Sin precio')
            telefono = datos.get('telefono', 'Sin teléfono')
            fecha_inicio = datos.get('fecha_inicio', 'Sin fecha')
            fecha_fin = datos.get('fecha_fin', 'Sin fecha')
            vencida = datos.get('vencida', False)
            
            if (termino_busqueda in servicio.lower() or 
                termino_busqueda in cliente.lower() or
                termino_busqueda in num_cliente.lower() or
                termino_busqueda in metodo.lower() or
                termino_busqueda in precio.lower() or
                termino_busqueda in telefono.lower() or
                termino_busqueda in fecha_inicio.lower() or
                termino_busqueda in fecha_fin.lower() or
                termino_busqueda in datos['usuario'].lower() or 
                termino_busqueda in datos['password'].lower()):
                # Formato más legible con espacios consistentes
                estado = "🚨 VENCIDA" if vencida else "✅ ACTIVA"
                linea_formato = f"{servicio:<20} | Cliente: {cliente:<15} | N°: {num_cliente:<8} | Método: {metodo:<12} | Precio: {precio:<10} | Tel: {telefono:<12} | Inicio: {fecha_inicio:<10} | Fin: {fecha_fin:<10} | {estado} | {datos['usuario']:<25} | {datos['password']}"
                lista.insert(tk.END, linea_formato)
                cuentas_encontradas += 1
        
        # Mostrar mensaje si no se encontraron resultados
        if cuentas_encontradas == 0:
            lista.insert(tk.END, f"🔍 No se encontraron cuentas que coincidan con '{termino_busqueda}'")
    
    # Actualizar estadísticas
    actualizar_estadisticas()



# ---------- Código Principal ----------
if __name__ == "__main__":
    # Mostrar ventana de login
    login_window = mostrar_login()
    login_window.mainloop()
