# Importamos la app y la base de datos que ya configuramos en conexion.py
from conexion import app, db

# ==========================================
# RUTAS DE LA PÁGINA WEB
# ==========================================
@app.route('/')
def inicio():
    return "<h1>¡Hola UNEMI! 🎓</h1> <p>El servidor de Citas Médicas está funcionando al 100% 🚀</p>"

# ==========================================
# ENCENDIDO DEL SERVIDOR
# ==========================================
if __name__ == '__main__':
    # debug=True hace que el servidor se actualice solo cada vez que guardes un cambio
    app.run(debug=True, port=5000)