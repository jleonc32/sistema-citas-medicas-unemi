from conexion import app, db
from modelos import Usuario, Medico
from werkzeug.security import generate_password_hash

# Abrimos el contexto de Flask para poder hablar con la base de datos
with app.app_context():
    print("Inyectando médicos en la base de datos...")

    # ==========================================
    # MÉDICO 1: Dr. Gregory House
    # ==========================================
    clave_house = generate_password_hash("doc123")
    usuario_house = Usuario(cedula="0987654321", nombre="Dr. Gregory House", email="house@unemi.edu.ec", password_hash=clave_house)
    db.session.add(usuario_house)
    db.session.commit() 

    medico_house = Medico(
        id_usuario=usuario_house.id_usuario, 
        especialidad_id=1, 
        telefono="0999999999",
        horario_atencion={"lunes": "08:00-12:00", "miercoles": "14:00-18:00"} 
    )
    db.session.add(medico_house)

    # ==========================================
    # MÉDICO 2: Dra. Meredith Grey
    # ==========================================
    clave_grey = generate_password_hash("doc123")
    usuario_grey = Usuario(cedula="0911111111", nombre="Dra. Meredith Grey", email="grey@unemi.edu.ec", password_hash=clave_grey)
    db.session.add(usuario_grey)
    db.session.commit()

    medico_grey = Medico(
        id_usuario=usuario_grey.id_usuario, 
        especialidad_id=2, 
        telefono="0988888888",
        horario_atencion={"martes": "09:00-13:00", "jueves": "09:00-13:00"}
    )
    db.session.add(medico_grey)
    
    # Guardamos todos los cambios finales
    db.session.commit()

    print("===========================================================")
    print("✅ ¡MAGIA PURA! Los doctores ya están listos para atender.")
    print("===========================================================")