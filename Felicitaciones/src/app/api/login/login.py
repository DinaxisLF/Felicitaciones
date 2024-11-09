from flask import request, jsonify, Blueprint


login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")  
    password = data.get("password")  

    try:
        from app import db  
        cursor = db.connection.cursor() 
        cursor.execute("SELECT Contraseña FROM Administrador WHERE Correo = %s", (email,))
        user = cursor.fetchone() 


        if user and user[0] == password: 
            return jsonify({"message": "Login exitoso"}), 200  
        else:
            return jsonify({"message": "Correo o contraseña incorrectos"}), 401 

    except Exception as e:
       
        print(f"Error en el login: {e}")
        return jsonify({"message": "Error en el servidor"}), 500  
