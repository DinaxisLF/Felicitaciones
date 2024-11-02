from flask import Blueprint, request, jsonify, current_app
from app import db 

#  blueprint 
filters_blueprint = Blueprint('filters_blueprint', __name__)

@filters_blueprint.route('/filtrar_docentes', methods=['GET'])
def filtrar_docentes():
    try:

        query = "SELECT * FROM docente WHERE 1=1"
        params = []

        nombre = request.args.get('nombre', default='')
        estado = request.args.get('estado', default='')
        mes_nacimiento = request.args.get('mesNacimiento', default='')

        if nombre:
            query += " AND Nombre LIKE %s"
            params.append(f"%{nombre}%")
        
        if estado:
            query += " AND Estado = %s"
            params.append(estado)
        
        if mes_nacimiento:
            query += " AND MONTH(Fecha_de_Nacimiento) = %s"
            params.append(mes_nacimiento)

        cursor = db.connection.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        docentes = []
        for row in results:
            docentes.append({
                'ID_docente': row[0],
                'Nombre': row[1],
                'Apellido': row[2],
                'Fecha_de_Nacimiento': row[3],
                'Correo': row[4],
                'Estado': row[5]
            })
        
        cursor.close()
        return jsonify(docentes)

    except Exception as e:
        
        current_app.logger.error(f"Error al ejecutar la consulta de filtrado: {e}")
        return jsonify({"error": "Error al obtener datos de docentes"}), 500
