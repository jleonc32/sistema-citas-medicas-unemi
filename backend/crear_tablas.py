from conexion import app, db
import modelos 

with app.app_context():
    db.create_all()
    
    print("===========================================================")
    print("✅ ¡MAGIA PURA BRO! Tablas creadas con éxito en tu MySQL.")
    print("===========================================================")