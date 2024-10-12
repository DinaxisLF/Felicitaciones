from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config


app=Flask(__name__)
conexion = MySQL(app)


@app.route('/docentes', methods=['GET'])
def list():
    try:
        cursor = conexion.connection.cursor()
        query = "SELECT * FROM docente"
        cursor.execute(query)
        response = cursor.fetchall()
        teachers = []
        
        for teacher in response:
            data={'ID_docente':teacher[0],'Nombre':teacher[1], 'Apellido':teacher[2], 
                'Fecha_de_Nacimiento':teacher[3], 'Correo':teacher[4], 'Estado':teacher[5]}
            teachers.append(data)
        return jsonify({'Docentes':teachers, 'message': "Consulta Realizada (Docentes)"})
    except Exception as ex:
        return jsonify({'message':"Error en la consulta"})

@app.route('/docentes/<id>', methods=['GET'])
def consult(id):
    try:
        cursor = conexion.connection.cursor()
        query = "SELECT * FROM docente where ID_docente = '{0}'".format(id)
        cursor.execute(query)
        response = cursor.fetchone()
        
        if response != None:
            data={'ID_docente':response[0],'Nombre':response[1], 'Apellido':response[2], 
                'Fecha_de_Nacimiento':response[3], 'Correo':response[4], 'Estado':response[5]}
            return jsonify({'Docentes':data, 'message': "Consulta Realizada (Docentes)"})
        else:
            return jsonify({'message':"Docente no encontrado"})
    except Exception as ex:
        return jsonify({'message':"Error en la consulta"})


@app.route('/docentes', methods=['POST'])
def registrar_docente():
    try:
        cursor = conexion.connection.cursor()
        query = """INSERT INTO docente (Nombre, Apellido, Fecha_de_Nacimiento, Correo, Estado) 
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')""".format(request.json['Nombre'], request.json['Apellido']
                                                            ,request.json['Fecha_de_Nacimiento']
                                                            , request.json['Correo']
                                                            ,request.json['Estado'])
        cursor.execute(query)
        conexion.connection.commit()
        return jsonify({'message': "Docente Registrado.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False}), 404
    


@app.route('/docentes/<id>', methods = ['PUT'])
def eliminar_docente(id):
    try:
        cursor = conexion.connection.cursor()
        query = "DELETE FROM docente WHERE ID_docente = '{0}'".format(id)
        cursor.execute(query)
        conexion.connection.commit()
        return jsonify({'message': "Docente eliminado", 'exito': True})
    except Exception as ex:
        return jsonify({'message':"Docente no encontrado",'exito': False})


def page_not_found(error):
    return "<h1>Pagina No Encontrada</h1>" , 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, page_not_found)
    app.run()
