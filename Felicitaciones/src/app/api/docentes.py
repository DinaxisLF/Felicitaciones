from flask import jsonify, request
from app.api import docentes_api


@docentes_api.route('/api/docentes', methods=['GET'])
def list():
    try:

        per_page = int(request.args.get('per_page', 4))  # Num filas por pag
        page = int(request.args.get('page', 1))  # Pagina inicial
        offset = (page - 1) * per_page

        from app import db
        cursor = db.connection.cursor()
        query = "SELECT * FROM docente LIMIT %s OFFSET %s"
        cursor.execute(query, (per_page, offset))
        response = cursor.fetchall()

        teachers = [
            {
                'ID_docente': teacher[0],
                'Nombre': teacher[1],
                'Apellido': teacher[2],
                'Fecha_de_Nacimiento': teacher[3],
                'Correo': teacher[4],
                'Estado': teacher[5]
            }
            for teacher in response
        ]

        # Contar total
        cursor.execute("SELECT COUNT(*) FROM docente")
        total_docentes = cursor.fetchone()[0]
        total_pages = (total_docentes + per_page - 1) // per_page

        return jsonify({
            'teachers': teachers,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'total_docentes': total_docentes
        }), 200

    except Exception as ex:
        return jsonify({'message': "Error en la consulta"}), 500


@docentes_api.route('/api/docentes/<id>', methods=['GET'])
def consult(id):
    try:
        from app import db
        cursor = db.connection.cursor()
        query = "SELECT * FROM docente where ID_docente = '{0}'".format(id)
        cursor.execute(query)
        response = cursor.fetchone()
        
        if response != None:
            data={'ID_docente':response[0],'Nombre':response[1], 'Apellido':response[2], 
                'Fecha_de_Nacimiento':response[3], 'Correo':response[4], 'Estado':response[5]}
            return jsonify({'docentes_api':data, 'message': "Consulta Realizada (docentes_api)"})
        else:
            return jsonify({'message':"Docente no encontrado"})
    except Exception as ex:
        return jsonify({'message':"Error en la consulta"})


@docentes_api.route('/api/docentes', methods=['POST'])
def registrar_docente():
    try:
        from app import db
        nombre = request.json['Nombre']
        apellido = request.json['Apellido']
        fecha_nacimiento = request.json['Fecha_de_Nacimiento']
        correo = request.json['Correo']
        estado = request.json['Estado']
        
        cursor = db.connection.cursor()
        query = """INSERT INTO docente (Nombre, Apellido, Fecha_de_Nacimiento, Correo, Estado) 
                   VALUES (%s, %s, %s, %s, %s)"""
        print(query)  # Agregar print para revisar la consulta
        cursor.execute(query, (nombre, apellido, fecha_nacimiento, correo, estado))
        db.connection.commit()
        
        return jsonify({'message': "Docente Registrado.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False}), 404

    

@docentes_api.route('/api/docentes/<id>', methods = ["PUT"])
def actulizar_docente(id):
    try:
        from app import db
        cursor = db.connection.cursor()
        query = """UPDATE docente SET Nombre = '{0}' , Apellido = '{1}', Fecha_de_Nacimiento = '{2}', 
        Correo = '{3}', Estado  = '{4}' WHERE ID_docente = '{5}'""".format(request.json['Nombre'], request.json['Apellido']
                                                            ,request.json['Fecha_de_Nacimiento']
                                                            , request.json['Correo']
                                                            ,request.json['Estado'], id)
        cursor.execute(query)
        db.connection.commit()
        return jsonify({'message': "Docente Actualizado.", 'exito': True})
    except Exception as ex:
        return jsonify({'message':"Docente no encontrado",'exito': False})


@docentes_api.route('/api/docentes/<id>', methods = ['DELETE'])
def eliminar_docente(id):
    try:
        from app import db
        cursor = db.connection.cursor()
        query = "DELETE FROM docente WHERE ID_docente = '{0}'".format(id)
        cursor.execute(query)
        db.connection.commit()
        return jsonify({'message': "Docente eliminado", 'exito': True})
    except Exception as ex:
        return jsonify({'message':"Docente no encontrado",'exito': False})



