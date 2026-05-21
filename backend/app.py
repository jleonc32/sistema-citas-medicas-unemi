from flask import render_template, request # Herramientas para leer HTML y formularios
from conexion import app, db
from modelos import Usuario, Paciente # Importamos las tablas
from werkzeug.security import generate_password_hash # La herramienta de encriptación

# ==========================================
# RUTAS DE LA PÁGINA WEB
# ==========================================
@app.route('/')
def inicio():
    return "<h1>¡Hola UNEMI! 🎓</h1> <p>El servidor de Citas Médicas está funcionando al 100% 🚀</p>"

# RUTA PARA REGISTRAR PACIENTES
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    # Si el usuario solo está visitando la página (GET), le mostramos el HTML del formulario
    if request.method == 'GET':
        return render_template('registro.html')
    
    # Si el usuario presionó el botón de "Registrarse" (POST), procesamos la información
    if request.method == 'POST':
        # 1. Atrapamos los datos que escribió en los inputs del HTML
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        telefono = request.form['telefono']
        direccion = request.form['direccion']

        # 2. Encriptamos la contraseña (¡MAGIA DE SEGURIDAD!)
        password_encriptada = generate_password_hash(password)

        # 3. Creamos al Usuario Padre
        nuevo_usuario = Usuario(
            cedula=cedula, 
            nombre=nombre, 
            email=email, 
            password_hash=password_encriptada
        )
        db.session.add(nuevo_usuario) # Lo preparamos para guardar
        db.session.commit() # Lo guardamos en MySQL para que nos genere su "id_usuario"

        # 4. Creamos al Paciente Hijo (conectándolo con el ID del usuario recién creado)
        nuevo_paciente = Paciente(
            id_usuario=nuevo_usuario.id_usuario,
            telefono=telefono,
            direccion=direccion
        )
        db.session.add(nuevo_paciente)
        db.session.commit() # Guardamos la conexión final

        return "<h2>¡Registro exitoso, bro! 🎉 Tu cuenta está lista y tu clave está segura.</h2>"

# ==========================================
# ENCENDIDO DEL SERVIDOR
# ==========================================
if __name__ == '__main__':
    app.run(debug=True, port=5000)