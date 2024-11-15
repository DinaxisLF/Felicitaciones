from flask import jsonify, request, redirect, session
from functools import wraps
from flask_login import login_user, logout_user, UserMixin, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from . import docentes_api


class User(UserMixin):
    def __init__(self, id, email):
        self.id = id
        self.email = email

    def get_id(self):
        return str(self.id)
    




@docentes_api.route('/api/login', methods=['POST'])
def login():
    try:
        from app import db
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
            
        cursor = db.connection.cursor()
        cursor.execute("SELECT ID_administrador, Correo, Contraseña FROM administrador WHERE Correo = %s", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user[2], password):  
            user_obj = User(id=user[0], email=user[1])
            login_user(user_obj)
            print(user[2], password)
            return jsonify({"message": "Login exitoso", "success": True}), 200
    
    
        return jsonify({"message": "Credenciales incorrectas", "success": False}), 401

    except Exception as ex:
        print(ex)
        return jsonify({"message": "Login failed", "success": False}), 500

@docentes_api.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect('/')

@docentes_api.route('/api/register', methods =['POST'])
@login_required
def register():
    try:
        from app import db
        data = request.json
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()


        if not name or not email or not password:
            return jsonify({"message": "All fields are required", "success": False}), 400

        password_hash = generate_password_hash(password)
        
        cursor = db.connection.cursor()
        cursor.execute("INSERT INTO administrador (Nombre, Correo, Contraseña) VALUES (%s, %s, %s)", (name, email, password_hash))
        db.connection.commit()
        cursor.close()
        
        return jsonify({"message": "Administrador Creado", "success": True}), 200

    except Exception as ex:
        print(ex)
        return jsonify({"message": "Registro ha fallado", "success": False}), 500