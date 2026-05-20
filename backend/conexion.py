from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Inicializamos la app y la herramienta de base de datos
app = Flask(__name__)
db = SQLAlchemy()

# ==========================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# ==========================================
# Formato: mysql+pymysql://usuario:contraseña@localhost:3306/nombre_base_datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Leon2004.@localhost:3306/citas_medicas_unemi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enlazamos la base de datos con la app
db.init_app(app)

# ==========================================
# PRUEBA DE CONEXIÓN
# ==========================================
if __name__ == '__main__':
    with app.app_context():
        try:
            # Intentamos "tocar" la base de datos
            db.engine.connect()
            print("=======================================")
            print("✅ ¡ÉXITO BRO! Conectado a MySQL local.")
            print("=======================================")
        except Exception as e:
            print("❌ Error de conexión. Revisa tu contraseña o que MySQL esté encendido.")
            print(f"Detalle: {e}")