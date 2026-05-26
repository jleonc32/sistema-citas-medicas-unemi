# Importamos session, redirect y url_for
from flask import render_template, request, session, redirect, url_for 
from conexion import app, db
from modelos import Usuario, Paciente, Medico, Especialidad, Cita
from werkzeug.security import generate_password_hash, check_password_hash 

# ==========================================
# CONFIGURACIÓN DE SEGURIDAD
# ==========================================
# Flask necesita una llave secreta para encriptar la memoria de la sesión
app.secret_key = 'clave_super_secreta_unemi_2026' 

# ==========================================
# RUTAS DE LA PÁGINA WEB
# ==========================================
@app.route('/')
def inicio():
    return "<h1>¡Hola UNEMI! 🎓</h1> <p>El servidor de Citas Médicas está funcionando al 100% 🚀</p>"

# 1. RUTA DE REGISTRO
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'GET':
        return render_template('registro.html')
    
    if request.method == 'POST':
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        telefono = request.form['telefono']
        direccion = request.form['direccion']

        password_encriptada = generate_password_hash(password)

        nuevo_usuario = Usuario(cedula=cedula, nombre=nombre, email=email, password_hash=password_encriptada)
        db.session.add(nuevo_usuario) 
        db.session.commit() 

        nuevo_paciente = Paciente(id_usuario=nuevo_usuario.id_usuario, telefono=telefono, direccion=direccion)
        db.session.add(nuevo_paciente)
        db.session.commit() 

        return "<h2>¡Registro exitoso! 🎉 Ve a <a href='/login'>Iniciar Sesión</a>.</h2>"

# 2. RUTA DE INICIO DE SESIÓN (LOGIN INTELIGENTE)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.password_hash, password):
            # Guardamos los datos básicos en la memoria de la sesión
            session['id_usuario'] = usuario.id_usuario
            session['nombre'] = usuario.nombre
            
            # EL SEMÁFORO: Verificamos en qué tabla existe este usuario
            es_paciente = Paciente.query.filter_by(id_usuario=usuario.id_usuario).first()
            es_medico = Medico.query.filter_by(id_usuario=usuario.id_usuario).first()

            if es_paciente:
                # Si es paciente, le damos esa etiqueta y lo mandamos a su panel
                session['rol'] = 'paciente'
                return redirect(url_for('dashboard'))
            elif es_medico:
                # Si es médico, le damos la etiqueta y lo mandamos a su panel VIP
                session['rol'] = 'medico'
                return redirect(url_for('dashboard_medico'))
            else:
                return "<h2>❌ Error: Usuario registrado, pero no tiene rol asignado.</h2>"
        else:
            return "<h2>❌ Error: Correo o contraseña incorrectos.</h2>"

# ==========================================
# RUTA VIP: PANEL DEL MÉDICO
# ==========================================
@app.route('/dashboard-medico')
def dashboard_medico():
    # Solo dejamos entrar si hay sesión activa Y si su rol es 'medico'
    if 'id_usuario' in session and session.get('rol') == 'medico':
        return render_template('dashboard_medico.html', nombre_usuario=session['nombre'])
    else:
        # Si un paciente intenta entrar aquí de intruso, lo pateamos al login
        return redirect(url_for('login'))

# 3. NUEVA RUTA: PANEL DE CONTROL PRIVADO (DASHBOARD)
@app.route('/dashboard')
def dashboard():
    # Verificamos si el usuario tiene una sesión activa
    if 'id_usuario' in session:
        # Si tiene memoria, le mostramos su página privada
        return render_template('dashboard.html', nombre_usuario=session['nombre'])
    else:
        # Si un intruso intenta entrar directo a /dashboard, lo pateamos al login
        return redirect(url_for('login'))

# 4. NUEVA RUTA: CERRAR SESIÓN
@app.route('/logout')
def logout():
    # Borramos la memoria
    session.clear()
    return redirect(url_for('login'))

# 5. RUTA PARA VER EL PERFIL DEL USUARIO
@app.route('/perfil')
def perfil():
    if 'id_usuario' in session:
        # Buscamos al usuario en la base de datos por su ID
        usuario = Usuario.query.get(session['id_usuario'])
        # Buscamos sus datos adicionales en la tabla paciente
        paciente = Paciente.query.filter_by(id_usuario=usuario.id_usuario).first()
        
        return render_template('perfil.html', usuario=usuario, paciente=paciente)
    else:
        return redirect(url_for('login'))

