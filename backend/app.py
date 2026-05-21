from flask import render_template, request
from conexion import app, db
from modelos import Usuario, Paciente
# Agregamos "check_password_hash" para verificar la clave
from werkzeug.security import generate_password_hash, check_password_hash 

# ==========================================
# RUTAS DE LA PÁGINA WEB
# ==========================================
@app.route('/')
def inicio():
    return "<h1>¡Hola UNEMI! 🎓</h1> <p>El servidor de Citas Médicas está funcionando al 100% 🚀</p>"

# 1. RUTA DE REGISTRO (Ya la tienes dominada)
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

        return "<h2>¡Registro exitoso, bro! 🎉 Tu cuenta está lista.</h2>"

# 2. NUEVA RUTA: INICIO DE SESIÓN (LOGIN)
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Si entra normal, le mostramos el formulario HTML
    if request.method == 'GET':
        return render_template('login.html')
    
    # Si le da al botón de Entrar
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Buscamos en la base de datos si existe un usuario con ese correo
        usuario = Usuario.query.filter_by(email=email).first()

        # Si el usuario existe y la contraseña coincide con el hash guardado...
        if usuario and check_password_hash(usuario.password_hash, password):
            return f"<h2>¡Bienvenido de vuelta, {usuario.nombre}! 🏥 Tienes acceso al sistema.</h2>"
        else:
            return "<h2>❌ Error: Correo o contraseña incorrectos. Intenta de nuevo.</h2>"

# ==========================================
# ENCENDIDO DEL SERVIDOR
# ==========================================
if __name__ == '__main__':
    app.run(debug=True, port=5000)