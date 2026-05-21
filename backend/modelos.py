from conexion import db

# 1. TABLA PADRE: USUARIOS
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cedula = db.Column(db.String(10), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

# 2. TABLA HIJA: PACIENTES
class Paciente(db.Model):
    __tablename__ = 'pacientes'
    id_paciente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Llave foránea que conecta con Usuario
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario', ondelete='CASCADE'), unique=True, nullable=False)
    telefono = db.Column(db.String(15))
    direccion = db.Column(db.String(255))

# 3. TABLA HIJA: MEDICOS
class Medico(db.Model):
    __tablename__ = 'medicos'
    id_medico = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Llave foránea que conecta con Usuario
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario', ondelete='CASCADE'), unique=True, nullable=False)
    especialidad_id = db.Column(db.Integer) 
    telefono = db.Column(db.String(15))
    horario_atencion = db.Column(db.JSON) # Guardamos el horario en formato JSON

# 4. TABLA PRINCIPAL: CITAS (Presencial / Virtual)
class Cita(db.Model):
    __tablename__ = 'citas'
    id_cita = db.Column(db.Integer, primary_key=True, autoincrement=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id_paciente', ondelete='CASCADE'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id_medico', ondelete='CASCADE'), nullable=False)
    
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    
    modalidad = db.Column(db.Enum('Presencial', 'Virtual'), nullable=False)
    enlace_virtual = db.Column(db.String(255), nullable=True)
    consultorio_fisico = db.Column(db.String(50), nullable=True)
    
    estado = db.Column(db.Enum('Pendiente', 'Confirmada', 'Cancelada', 'Completada'), default='Pendiente')
    motivo_consulta = db.Column(db.Text)
    costo = db.Column(db.Numeric(10, 2))