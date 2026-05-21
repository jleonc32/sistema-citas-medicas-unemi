# Importamos session, redirect y url_for
from flask import render_template, request, session, redirect, url_for 
from conexion import app, db
from modelos import Usuario, Paciente
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

# 2. RUTA DE INICIO DE SESIÓN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.password_hash, password):
            # ¡AQUÍ ESTÁ LA MAGIA DE LA MEMORIA! Guardamos sus datos en la sesión
            session['id_usuario'] = usuario.id_usuario
            session['nombre'] = usuario.nombre
            
            # Lo redirigimos a su zona privada
            return redirect(url_for('dashboard'))
        else:
            return "<h2>❌ Error: Correo o contraseña incorrectos.</h2>"

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

# ==========================================
# ENCENDIDO DEL SERVIDOR
# ==========================================
if __name__ == '__main__':
    app.run(debug=True, port=5000)