# 6. RUTA PARA AGENDAR CITA MEDICA
# ==========================================
# RUTA: AGENDAR NUEVA CITA (PACIENTE)
# ==========================================
@app.route('/agendar', methods=['GET', 'POST'])
def agendar_cita():
    if 'id_usuario' in session and session.get('rol') == 'paciente':
        if request.method == 'GET':
            especialidades = Especialidad.query.all()
            medicos = db.session.query(Medico, Usuario).join(Usuario, Medico.id_usuario == Usuario.id_usuario).all()
            return render_template('agendar_cita.html', especialidades=especialidades, medicos=medicos)
        
        if request.method == 'POST':
            # 1. Atrapamos los datos que el usuario escribió en el HTML
            medico_id = request.form['medico_id']
            fecha = request.form['fecha']
            hora = request.form['hora']
            motivo = request.form['motivo']
            
            # 2. Buscamos cuál es el 'id_paciente' del usuario que está conectado ahora mismo
            paciente_actual = Paciente.query.filter_by(id_usuario=session['id_usuario']).first()
            
            # 3. Armamos la nueva cita para la base de datos
            nueva_cita = Cita(
                paciente_id=paciente_actual.id_paciente,
                medico_id=medico_id,
                fecha=fecha,
                hora=hora,
                modalidad='Presencial', # Por defecto lo ponemos presencial por ahora
                estado='Pendiente',
                motivo_consulta=motivo
            )
            
            # 4. Guardamos en MySQL
            db.session.add(nueva_cita)
            db.session.commit()
            
            # 5. Lo devolvemos al panel azul
            return redirect(url_for('dashboard'))
            
    else:
        return redirect(url_for('login'))
    
#ruta 7
# ==========================================
# RUTA: MIS CITAS (PACIENTE)
# ==========================================
@app.route('/mis-citas')
def mis_citas():
    # Validamos que sea un paciente
    if 'id_usuario' in session and session.get('rol') == 'paciente':
        
        # 1. Buscamos quién es el paciente logueado
        paciente_actual = Paciente.query.filter_by(id_usuario=session['id_usuario']).first()
        
        # 2. Traemos su historial de citas cruzando datos con Médico, Usuario y Especialidad
        citas = db.session.query(Cita, Medico, Usuario, Especialidad)\
            .join(Medico, Cita.medico_id == Medico.id_medico)\
            .join(Usuario, Medico.id_usuario == Usuario.id_usuario)\
            .join(Especialidad, Medico.especialidad_id == Especialidad.id_especialidad)\
            .filter(Cita.paciente_id == paciente_actual.id_paciente)\
            .order_by(Cita.fecha.desc(), Cita.hora.desc()).all()
            
        return render_template('mis_citas.html', citas=citas)
    else:
        return redirect(url_for('login'))

#ruta 8
# ==========================================
# RUTA: SOLICITUDES PENDIENTES (MÉDICO)
# ==========================================
@app.route('/solicitudes-medico')
def solicitudes_medico():
    if 'id_usuario' in session and session.get('rol') == 'medico':
        # 1. Buscamos qué médico está logueado
        medico_actual = Medico.query.filter_by(id_usuario=session['id_usuario']).first()
        
        # 2. Buscamos todas sus citas que estén en estado 'Pendiente'
        # Cruzamos con Paciente y Usuario para saber el nombre de quién pide la cita
        citas_pendientes = db.session.query(Cita, Paciente, Usuario)\
            .join(Paciente, Cita.paciente_id == Paciente.id_paciente)\
            .join(Usuario, Paciente.id_usuario == Usuario.id_usuario)\
            .filter(Cita.medico_id == medico_actual.id_medico)\
            .filter(Cita.estado == 'Pendiente')\
            .order_by(Cita.fecha, Cita.hora).all()
            
        return render_template('solicitudes_medico.html', citas=citas_pendientes)
    else:
        return redirect(url_for('login'))

# ruta 9
# ==========================================
# ACCIÓN: CONFIRMAR O CANCELAR CITA
# ==========================================
@app.route('/actualizar-cita/<int:id_cita>/<string:accion>')
def actualizar_cita(id_cita, accion):
    if 'id_usuario' in session and session.get('rol') == 'medico':
        # Buscamos la cita específica en la base de datos
        cita = Cita.query.get(id_cita)
        
        if cita:
            if accion == 'confirmar':
                cita.estado = 'Confirmada'
            elif accion == 'cancelar':
                cita.estado = 'Cancelada'
            
            # Guardamos el nuevo estado en MySQL
            db.session.commit()
            
        return redirect(url_for('solicitudes_medico'))
    else:
        return redirect(url_for('login'))

# ==========================================
# ENCENDIDO DEL SERVIDOR
# ==========================================
if __name__ == '__main__':
    app.run(debug=True, port=5000)